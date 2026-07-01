---
date: 2026-06-20
type: handoff
tags: [smartbrain, korean-root, harness, llm-gateway, ingenieria]
status: en-progreso
---

# Harness Engineering SmartBrain KR — Handoff (2026-06-20)

Documento de continuidad para retomar el proyecto en otra sesión de Claude Code.
Memoria persistente asociada: `project_kr_harness.md`.

## Qué es

Convertir **SmartBrain KR** (VPS `root@103.199.187.246`, brand `korean-root`) de llamados LLM dispersos one-shot a un **harness confiable / observable / escalable**. Roadmap en 4 fases. Es además la base del **Content Hub SaaS**: lo que se forja en KR se replica a Smart Foods y a futuros clientes.

**Diagnóstico que originó el proyecto:** los bugs recurrentes de KR son siempre el mismo patrón con tres caras — alucina (no groundea), falla silencioso (token vacío → fallback mudo; WA send que devuelve True pero no entrega), y "falla aleatoria" del chatbot (search_kb keyword frágil). El harness es la cura: andamiaje determinista alrededor de cada llamado LLM.

## Estado — hecho en sesión del 2026-06-20

Todo en branch `korean-root`, **commits LOCALES en el VPS (NO pusheados)**, verificado y reversible.

| Bloque | Commit(s) | Qué |
|---|---|---|
| Fase 0 — versionado | `c01b616` `f5e5196` `6156f9f` `b2b9b03` | Prod tenía 216 archivos sin commitear (−71k líneas = cierre en disco de migración legacy→packages) y módulos vivos untracked (un `git clean` borraba producción). Estabilizado: `.gitignore`, cierre migración, trackeo de módulos/crons, consolidación marketing |
| Fase 1 PR#0 — gateway | `2444b5a` | `backend/llm_client.py` endurecido + `backend/api_tracker.py` extendido |
| Fase 1 Tier A | `dc353f9` | 5 call-sites → gateway: `sales_ai`, `ig_comments`, `bot_learning`, `b2c`, cleanup `salto_ai_feedback` |
| Seguridad | `c7dd3d6` | Borrado `scripts/cron_flexit_sync.py` (era de SF, JWT Flexit hardcodeado, huérfano) |
| Fase 1 Tier B | `4007987` `c424ea8` | `salto_ingestor`, `ig_dm_redirect`, `proposals` → gateway; **se agregó `allm_chat(messages)` multi-turno** |

Backups: `/root/_harness_backups/{fase0_,fase1_gateway_,fase1_tierA_,fase1_tierB_,fase1_proposals_}20260620/`

## Arquitectura del gateway hoy

**`backend/llm_client.py`:**
- `allm_call(prompt, model, system_prompt, max_tokens, temperature, json_mode, timeout, track, return_meta)` — async, 1 turno.
- `allm_chat(messages, model, max_tokens, temperature, json_mode, timeout, track, return_meta)` — async, multi-turno (OpenRouter nativo + conversión Gemini/Anthropic).
- `llm_call(...)` — versión sync.
- Endurecimiento: retry+backoff en ambos paths; fallback cruzado OpenRouter→Gemini/Anthropic con log ERROR (no silent); captura `finish_reason`; retry ante truncamiento (capeado a `mt+8000`); tracking opt-in.
- API pública backward-compatible (params nuevos con defaults; los call-sites previos no se enteran).

**`backend/api_tracker.py`:**
- `track_usage(brand_id, operation, model, input_tokens, output_tokens, provider, finish_reason, latency_ms, success, post_id, db_path)` — interfaz para el gateway, tokens directos, never-raises.
- Columnas nuevas: provider, finish_reason, latency_ms, success. Pricing real Gemini/Haiku (antes asumía Sonnet).
- Tracking se activa pasando `track={brand_id, operation, post_id, db_path}` a `allm_call`/`allm_chat`.

## Pendiente (roadmap)

- **Tier C** — `chatbot_engine._gemini_simple` al gateway (caso trivial sin tools; archivo MÁS sensible, bot en vivo SF+KR).
- **Diferido** — `chatbot_engine._ask_gemini` (function-calling, tools formato Gemini, multi-turno). Camino: extender `allm_chat` con `tools=` y recién ahí migrar. Es un mini-proyecto.
- **Fase 2** — Capa juez (`ContentJudge`) unificada pre-envío contra reglas de marca (términos prohibidos, groundedness real, URLs, params WA tempranos, límites Perfit, cupones) + **evals golden** por tenant anti-regresión. Mayor ROI vs alucinaciones.
- **Fase 3** — Grounding semántico (embeddings sqlite-vec/FAISS, filtro bot_id/brand_id en queries KB) + escala (sacar LLM del request path, rate-limit por tenant).
- Cablear `track=` en los call-sites ya migrados (hoy disponible pero no usado) → costo/tokens por tenant.
- Limpieza residual de "flexit" en `cerebro.py` / `db.py` / `cron_ai_alerts.py` (solo mencionan, sin token).

