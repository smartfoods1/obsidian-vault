---
date: 2026-04-24
type: spec
tags: [smart-foods, marketing, triggers, automation]
status: draft
---

# Trigger Engine

> Parte de [[index|Agente Marketing Autónomo]]

## Responsabilidad

Detectar **oportunidades de campaña sin input humano**. Cada trigger produce una propuesta de campaña que pasa al Decision Layer.

## Cron principal

`scripts/cron_marketing_triggers.py` — corre **cada 6h** (00:00, 06:00, 12:00, 18:00 ART).

Pseudocódigo:

```python
async def run_triggers():
    brand_id = "smart-foods"
    proposals = []

    # Cada trigger retorna lista de TriggerProposal o []
    proposals += await trigger_reactivation_45d(brand_id)
    proposals += await trigger_reactivation_90d(brand_id)
    proposals += await trigger_b2b_reorder_30d(brand_id)
    proposals += await trigger_stock_alert(brand_id)
    proposals += await trigger_cart_abandoned(brand_id)
    proposals += await trigger_anniversary(brand_id)
    proposals += await trigger_vip_top50(brand_id)

    for p in proposals:
        if should_skip(p):  # anti-fatigue, segment <50, campaña reciente
            continue
        await decision_layer.handle(p)
```

## Triggers iniciales — v1 (lanzar con estos 5)

### 1. `trigger_reactivation_45d`

**Detecta**: clientes D2C que compraron hace 45-50 días y no recompraron.

**Query base**:
```sql
SELECT customer_id, customer_email, customer_phone,
       last_product_bought, last_order_total
FROM b2c_customers
WHERE last_order_at BETWEEN datetime('now', '-50 days') AND datetime('now', '-45 days')
  AND recompras = 0  -- solo quienes NO volvieron
  AND customer_email IS NOT NULL
  AND unsubscribed = 0
```

**Hipótesis**: ventana óptima según histórico. Si no hay histórico → A/B entre 30d, 45d, 60d inicialmente.

**Propone**:
- Channel: email (preferido) + WA opt-in
- Descuento: 15% en producto que ya compró (cross-category) O 15% en `all`
- Subject line: "Tu [producto] se está terminando. -15%"
- Expires: 14 días

### 2. `trigger_reactivation_90d`

Igual a (1) pero para ventana 90-95d. Descuento hasta 20% (requiere aprobación humana por ser >15%).

### 3. `trigger_b2b_reorder_30d`

**Detecta**: clientes B2B (tier hot/warm) cuyo último pedido fue hace 28-35 días.

**Query**:
```sql
SELECT business_id, contact_name, contact_phone, contact_email,
       last_order_at, avg_order_value, top_product
FROM crm_b2b_customers
WHERE tier IN ('hot', 'warm')
  AND last_order_at BETWEEN datetime('now', '-35 days') AND datetime('now', '-28 days')
  AND status = 'active'
```

**Canal**: WhatsApp (B2B responde más por WA que email)

**Copy**: mensaje personalizado con nombre del comercio + producto más vendido del cliente.

**Cupón**: opcional, B2B tiene precio mayorista fijo. Si se incluye → `B2BREORD-[FECHA]-EXPRESS` (envío express gratis en lugar de descuento en producto).

### 4. `trigger_stock_alert`

**Detecta**: SKUs con stock alto + rotación lenta (riesgo de vencimiento o capital inmovilizado).

**Query** (usa `products` + `stock_movements`):
```sql
SELECT sku, name, current_stock, avg_daily_sales_last_30d,
       (current_stock / NULLIF(avg_daily_sales_last_30d, 0)) as days_of_stock
FROM products
WHERE brand_id = 'smart-foods'
  AND current_stock > 0
  AND (current_stock / NULLIF(avg_daily_sales_last_30d, 0)) > 60
```

**Propone**: descuento 15-25% solo en ese SKU, a toda la base opt-in.

**Hipótesis**: "liquidar stock sin canibalizar ventas de SKUs rotando bien".

**Guardrail**: si `days_of_stock > 180` y producto vence en <90d → flaguear para Andrés, no autónomo.

### 5. `trigger_cart_abandoned`

**Detecta**: carritos Shopify abandonados hace 24-48h sin conversión.

**Fuente**: Shopify `checkouts` endpoint (abandoned_at IS NOT NULL).

