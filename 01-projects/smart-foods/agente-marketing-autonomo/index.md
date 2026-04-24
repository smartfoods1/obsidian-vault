---
date: 2026-04-24
type: project
tags: [smart-foods, marketing, agente-autonomo, smartbrain]
status: in-progress
---

# Agente Marketing Autónomo — Smart Foods

## Objetivo

Cerrar el loop de marketing (email + WhatsApp) para que corra autónomo con:

1. **Atribución real** de revenue por campaña
2. **Triggers automáticos** que detectan oportunidades sin input humano
3. **Cupones Shopify** generados programáticamente antes de cada envío
4. **Decisión de enviar/pausar/escalar** con guardrails de seguridad
5. **Briefing WA diario** con resultados y pedido de OK para acciones mayores

## Función objetivo

Maximizar `margen_contribución_mensual` de campañas email + WA.

Fórmula:
```
margen_neto = revenue_gross - discount_cost - COGS - costo_envío_WA
roas = revenue_net / (discount_cost + costo_operativo)
```

## Scope inicial

- **Canales**: Klaviyo (email) + WA Cloud API
- **Brand**: solo `smart-foods` (no `specialandres`, no `korean-root` todavía)
- **Canal de venta**: Shopify D2C (MeLi queda fuera — cupones programáticos limitados)

## Fuera de scope (explícito)

- Meta/Google Ads → otro proyecto, otro agente
- Contenido IG → ya corre autónomo via `cron_ig_publish.py`
- B2B outreach → ya existe `skills/outreach_engine`
- Cambios de producto, fórmula, pricing fuera del rango ±8%
- Lanzamientos de productos nuevos
- Comunicaciones de crisis / PR

## Arquitectura — diagrama de flujo

```
[Trigger Engine] cron cada 6h
    │
    │ detecta: reactivación 45d | B2B reorden 30d | stock alto | etc.
    ▼
[Decision Layer]
    │
    ├── segment_size < 50? → descarta
    ├── segmento ya recibió campaña en <14d? → descarta (anti-fatigue)
    ├── genera campaign_id
    │
    ▼
[Shopify Discount API]
    │
    ├── crea PriceRule + DiscountCode
    ├── si falla → aborta, alerta por WA
    │
    ▼
[Copy Generator] (Gemini 2.5 Flash)
    │
    ├── lee brand/prompt-context
    ├── genera copy con code incluido
    │
    ▼
[Test 5%]
    │
    ├── envía a 5% del segmento
    ├── espera 6h (email) / 2h (WA)
    │
    ▼
[Umbral check]
    │
    ├── OR >15% & CTR >1.5% → escalar al 95% restante
    ├── por debajo → pausar + desactivar cupón Shopify
    │
    ▼
[Atribution]
    │
    ├── webhook Shopify orders/create
    ├── match discount_code → campaign_id
    ├── actualiza métricas en campaign_attribution
    │
    ▼
[Daily WA Briefing] cron 8:30 ART
    │
    └── síntesis Gemini → 1 mensaje WA a Andrés (+5491165973204)
```

## Roadmap de implementación — 10 días

| Día | Milestone | Spec |
|-----|-----------|------|
| 1–2 | Attribution engine (tablas + webhooks Shopify + backfill 90d) | [[01-attribution-engine]] |
| 3 | Daily WA briefing corriendo con métricas actuales (sin agente aún — vos seguís disparando campañas como hoy, pero ves el reporte unificado) | [[05-daily-briefing]] |
| 4–5 | Shopify discount integration + triggers iniciales | [[02-shopify-discount-api]] + [[03-trigger-engine]] |
| 6–8 | Decision layer con guardrails + test 5% + escalado | [[04-decision-layer]] |
| 9 | Kill switch + approval via WA (responder SÍ/NO/STOP) | [[04-decision-layer]] |
| 10 | Shadow mode: agente decide pero NO ejecuta, manda propuestas por WA para vos aprobar todo. 7 días shadow antes de autonomía real. | [[04-decision-layer]] |

## Guardrails — decididos 2026-04-24

| Guardrail | Valor |
|---|---|
| Umbral pausa email | OR <15% **o** CTR <1.5% en test 5% |
| Umbral pausa ROAS | <2× a 72h |
| Descuento máximo autónomo | 15% |
| Segmento mínimo | 50 personas |
| Segmento máximo autónomo | toda la base si copy en tono validado |
| Anti-fatigue | mismo segmento no recibe 2 campañas <14d |
| Tipo cupón default | compartido + `usage_limit = segment_size` |
| Cupón único por cliente | si segmento >500 **o** descuento >20% |
| Kill switch | "STOP" por WA → pausa todo menos contenido IG aprobado |

## Decisiones que SIEMPRE requieren aprobación explícita vía WA

- Cupones >15%
- Segmentos nuevos (primer envío a un segment recién definido)
- Lanzamientos de producto
- Mensajes WA masivos >200 personas
- Cualquier campaña con palabra "ANMAT", "salud", "cura", "diabetes" (o términos regulados)

## Formato del WA diario — 8:30 ART

```
Marketing — [fecha]

Email (Klaviyo)
• [campaña] → [env], OR [%], CTR [%], [pedidos] pedidos,
  $[X]k rev, ROAS [X]×. [Veredicto]. [Acción tomada/propuesta]

WhatsApp
• [campaña] → [env], [leídos], [respondieron], [pedidos] pedidos,
  $[X]k rev o potencial.

Resumen día
Revenue atribuido: $[X]M · Costo cupones: $[X]k · Margen neto: $[X]k
Mes a la fecha: $[X]M rev · ROAS email [X]× · WA [X]×

Acciones que piden tu OK:
1. [acción propuesta] → responde 1-SÍ / 1-NO
2. [acción propuesta] → responde 2-SÍ / 2-NO
```

## Links a specs detallados

- [[01-attribution-engine|Attribution engine — tablas, webhooks, backfill]]
- [[02-shopify-discount-api|Shopify Discount API — crear cupones programáticos]]
- [[03-trigger-engine|Trigger engine — detección de oportunidades]]
- [[04-decision-layer|Decision layer — A/B test, guardrails, aprobaciones]]
- [[05-daily-briefing|Daily WA briefing — cron 8:30, prompt Gemini]]

## Métricas de éxito del proyecto

Al día 60 post-lanzamiento:

- 10+ campañas ejecutadas autónomas sin intervención
- ROAS blended email+WA ≥ 4×
- 0 campañas enviadas con copy off-brand o regulatoriamente riesgoso
- Briefing WA diario 100% de days (sin fallas técnicas)
- Tiempo de Andrés dedicado a email+WA baja de ~3h/semana a <30min/semana