## Gotchas operativos (clave para no tropezar)

- **Import/test en VPS:** sourcear env o `config.py` aborta → `source <(grep -v "^#" /etc/smartbrain/.env | grep "=" | sed "s/^/export /")`.
- **Arranque:** `smartbrain-api` tarda ~9s. `/` y `/openapi.json` dan **404 SIEMPRE** (docs off) — NO es fallo. Salud real = `"startup complete"` en `journalctl -u smartbrain-api` + `systemctl is-active`.
- **venv:** `/opt/journey-venv/bin/python3`.
- **Imports:** routers de `packages/` usan `from llm_client import ...` (main.py mete `dashboard/` en path; `backend/` queda en path por uvicorn).
- **KR sin `GEMINI_API_KEY`** → todo por OpenRouter (`chain=['openrouter']`).
- **WA send de KR roto** (`Missing WA credentials for bot 'korean-root'`) → no se puede testear el bot en vivo en KR (deuda preexistente, ver `project_kr_wa_token_dead`).
- **Patrón de deploy seguro (usado en toda la sesión):** backup → scp a staging → compile remoto → cp a destino → import test → restart → verificar `startup complete` + sin tracebacks → smoke real → commit o **rollback automático**. KR es cliente pago: nada sin verificar, todo reversible.
- NO escribir en Meta (solo lectura). NO pushear a Tienda Nube sin pedido explícito.

## Prompt para pegar en una nueva ventana

```
Continuá el proyecto "harness engineering" sobre SmartBrain KR (VPS root@103.199.187.246, brand korean-root). PRIMERO leé la memoria project_kr_harness.md completa y este handoff (01-projects/korean-root/harness-llm-gateway-handoff-2026-06-20.md).

Estado: Fase 0 (versionado prod) + Fase 1 PR#0 (gateway llm_client endurecido + api_tracker) + Tier A (5 call-sites) + Tier B (3 call-sites, incluye allm_chat multi-turno) HECHOS, desplegados y verificados en branch korean-root (commits LOCALES en el VPS, NO pusheados). Backups en /root/_harness_backups/*_20260620/.

El gateway backend/llm_client.py ya expone allm_call (1 turno) y allm_chat (multi-turno) con retry/fallback/finish_reason/timeout/tracking opt-in (track=). api_tracker.track_usage() registra tokens/costo/latencia/provider/finish/success.

Reglas operativas DURAS:
- SSH cortos con timeout. venv: /opt/journey-venv/bin/python3.
- Para correr python en el VPS sourceá el env o config.py aborta: source <(grep -v "^#" /etc/smartbrain/.env | grep "=" | sed "s/^/export /")
- smartbrain-api tarda ~9s en arrancar; / y /openapi.json dan 404 SIEMPRE (no es fallo). Salud = "startup complete" en journalctl + service active.
- KR usa solo OpenRouter (sin GEMINI_API_KEY). WA send de KR roto → no testear el bot en vivo.
- Deploy SIEMPRE con: backup → staging → compile remoto → import test → restart → verificar startup+sin tracebacks → smoke → commit o rollback. KR es cliente pago: nada sin verificar, todo reversible.
- Routers de packages importan `from llm_client import ...`. NO escribir en Meta (solo lectura). NO pushear a Tienda Nube sin pedido explícito.

Próximo paso que quiero hacer: <ELEGÍ UNO>
  (a) Fase 2 — capa juez (ContentJudge) + evals anti-regresión: verificación unificada pre-envío contra reglas de marca (términos prohibidos, groundedness, URLs, params WA, límites Perfit, cupones) + set de casos golden por tenant. Es el mayor ROI vs alucinaciones.
  (b) Tier C — migrar chatbot_engine._gemini_simple al gateway (cuidado: archivo más sensible, bot SF+KR).
  (c) Extender allm_chat con tools= para después migrar chatbot_engine._ask_gemini (function-calling).
  (d) Cablear tracking track= en los call-sites ya migrados para ver costo/tokens por tenant.

Arrancá auditando el estado real contra la memoria antes de tocar nada, y proponeme el plan antes de ejecutar.
```
