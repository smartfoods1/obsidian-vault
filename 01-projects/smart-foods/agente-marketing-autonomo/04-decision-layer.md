---
date: 2026-04-24
type: spec
tags: [smart-foods, marketing, agent, gemini, guardrails]
status: draft
---

# Decision Layer

> Parte de [[index|Agente Marketing Autónomo]]

## Responsabilidad

Recibe `TriggerProposal` → decide si ejecutar, genera copy, corre A/B test del 5%, escala o pausa, registra todo.

**Esta es la única capa que toma decisiones autónomas con impacto en plata.** Por eso los guardrails son estrictos.

## Flujo de decisión

```
TriggerProposal entra
    │
    ▼
[1. Pre-checks]
    │  ├── segment_size >= 50 ?            ─no─> descartar, log
    │  ├── discount <= 15% (si autónomo) ? ─no─> pedir aprobación WA
    │  ├── segmento "nuevo" ?              ─sí─> pedir aprobación WA
    │  ├── copy contiene términos regulados?─sí─> pedir aprobación WA
    │  └── kill_switch activo ?            ─sí─> abortar
    │
    ▼
[2. Shopify discount]
    │  create_discount() → si falla → alerta + abort
    │
    ▼
[3. Generar copy]
    │  Gemini con brand/prompt-context
    │  3 variantes, scoring interno
    │
    ▼
[4. Test 5%]
    │  enviar a muestra aleatoria 5% del segmento
    │  esperar: 6h email | 2h WA
    │
    ▼
[5. Umbral check]
    │  OR >= 15% & CTR >= 1.5% ?
    │  ├── sí → escalar al 95% restante
    │  └── no → pausar + disable Shopify discount + log
    │
    ▼
[6. Monitoreo 72h]
    │  ROAS >= 2× ?
    │  ├── sí → mantener activa hasta expires_at
    │  └── no → pausar + log
    │
    ▼
[7. Close]
    │  cuando discount expires_at se cumple → status='completed'
    │  reporte final en briefing siguiente
```

## Pre-checks detallados

```python
def pre_check(proposal: TriggerProposal) -> CheckResult:
    # 1. Segment size
    if proposal.segment_size < 50:
        return CheckResult(skip=True, reason="segment_too_small")

    # 2. Kill switch
    if get_flag("marketing_agent_kill_switch"):
        return CheckResult(skip=True, reason="kill_switch_active")

    # 3. Descuento requiere aprobación?
    if proposal.suggested_discount_value > 15:
        return CheckResult(
            require_approval=True,
            approval_reason=f"discount_{proposal.suggested_discount_value}_over_15"
        )

    # 4. Segmento nuevo (primera vez que se envía a este segment_name)
    prior = db.query(
        "SELECT COUNT(*) FROM campaign_attribution WHERE segment_name = ?",
        proposal.segment_name
    )
    if prior == 0:
        return CheckResult(require_approval=True, approval_reason="new_segment")

    # 5. WA masivo >200
    if proposal.channel == "whatsapp" and proposal.segment_size > 200:
        return CheckResult(require_approval=True, approval_reason="wa_mass_over_200")

    # 6. Términos regulados en copy (se chequea post-generación)
    # ver generate_copy()

    return CheckResult(proceed=True)
```

## Términos regulados (bloquean envío autónomo)

```python
REGULATED_TERMS = [
    # salud/claims
    "cura", "curar", "curación", "previene", "diagnostica", "trata",
    "enfermedad", "diabetes", "cáncer", "depresión", "ansiedad clínica",
    "Alzheimer", "Parkinson", "COVID",
    # ANMAT
    "medicamento", "suplemento dietario" (si no aparece disclaimer),
    # regulatorio
    "garantiza", "garantizado",
]
```

Si el copy generado por Gemini contiene alguno → `require_approval=True, approval_reason="regulated_term"`.

## Copy generator (Gemini 2.5 Flash)

```python
async def generate_copy(proposal, discount_code, brand_context):
    system = f"""Sos copywriter de Smart Foods Argentina, marca premium de
extractos de hongos adaptógenos. Tono: {brand_context.voice}.
Idioma: español argentino voseo. No usar emojis.
PROHIBIDO: palabras regulatorias (curar, diagnosticar, prevenir, tratar enfermedad).
PROHIBIDO: mencionar cápsulas (el producto es POLVO).
"""

    user = f"""Generá copy para campaña {proposal.channel}.

Contexto:
- Trigger: {proposal.trigger_type}
- Hipótesis: {proposal.hypothesis}
- Segmento: {proposal.segment_name} ({proposal.segment_size} personas)
- Descuento: {proposal.suggested_discount_value}% en {proposal.suggested_scope}
- Código: {discount_code}
- Expira: {proposal.expires_days} días

Formato email:
- subject_line (max 60 chars, sin clickbait burdo)
- preheader (max 80 chars)
- body (HTML simple, 3-4 párrafos, CTA clara)

Formato WhatsApp:
- message (max 400 chars, 1 emoji permitido solo si natural)

Generá 3 variantes. Scoring por: claridad, ajuste a tono, CTA fuerza.
Responder JSON estricto.
"""

    response = await gemini.generate(
        model="gemini-2.5-flash",
        system=system,
        prompt=user,
        response_mime_type="application/json",
        temperature=0.7,
        max_output_tokens=2000,
    )

    variants = json.loads(response)
    # validar contra REGULATED_TERMS
    for v in variants:
        if has_regulated_terms(v):
            return None, "regulated_term_in_generated_copy"

    # elegir variante top-scored
    return variants[0], None
```

