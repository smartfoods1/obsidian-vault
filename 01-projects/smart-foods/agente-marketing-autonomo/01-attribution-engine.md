---
date: 2026-04-24
type: spec
tags: [smart-foods, marketing, attribution, shopify, smartbrain]
status: draft
---

# Attribution Engine

> Parte de [[index|Agente Marketing Autónomo]]

## Responsabilidad

Unir el ciclo completo de cada campaña: **envío → open → click → order → revenue → margen**.

Sin esta capa, todo lo demás miente. Es prerequisito para cualquier decisión autónoma.

## Tablas nuevas (ops_smart-foods.db)

### `campaign_attribution`

Registro maestro de cada campaña. Una fila por campaña.

```sql
CREATE TABLE campaign_attribution (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id TEXT UNIQUE NOT NULL,      -- ej: REACT45-2604-BRAIN15
    brand_id TEXT NOT NULL DEFAULT 'smart-foods',
    channel TEXT NOT NULL,                 -- 'email' | 'whatsapp'
    trigger_type TEXT NOT NULL,            -- reactivation_45d | b2b_reorder_30d | stock_alert | anniversary | custom
    segment_name TEXT,
    segment_size INTEGER,
    hypothesis TEXT,

    -- Shopify discount
    shopify_price_rule_id TEXT,
    shopify_discount_code_id TEXT,
    discount_code TEXT UNIQUE,
    discount_value REAL,
    discount_type TEXT,                    -- 'percentage' | 'fixed_amount'
    discount_scope TEXT,                   -- 'all' | 'collection:X' | 'product:Y'
    expires_at TIMESTAMP,

    -- Copy (snapshot para auditoría)
    subject_line TEXT,                     -- solo email
    body_snippet TEXT,                     -- primeros 500 chars

    -- Estado
    status TEXT DEFAULT 'draft',           -- draft | testing | active | paused | completed | failed
    sent_at_test TIMESTAMP,
    sent_at_full TIMESTAMP,
    paused_at TIMESTAMP,
    pause_reason TEXT,

    -- Métricas agregadas (actualizan vía webhooks + cron reconcile c/2h)
    sent_count INTEGER DEFAULT 0,
    delivered_count INTEGER DEFAULT 0,
    opened_count INTEGER DEFAULT 0,
    clicked_count INTEGER DEFAULT 0,
    replied_count INTEGER DEFAULT 0,       -- solo WA
    orders_count INTEGER DEFAULT 0,
    revenue_gross REAL DEFAULT 0,
    discount_cost REAL DEFAULT 0,
    revenue_net REAL DEFAULT 0,
    cogs_estimated REAL DEFAULT 0,
    margin_net REAL DEFAULT 0,

    -- Decisión del agente
    agent_decision TEXT,                   -- 'scaled' | 'paused_low_or' | 'paused_low_ctr' | 'paused_low_roas' | 'completed'
    agent_decision_at TIMESTAMP,
    human_override TEXT,                   -- si Andrés respondió SÍ/NO a propuesta

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    closed_at TIMESTAMP
);

CREATE INDEX idx_ca_status ON campaign_attribution(status);
CREATE INDEX idx_ca_brand_created ON campaign_attribution(brand_id, created_at);
CREATE INDEX idx_ca_discount_code ON campaign_attribution(discount_code);
```

### `campaign_events`

Eventos granulares. Una fila por evento.

```sql
CREATE TABLE campaign_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id TEXT NOT NULL,
    event_type TEXT NOT NULL,              -- sent | delivered | opened | clicked | replied | ordered | unsubscribed
    customer_identifier TEXT,              -- email o phone E.164
    customer_id INTEGER,                   -- FK a b2c_customers si existe
    shopify_order_id TEXT,
    order_total REAL,
    metadata_json TEXT,                    -- contexto adicional
    occurred_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (campaign_id) REFERENCES campaign_attribution(campaign_id)
);

CREATE INDEX idx_ce_campaign_event ON campaign_events(campaign_id, event_type);
CREATE INDEX idx_ce_customer ON campaign_events(customer_identifier);
CREATE INDEX idx_ce_order ON campaign_events(shopify_order_id);
```

## Endpoints

### `POST /api/campaigns/attribution/create`

Body:
```json
{
  "brand_id": "smart-foods",
  "channel": "email",
  "trigger_type": "reactivation_45d",
  "segment_name": "d2c_lapsed_45d",
  "segment_size": 1200,
  "hypothesis": "cliente 45d sin recompra responde a -15% en Brain Boost",
  "discount_config": {
    "value": 15,
    "type": "percentage",
    "scope": "all",
    "expires_days": 14
  }
}
```

Respuesta: crea registro en `draft`, devuelve `campaign_id`.

### `POST /api/webhooks/shopify/orders`

Recibe `orders/create` de Shopify. Valida HMAC.

