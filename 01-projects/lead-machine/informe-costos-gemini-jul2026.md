---
date: 2026-08-01
type: informe
tags: [gondola, smartbrain, gemini, costos]
status: ejecutado
---

# Informe — Gasto Gemini API julio 2026 y plan de ahorro ejecutado

## Factura real (Cloud Billing, cuenta 0176A6-3E29C7-80117A)

**Julio: $217.36** (tope enforced $250 — quedó a $33). Gemini API $200.48 + Places $16.88.

| SKU | Uso | Costo |
|---|---|---|
| Output tokens gemini-2.5-flash | 40M tokens | $100.13 |
| Search grounding (paid queries) | 2.219 queries | $77.67 |
| Input tokens gemini-2.5-flash | 71.3M tokens | $21.40 |
| Places Text Search Enterprise+Atmosphere | 1.422 calls | $16.88 |

Todo el tráfico salía por UNA key ("Openclaw") compartida entre Góndola, SmartBrain SF,
gondola-gen, smartwap, wa-chat, telegram-bot y la Mac → atribución imposible en Google.

## Causa raíz encontrada

`gemini_grounded_json_async` (lead-machine/app.py) — la llamada con Google Search grounding
que hace el worker/enrich de Góndola (2 por enrich: contacto + surtido) — **no seteaba
`thinkingConfig`** → thinking ON default en gemini-2.5-flash:

1. Miles de thinking tokens por llamada **facturados como output** ($2.50/M) → el grueso de los $100.
2. El thinking consumía `maxOutputTokens` y **truncaba el JSON** → el caller reintentaba → **otro fee de grounding $0.036**. El bug multiplicaba ambos SKUs.
3. El `cost_ledger` registraba SOLO el fee plano ($0.036/llamada) → el panel de costos de Góndola era ciego a los tokens (~$100/mes invisibles).

KR no participa: $2/mes vía OpenRouter. El bot SF: 251 mensajes/julio, despreciable.

## Ejecutado (1/8/2026)

1. **lead-machine (deploy con tests+smoke OK, commit 0254429)**:
   - `thinkingBudget: 0` en la llamada grounded.
   - `gemini_grounded_json_async` devuelve `(json, usd_tokens)` desde `usageMetadata`; `_gather_enrich_signals` y el enrich manual registran **fees + tokens reales** en `cost_ledger`.
   - Verificado en vivo: JSON válido, $0.000149/llamada de tokens (antes ~$0.04 de thinking).
2. **`LM_WORKER_BUDGET` 1.5 → 0.5** ($/día) — pool 99% enriquecido; backup `.env.bak.gemini-cost.20260801`.
3. **thinking OFF** también en: gondola-gen (`gondola_lib.py`, + key por header — se filtraba completa en tracebacks del log, pasó el 31/7), smartwap (`content.py`, `content_tier1.py`, `cron_weekly_content.py`, `autodiscover.py`), SF `ig_comments.py`. Backups `*.bak.thinking.20260801`. Servicios `smartwap-api` y `smartbrain-api` reiniciados y sanos.

**Run-rate esperado: ~$75-90/mes** (vs $217). Palancas: output tokens ~$100→~$5, menos
reintentos de grounding, worker a un tercio.

## Señal de alarma vista

`gondola-gen` tiró **403 el 31/7** y volvió solo el 1/8 → patrón de enforcement del tope
pegando a fin de mes. Si un mes se acerca a $250, Meta el bot/contenido mueren los últimos días.
Con el nuevo run-rate no debería repetirse.

## Pendientes

- **Split de keys por servicio**: BLOQUEADO — la org (smartfoods.ar) exige keys nuevas vinculadas a service account (flow nuevo de Google). Alternativa: SA + rol `Generative Language API User`, o política de org. Mientras tanto la atribución la da el `cost_ledger` de Góndola (ahora completo).
- **"Clave de API 2"** (la de Places, AIzaSyB9…) sigue **sin restricciones** (warning rojo de Google). Restringirla a Places API tras confirmar qué la usa.
- `bot_processor.py` usa **gemini-2.5-pro** para respuestas del bot (caro/llamada, volumen bajo) — evaluar bajar a flash.
- `chatbot_engine.py` (tool-loop del bot SF) sigue thinking ON a propósito (volumen ínfimo, no arriesgar calidad).
- `api_usage` de SF muerto desde 10/5 (tracker sin cablear) — opcional reactivar.
- Vigilar `cost_ledger` de Góndola esta semana: ahora registra el costo REAL (fees+tokens) → si el diario supera ~$2.5, revisar.
