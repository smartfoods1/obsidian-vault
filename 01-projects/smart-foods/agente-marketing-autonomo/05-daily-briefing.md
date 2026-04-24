---
date: 2026-04-24
type: spec
tags: [smart-foods, marketing, reporting, whatsapp, gemini]
status: draft
---

# Daily WA Briefing

> Parte de [[index|Agente Marketing Autónomo]]

## Responsabilidad

Cada mañana a las 8:30 ART, enviar **un único mensaje de WhatsApp** a Andrés (`+5491165973204`) con:

1. Performance de campañas activas y recién cerradas
2. Revenue atribuido del día anterior + mes a la fecha
3. Acciones que requieren aprobación explícita

**Regla**: un solo mensaje. Si hay mucha data, el agente prioriza y resume, no fragmenta.

## Cron

`scripts/cron_marketing_daily_briefing.py` — **8:30 ART daily** (`30 11 * * *` en UTC, ajustar por DST).

## Data sources

1. `campaign_attribution` — campañas activas + últimos 30d
2. `campaign_events` — eventos de ayer
3. `agent_budget` — gasto mes a la fecha
4. `agent_pending_approvals` — propuestas esperando SÍ/NO

## Prompt Gemini para síntesis

```python
SYSTEM_PROMPT = """Sos el asistente de marketing de Andrés, CEO de Smart Foods.
Cada mañana resumís en UN SOLO mensaje de WhatsApp el desempeño de campañas de
email y WA del día anterior + estado del mes.

Tono: directo, sin saludos efusivos, sin emojis salvo que sean estrictamente
necesarios. Español argentino voseo. Máximo 1500 caracteres.

Estructura:
1. Header: 'Marketing — [fecha]'
2. Sección Email con 1 línea por campaña (máx 4 campañas, resumí el resto)
3. Sección WhatsApp con 1 línea por campaña (máx 3)
4. Resumen del día: revenue atribuido, costo cupones, margen neto
5. Mes a la fecha: revenue acumulado, ROAS blended email, ROAS blended WA
6. Acciones que piden OK: numeradas, con formato 'N-SÍ / N-NO' para responder

Para cada campaña reportá:
- nombre corto
- envíos, OR%, CTR%, pedidos, revenue, ROAS
- veredicto: 'gano' (ROAS>4×), 'ok' (2-4×), 'flojo' (1-2×), 'perdió' (<1×)
- acción tomada por el agente o propuesta

NO inventes números. Usá exactamente los datos que te paso."""

USER_PROMPT = f"""Data del día {fecha}:

Campañas email ayer:
{campaigns_email_json}

Campañas WA ayer:
{campaigns_wa_json}

Métricas agregadas día anterior:
{daily_totals_json}

Mes a la fecha:
{mtd_totals_json}

Aprobaciones pendientes:
{pending_approvals_json}

Gastos del mes contra cap:
- Descuentos: ${spent} / ${cap} ARS
- WA sends: {wa_sent} / {wa_cap}

Generá el mensaje WA siguiendo el formato del system prompt."""
```

## Formato del mensaje (ejemplo real)

```
Marketing — 24 abr

Email (Klaviyo)
• REACT45-2304-BRAIN15 → 1.180 env, OR 28%, CTR 4.1%,
  6 pedidos, $412k rev, ROAS 8.2×. Gano. Escalada toda la base.
• STOCK-IMMUNE-2304-20 → 2.400 env, OR 19%, CTR 1.8%,
  3 pedidos, $156k rev, ROAS 2.1×. Ok. Mantengo.
• REACT90-2204-GLOW20 → 845 env, OR 14%, CTR 1.2%,
  1 pedido, $89k. Flojo. Pausada. Probaré hook nuevo vie.

WhatsApp
• B2BREORD-2304-EXPRESS → 42 env, 38 leídos (90%), 7 respondieron,
  3 pedidos confirmados + 4 en negociación. $1.1M en curso.
• CARTABN-2304-ALL10 → 68 env, 52 leídos, 9 conversiones,
  $340k rev, ROAS 11×. Gano.

Día anterior
Revenue atribuido: $2.01M · Costo cupones: $58k · Margen neto: $890k

Mes a la fecha (abr)
Rev: $18.4M · ROAS email 6.1× · ROAS WA 11.4× · Descuentos: $380k/$500k cap

Acciones que piden tu OK:
1. Lanzar REACT90-2504-GLOW20 a 845 personas (descuento 20% supera techo).
   Revenue esperado ~$380k. Respondé 1-SÍ / 1-NO.

2. Reactivar campaña pausada con nuevo hook copy. Costo cupón repetido $0.
   Respondé 2-SÍ / 2-NO.
```

## Código del cron