## A/B test del 5%

```python
async def test_and_scale(campaign_id, segment, copy):
    test_size = max(20, int(len(segment) * 0.05))  # piso 20 personas
    test_group = random.sample(segment, test_size)
    hold_group = [c for c in segment if c not in test_group]

    await send_to_batch(campaign_id, test_group, copy)
    await update_campaign_status(campaign_id, "testing", sent_at_test=now())

    # Esperar ventana de medición
    wait_seconds = 6 * 3600 if channel == "email" else 2 * 3600
    await asyncio.sleep(wait_seconds)

    # Reconciliar métricas del test
    await reconcile_metrics(campaign_id)
    metrics = await get_campaign_metrics(campaign_id)

    # Umbral
    open_rate = metrics.opened_count / max(metrics.delivered_count, 1)
    click_rate = metrics.clicked_count / max(metrics.delivered_count, 1)

    passes = open_rate >= 0.15 and click_rate >= 0.015

    if not passes:
        await pause_campaign(
            campaign_id,
            reason=f"test_failed_or_{open_rate:.1%}_ctr_{click_rate:.1%}"
        )
        await shopify_discount.disable(campaign.price_rule_id)
        return {"escalated": False, "reason": "test_thresholds_not_met"}

    # Escalar
    await send_to_batch(campaign_id, hold_group, copy)
    await update_campaign_status(campaign_id, "active", sent_at_full=now())
    return {"escalated": True, "full_audience_size": len(segment)}
```

## Monitoreo 72h post-escalado

Cron `cron_marketing_monitor.py` cada 2h:

```python
async def monitor_active_campaigns():
    active = db.query("""
        SELECT * FROM campaign_attribution
        WHERE status = 'active'
        AND sent_at_full > datetime('now', '-72 hours')
    """)

    for c in active:
        if (now() - c.sent_at_full).hours < 24:
            continue  # esperar al menos 24h para juzgar ROAS

        roas = c.revenue_net / max(c.discount_cost + WA_SEND_COST * c.sent_count, 1)

        if roas < 2.0 and (now() - c.sent_at_full).hours >= 48:
            await pause_campaign(c.campaign_id, reason=f"low_roas_{roas:.1f}")
            await shopify_discount.disable(c.shopify_price_rule_id)
```

## Aprobación vía WA

Cuando `require_approval=True`, el agente **no ejecuta** — en su lugar:

```
WA a Andrés (5491165973204):

Propuesta de campaña pide tu OK.

ID: REACT90-2604-GLOW20
Canal: email
Segmento: d2c_lapsed_90d (845 personas)
Hipótesis: clientes 90d sin recompra responden a -20% en Inner Glow
Revenue esperado: ~$380k
Margen esperado: ~$190k
Motivo de aprobación: descuento 20% supera techo autónomo 15%

Responde:
- "SÍ REACT90-2604-GLOW20" → lanzo ahora
- "NO REACT90-2604-GLOW20" → descarto
- "MODIFICAR REACT90-2604-GLOW20 [instrucciones]" → edito y reconsulto
```

Handler en `journey_proxy.py`:

```python
def handle_incoming_message(msg):
    text = msg.text.strip().upper()
    if text.startswith("SÍ ") or text.startswith("SI "):
        campaign_id = text.split()[1]
        if from_phone == "5491165973204":  # solo Andrés aprueba
            asyncio.run(execute_campaign(campaign_id))
    elif text.startswith("NO "):
        ...
    elif text == "STOP":
        set_flag("marketing_agent_kill_switch", True)
        reply("Agente pausado. Nada nuevo se envía. Para reactivar: 'START'")
```

## Shadow mode (día 10 en roadmap)

Antes de autonomía real, 7 días en **shadow mode**:

- Agente corre todo el flujo **excepto enviar**
- Cada propuesta que habría ejecutado → WA a Andrés con "habría hecho X, apruebas ex-post? SÍ/NO"
- Andrés responde → aprender del acuerdo/desacuerdo
- Al día 17 (o cuando tasa de aprobación >85%), pasamos a autónomo real

## Guardrails de emergencia

### Circuit breaker

Si en cualquier ventana de 24h:
- >= 3 campañas consecutivas pausadas por umbral → agente entra en "cooldown": no lanza nada nuevo en 24h, alerta a Andrés.
- Revenue atribuido baja >50% vs media móvil 14d → cooldown + alerta.
- Shopify devuelve errores 5xx en >30% de calls → pausa agente, alerta.

### Budget cap

Tabla `agent_budget`:
```sql
CREATE TABLE agent_budget (
    period TEXT,  -- '2026-04'
    discount_cost_spent REAL DEFAULT 0,
    discount_cost_cap REAL,
    wa_sends_count INTEGER DEFAULT 0,
    wa_sends_cap INTEGER
);
```

Por mes: cap de $150k en descuentos, 5000 WA sends. Antes de lanzar, check si excedería.

## Tabla de estados

```
draft → (pre_check pass) → testing → (umbral pass) → active → completed
                                   ↘ (umbral fail) → paused
                                            ↑
                                   active → (roas fail) → paused
```

## Tests críticos

1. Test 5% falla → cupón se desactiva en Shopify (verificar en Admin)
2. Kill switch activo → nueva propuesta se descarta, log claro
3. Aprobación WA SÍ → ejecuta; NO → descarta; MODIFICAR → reconsulta
4. Circuit breaker: 3 campañas failing consecutivas → cooldown activo
5. Copy con término regulado → bloqueado, require_approval=True
6. Segmento <50 → descartado