**Canal**: email (Klaviyo ya tiene flow, pero sobreescribimos con atribución directa) + WA si hay phone.

**Copy**: "Te quedó esto en el carrito. -10% si completás en 48h" (descuento bajo porque intención ya alta).

**Cupón**: `CARTABN-[FECHA]-USERID10` (uso único por customer).

## Triggers v2 — después del día 10

- `trigger_anniversary` — 1 año desde primera compra → cupón celebración
- `trigger_vip_top50` — VIP que no compra hace 30d → cupón premium 20% (requiere aprobación)
- `trigger_review_request` — cliente que compró hace 14d → pide review (sin cupón, flow informativo)
- `trigger_competitor_price_war` — si competidor baja precio → campaña "nuestro precio vale porque..."
- `trigger_low_engagement_save` — cliente que no abre email en 90d → campaña "seguís con nosotros?" + cupón

## Anti-fatigue rules

Antes de enviar a un customer:

```python
def should_skip_customer(customer_id, proposed_campaign):
    # regla 1: no recibió campaña en últimos 14 días
    recent = db.query("""
        SELECT COUNT(*) FROM campaign_events
        WHERE customer_id = ? AND event_type = 'sent'
        AND occurred_at > datetime('now', '-14 days')
    """, customer_id)
    if recent > 0:
        return True, "received_campaign_in_14d"

    # regla 2: no más de 3 campañas en 30 días
    month = db.query("""
        SELECT COUNT(*) FROM campaign_events
        WHERE customer_id = ? AND event_type = 'sent'
        AND occurred_at > datetime('now', '-30 days')
    """, customer_id)
    if month >= 3:
        return True, "fatigue_3_per_month"

    # regla 3: marcó unsubscribe
    if customer.unsubscribed:
        return True, "unsubscribed"

    # regla 4: es cliente B2B y campaña es D2C (o viceversa)
    if customer.type != proposed_campaign.target_type:
        return True, "type_mismatch"

    return False, None
```

## Anti-segment-overlap

Si dos triggers producen propuestas para overlapping segments en la misma corrida:

1. **Prioridad por margen esperado** — el trigger que prometa mejor margen gana el cliente.
2. **Mutex por customer** — un customer solo recibe una de las dos campañas ese día.

Orden de prioridad (alto → bajo):
1. `cart_abandoned` (intención más caliente)
2. `b2b_reorder_30d` (ticket promedio alto)
3. `vip_top50`
4. `reactivation_45d`
5. `reactivation_90d`
6. `stock_alert`
7. `anniversary`

## TriggerProposal (dataclass)

```python
@dataclass
class TriggerProposal:
    trigger_type: str
    brand_id: str
    channel: Literal["email", "whatsapp"]
    segment_name: str
    segment_customers: list[CustomerRef]  # max 5000 en un batch
    hypothesis: str
    suggested_discount_value: float
    suggested_discount_type: str  # 'percentage' | 'fixed_amount'
    suggested_scope: str  # 'all' | 'collection:X' | 'product:Y'
    expected_revenue: float
    expected_margin: float
    confidence: float  # 0-1, basado en performance histórica de triggers similares
    requires_approval: bool  # True si discount >15% o segment nuevo
    priority: int  # 1-10
```

## Logs y observabilidad

Cada corrida del cron loguea:

```python
log.info("trigger_run", extra={
    "triggers_executed": ["reactivation_45d", "b2b_reorder_30d", ...],
    "proposals_generated": 7,
    "proposals_skipped_fatigue": 3,
    "proposals_sent_to_decision_layer": 4,
    "duration_ms": 1234,
})
```

Tabla `trigger_runs`:
```sql
CREATE TABLE trigger_runs (
    id INTEGER PRIMARY KEY,
    run_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    triggers_executed_json TEXT,
    proposals_generated INTEGER,
    proposals_filtered INTEGER,
    duration_ms INTEGER
);
```

## Tests

1. Correr trigger_reactivation_45d en staging con DB de prueba → verifica que propuestas tengan segment válido.
2. Trigger overlap: simular 2 triggers apuntando a mismo customer → solo uno gana.
3. Anti-fatigue: customer recibió campaña hace 7d → debe skiparse.
4. Trigger stock_alert con SKU vencible → flag `requires_approval=True`, no autónomo.