```python
# scripts/cron_marketing_daily_briefing.py
import asyncio
import aiohttp
from datetime import date, timedelta
from services.gemini import generate_text
from services.wa import send_message
from db import get_connection

TARGET_PHONE = "5491165973204"


async def build_briefing(brand_id: str = "smart-foods") -> str:
    yesterday = date.today() - timedelta(days=1)
    mtd_start = date.today().replace(day=1)

    with get_connection(brand_id) as db:
        # Campañas activas + completadas ayer
        campaigns_email = db.query("""
            SELECT campaign_id, subject_line, segment_name, segment_size,
                   sent_count, delivered_count, opened_count, clicked_count,
                   orders_count, revenue_net, discount_cost, margin_net,
                   status, agent_decision
            FROM campaign_attribution
            WHERE channel = 'email'
              AND (date(sent_at_full) = ?
                   OR (status = 'active' AND sent_at_full IS NOT NULL))
            ORDER BY revenue_net DESC
            LIMIT 8
        """, yesterday)

        campaigns_wa = db.query("""
            SELECT ... (análogo para WA, incluir replied_count)
        """)

        # Totales día anterior
        daily = db.query("""
            SELECT SUM(revenue_net) AS rev, SUM(discount_cost) AS disc,
                   SUM(margin_net) AS margin
            FROM campaign_events e
            JOIN campaign_attribution c ON e.campaign_id = c.campaign_id
            WHERE date(e.occurred_at) = ? AND e.event_type = 'ordered'
        """, yesterday)

        # Mes a la fecha
        mtd = db.query("""
            SELECT SUM(revenue_net) AS rev,
                   SUM(CASE WHEN channel='email' THEN revenue_net END) AS email_rev,
                   SUM(CASE WHEN channel='email' THEN discount_cost END) AS email_cost,
                   SUM(CASE WHEN channel='whatsapp' THEN revenue_net END) AS wa_rev,
                   SUM(CASE WHEN channel='whatsapp' THEN discount_cost END) AS wa_cost
            FROM campaign_attribution
            WHERE date(created_at) >= ?
        """, mtd_start)

        # Aprobaciones pendientes
        pending = db.query("""
            SELECT campaign_id, approval_reason, segment_name, segment_size,
                   suggested_discount_value, expected_revenue
            FROM campaign_attribution
            WHERE status = 'pending_approval'
            ORDER BY expected_revenue DESC
            LIMIT 3
        """)

        # Budget
        budget = db.query("""
            SELECT discount_cost_spent, discount_cost_cap,
                   wa_sends_count, wa_sends_cap
            FROM agent_budget
            WHERE period = ?
        """, date.today().strftime("%Y-%m"))

    briefing = await generate_text(
        model="gemini-2.5-flash",
        system=SYSTEM_PROMPT,
        user=USER_PROMPT.format(
            fecha=yesterday.strftime("%d %b"),
            campaigns_email_json=json.dumps(campaigns_email, default=str),
            campaigns_wa_json=json.dumps(campaigns_wa, default=str),
            daily_totals_json=json.dumps(daily, default=str),
            mtd_totals_json=json.dumps(mtd, default=str),
            pending_approvals_json=json.dumps(pending, default=str),
            spent=budget.discount_cost_spent,
            cap=budget.discount_cost_cap,
            wa_sent=budget.wa_sends_count,
            wa_cap=budget.wa_sends_cap,
        ),
        temperature=0.3,
        max_output_tokens=2000,
    )

    return briefing


async def main():
    briefing = await build_briefing()

    # Truncar si >1500 chars (WA permite 4096, pero queremos legibilidad)
    if len(briefing) > 1500:
        briefing = briefing[:1450] + "\n\n(Truncado. Ver dashboard.)"

    await send_message(
        to=TARGET_PHONE,
        body=briefing,
        type="text",
    )

    # Log que se envió
    with get_connection("smart-foods") as db:
        db.execute("""
            INSERT INTO daily_briefings (sent_at, phone, body, length)
            VALUES (?, ?, ?, ?)
        """, (datetime.now(), TARGET_PHONE, briefing, len(briefing)))


if __name__ == "__main__":
    asyncio.run(main())
```

## Tabla `daily_briefings`

```sql
CREATE TABLE daily_briefings (
    id INTEGER PRIMARY KEY,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    phone TEXT,
    body TEXT,
    length INTEGER,
    reply_received TEXT,  -- respuesta de Andrés si hubo
    reply_at TIMESTAMP
);
```

## Fallback si Gemini falla

Si `generate_text` devuelve error o JSON malformado:

```python
try:
    briefing = await generate_text(...)
except Exception as e:
    # Fallback: template hardcoded
    briefing = build_fallback_briefing(daily, mtd, pending)
    log.warning(f"gemini_failed_using_fallback: {e}")
```

Fallback template:
```
Marketing — {fecha} (modo simple)

Email: {n} campañas, {rev_email} revenue, ROAS {roas_email}×
WA: {n} campañas, {rev_wa} revenue, ROAS {roas_wa}×

Día: ${rev_total} · Mes: ${mtd_total}

Aprobaciones pendientes: {n}

(Gemini no disponible, reporte abreviado. Ver dashboard.)
```

## Evolución (después de 30 días)

- Agregar comparativa vs semana anterior (delta %)
- Agregar top 3 insights ("Brain outperform vs Immune en segmento mujer 30-40")
- Sumar mini-forecast: "a este ritmo, cerramos mes en $X M"
- Botón "ver dashboard" con deep link a `/campaigns/dashboard`
- Versión viernes: resumen semanal + plan próxima semana

## Tests

1. Correr cron en staging con data mock → verifica WA llega, <1500 chars, formato correcto
2. Gemini error → usa fallback template, loguea, no rompe el cron
3. 0 campañas activas → mensaje sigue saliendo con "Sin campañas ayer. Triggers próxima corrida 12:00."
4. >5 campañas → Gemini resume top 4 y dice "+ N más menores"