Lógica:
```python
for discount_code in order.discount_codes:
    campaign = db.query(
        "SELECT campaign_id FROM campaign_attribution WHERE discount_code = ?",
        discount_code.code
    )
    if campaign:
        insert_event(campaign_id, 'ordered', customer_email,
                     order.id, order.total_price)
        recompute_metrics(campaign_id)
```

### `GET /api/campaigns/{campaign_id}`

Métricas en vivo de una campaña + últimos 50 eventos.

### `GET /api/campaigns/dashboard?brand_id=smart-foods&days=7`

Vista agregada para el daily briefing. Devuelve campañas activas + paused + completed últimos N días, ordenadas por ROAS.

### `POST /api/campaigns/{campaign_id}/reconcile`

Pull manual de métricas desde Klaviyo + WA para esa campaña. Llamado también por cron cada 2h.

## Webhooks externos

### Shopify

Subscribirse vía Admin API:

```python
# Endpoints a subscribir
topics = [
    "orders/create",
    "orders/updated",
    "orders/cancelled",
    "orders/paid"
]

for topic in topics:
    shopify.webhook.create(
        topic=topic,
        address="https://api.smartbrain.com.ar/api/webhooks/shopify/orders",
        format="json"
    )
```

Validar HMAC con `X-Shopify-Hmac-Sha256` header y `SHOPIFY_WEBHOOK_SECRET`.

### Klaviyo

**No** tiene webhooks reales para opens/clicks. Usar pull:

```python
# cron cada 2h
from klaviyo_api import Klaviyo

for campaign in active_campaigns:
    metrics = klaviyo.get_metric_aggregates(
        metric_id="opened_email",
        filter=f"equals(campaign_id,'{campaign.klaviyo_id}')",
        measurements=["count"]
    )
    update_campaign_metric(campaign.campaign_id, 'opened', metrics.count)
```

### WhatsApp Cloud API

Webhooks ya entran por `journey_proxy.py` (port 18791). Sumar handler:

```python
# journey_proxy.py
def handle_message_status(payload):
    for status in payload.get('statuses', []):
        msg_id = status['id']
        # buscar campaign_id por msg_id (guardado al enviar)
        campaign = db.query("SELECT campaign_id FROM wa_sent_log WHERE wa_message_id = ?", msg_id)
        if campaign:
            event_type = {'delivered': 'delivered', 'read': 'opened', 'sent': 'sent'}.get(status['status'])
            if event_type:
                insert_event(campaign.campaign_id, event_type, status['recipient_id'])
```

Nueva tabla auxiliar `wa_sent_log`:
```sql
CREATE TABLE wa_sent_log (
    wa_message_id TEXT PRIMARY KEY,
    campaign_id TEXT NOT NULL,
    recipient_phone TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Backfill histórico

Script `scripts/backfill_campaign_attribution.py`:

```python
# 1. Lee últimos 90d de orders Shopify via REST API
# 2. Para cada order con discount_codes, check si existe campaign_attribution
# 3. Si no existe → crea registro "legacy" con trigger_type='manual_backfill'
# 4. Inserta campaign_events para 'ordered'
# 5. Recalcula métricas agregadas
```

Útil para:
- Baseline de ROAS histórico
- Validar que el webhook funciona comparando nuevos orders con backfill
- Identificar patrones de cupones que funcionaron bien (input para triggers)

## Cálculo de COGS y margen

```python
# ops_smart-foods.db tiene tabla products con cost_per_unit
def estimate_cogs(order_line_items):
    total_cogs = 0
    for item in order_line_items:
        product = db.get_product(item.sku)
        total_cogs += (product.cost_per_unit or 0) * item.quantity
    return total_cogs

margin_net = revenue_net - cogs_estimated
```

Si `cost_per_unit` es NULL para algún producto → alertar a Andrés/Flo para cargarlo. Sin esto el margen es estimado a 0 y todas las decisiones salen miscalibradas.

## Tests de validación

Antes de ir live:

1. **Webhook Shopify**: crear order de prueba con cupón `TEST-ATTRIBUTION-01` → ver que aparezca `campaign_events` entry en <10s.
2. **Klaviyo reconcile**: lanzar campaña test a 5 emails internos, verificar opens/clicks en DB al cabo de 2h.
3. **WA status tracking**: enviar template WA a 3 números internos, verificar `delivered` + `opened` en `campaign_events`.
4. **Backfill**: correr backfill 30d, contar orders con discount_code vs registros creados (deben coincidir).

## Riesgos conocidos

- **Shopify API version 2026-01** — cambios de schema en `webhooks/orders/create`. Validar payload antes de deploy.
- **Klaviyo rate limit**: 75 req/s burst, 700 req/min. Con 10 campañas activas y reconcile cada 2h estamos bajísimo, pero considerar si escala.
- **WA templates rate limit**: 80 mensajes/segundo. Para campañas >500 destinatarios chunkeá en batches.
- **Orders canceladas**: webhook `orders/cancelled` debe revertir métricas. No olvidar.
- **Refunds parciales**: si un order con cupón se reembolsa parcialmente, ajustar revenue_gross proporcional.
