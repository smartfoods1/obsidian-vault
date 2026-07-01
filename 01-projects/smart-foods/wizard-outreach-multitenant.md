---
date: 2026-05-30
type: design-spec
tags: [smartbrain, outreach, whatsapp, baileys, multi-tenant, content-hub, wizard]
status: diseñado-pendiente-build
---

# Wizard de Outreach WhatsApp multi-tenant (SmartBrain)

> **Objetivo:** que cualquier tenant (SF primero, KR después, y futuros clientes del Content Hub) pueda, desde un wizard en SmartBrain: conseguir un SIM nuevo → vincularlo al VPS → configurar el outreach frío (cantidad/día, mensajes, follow-ups) → activar. Todo self-service, sin que yo toque el servidor a mano.
>
> **Decisión de build (30 may 2026):** alcance COMPLETO (vínculo + límites + mensajes + follow-ups). Build DIFERIDO — primero Andrés hace otras cosas. Este doc es el spec para retomar.

## Estado actual (ya hecho — 30 may 2026)

- Motor **Baileys single-session** funcionando para SF. Servicio `wa-baileys.service` (systemd, enabled) en `/root/.openclaw/workspace/wa-baileys/server.js`, escucha `127.0.0.1:8787`.
- Chip SF `5491165857832` vinculado, anclado en un **ZTE Blade A35** (dispositivo primario; VPS = dispositivo vinculado). Sesión `open`, sobrevive restarts.
- Warm-up seteado: `WA_MAX_DAY=10`, `WA_MAX_HOUR=4`, delays 60-120s.
- API actual (single-session): `/status`, `/pair`, `/send`, `/send-bulk`, `/bulk-status`, `/qr`, `/refresh-qr`.
- Proxy autenticado existente: `dashboard/packages/smartbot/backend/routers/wa_web.py` (prefix `/api/wa-web`) → pega a `127.0.0.1:8787`.
- Pipeline outreach existente: `skills/outreach_engine/` (`outreach_main.py`, `outreach_dispatcher.py`, `message_builder.py`, `outreach_config.py`, `outreach_tracker.py`). Genera mensajes (Gemini) → manda tarjetas de aprobación a Andrés por WABA → Andrés aprueba "ok N".
- ⚠️ **Pendiente sin verificar:** el handler "ok N" → `/send` (la pieza que dispara el envío real al prospecto tras la aprobación). Se cierra en Fase 4.

Ver memoria: `project_wa_baileys_outreach.md`.

## Insight de arquitectura

El motor pasa de **single-session** a **multi-sesión keyed by `brand_id`, uno por VPS**.
- VPS SF (`76.13.228.77`): smart-foods (+ specialandres opcional).
- VPS KR (`103.199.187.246`): korean-root.
- "Enviar a KR" = deployar el mismo código allá y correr el wizard con el chip nuevo de KR.

La config vive en la **DB del tenant** (un `.db` por tenant, brand_id implícito vía `_resolve_db_path()`), NO en `outreach_config.py`. Esto mata el hardcoding (regla no-hardcode) y permite que cada cliente tenga sus propios números/límites/mensajes.

## Capa 1 — Motor Baileys multi-sesión (Node)

Refactor de `server.js` a un **manager de N sesiones**:
- Sesiones en un `Map` keyed by `brand_id`. Auth aislada: `auth_info/{brand_id}/`. Contadores y `config.json` por sesión.
- **Migración sin romper SF:** al arrancar, si existe `auth_info/creds.json` (flat) y no existe `auth_info/smart-foods/`, mover los archivos flat a `auth_info/smart-foods/`. One-shot, preserva la sesión viva (no se re-vincula).
- API nueva (todas aceptan `brand_id`; si falta → default `smart-foods` por compat):
  - `GET /sessions` → lista `[{brand_id, status, sent_today, sent_hour}]`
  - `GET /status?brand_id=X`
  - `POST /pair {brand_id, phone}` → `{code}`
  - `POST /unlink {brand_id}` → logout + borra `auth_info/{brand_id}/`
  - `POST /send {brand_id, phone, message}`
  - `POST /send-bulk {brand_id, contacts, delay_seconds}`
  - `POST /config {brand_id, max_per_day, max_per_hour, delay_min, delay_max}` → persiste config por sesión (enforced en `sendOne`)
- Mantener `127.0.0.1` (localhost-only). Caps enforced en el motor; ventana horaria/días enforced en el dispatcher (controla el timing).
- **No reiniciar una sesión durante la ventana post-pairing** (causa 401 — aprendido a la mala). Solo leer status hasta `open`.

## Capa 2 — Backend (FastAPI, brand-scoped)

**Tabla nueva `outreach_settings`** (en cada `.db` de tenant; `brand_id` explícito para que el motor lo reciba):

```sql
CREATE TABLE IF NOT EXISTS outreach_settings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  brand_id TEXT NOT NULL DEFAULT '',
  chip_number TEXT NOT NULL,                 -- 549...
  label TEXT,                                -- "Chip frío B2B"
  status TEXT NOT NULL DEFAULT 'unlinked',   -- unlinked | linked | active | paused
  max_per_day INTEGER NOT NULL DEFAULT 10,
  max_per_hour INTEGER NOT NULL DEFAULT 4,
  delay_min_sec INTEGER NOT NULL DEFAULT 60,
  delay_max_sec INTEGER NOT NULL DEFAULT 120,
  active_hours_start INTEGER DEFAULT 9,
  active_hours_end INTEGER DEFAULT 20,
  active_days TEXT DEFAULT 'mon,tue,wed,thu,fri',
  opt_out_keyword TEXT DEFAULT 'BAJA',
  follow_up_days INTEGER DEFAULT 7,
  max_follow_ups INTEGER DEFAULT 2,
  created_at TEXT, updated_at TEXT
);
```

Los **mensajes** reutilizan la tabla `outreach_templates` que YA existe (variantes hot/warm/influencer/followup, variables `{nombre}`/`{hook}`). El wizard la edita por tenant — no se reinventa.

**Router autenticado** (extender `wa_web.py` o nuevo `routers/outreach_setup.py`), resuelve brand por JWT/override, proxea al motor pasando `brand_id`:
- `GET  /api/wa-web/session` → status del brand actual
- `POST /api/wa-web/session/pair {phone}` → guarda `chip_number`, proxy `/pair`, devuelve `{code}`
- `POST /api/wa-web/session/unlink`
- `GET  /api/wa-web/outreach-config` → lee `outreach_settings`
- `PUT  /api/wa-web/outreach-config {...}` → upsert `outreach_settings` + `POST` motor `/config`
- `GET/PUT /api/wa-web/outreach-templates` → CRUD `outreach_templates`
- Registrar en `dashboard/backend/main.py` (`app.include_router(...)`). Gate por rol ceo/ops.

## Capa 3 — Frontend (wizard React)

- **Componente:** `components/crm/OutreachSetupWizard.tsx` (clon del patrón de `UnifiedSequenceWizard.tsx`).
- **Ruta:** en `App.tsx`, `gated('smartbot', <OutreachSetupWizard/>, { roles: ['ceo','ops'], feature: 'b2b_outreach' })`. Sugerido `/smartbot/outreach-setup` (al lado del `/smartbot/outreach` existente).
- **Pasos:**
  1. **Número / SIM**: input del número del chip + label. Guarda `chip_number`.
  2. **Vincular**: botón "Generar código" → `POST pair` → muestra código de 8 dígitos + instrucciones (WhatsApp → Dispositivos vinculados → Vincular un dispositivo → **Vincular con número de teléfono**) → poll `GET /session` cada ~3s hasta `status=linked` → check verde. Manejar expiry (botón "Generar otro").
  3. **Configurar outreach**: form — msgs/día, msgs/hora, delays min/max, ventana horaria (start/end + días activos), opt-out keyword, follow-ups (días + máximo). + editor de templates (hot/warm/follow-up) con chips de variables.
  4. **Revisar + Activar**: resumen → `PUT outreach-config` con `status=active`.

## Capa 4 — Cablear sender/dispatcher a la DB

- `outreach_engine` lee límites/templates/follow-ups desde `outreach_settings` + `outreach_templates` de la DB del tenant (reemplaza constantes de `outreach_config.py`).
- **Cerrar el handler "ok N" → `/send`** (pendiente): cuando Andrés aprueba una tarjeta, el handler (en `journey_proxy.py` o el bot) debe llamar `/api/wa-web/send` con el `brand_id` correcto. Verificar/arreglar acá.
- Enforcement de ventana horaria/días en el dispatcher.

## Plan por fases

| Fase | Entregable | Aceptación |
|---|---|---|
| 1 | Motor multi-sesión | SF sigue `open` sin re-vincular; `/status?brand_id=smart-foods` OK; `/pair` con brand nuevo da código |
| 2 | Tabla + router backend | `PUT /outreach-config` persiste y pushea al motor; `GET /session` devuelve estado del brand |
| 3 | Wizard frontend | Flujo 4 pasos funcional en SF: vincular un chip de prueba + configurar + activar |
| 4 | Cableado DB + handler "ok N" | Aprobar "ok N" manda al prospecto leyendo límites de la DB; canary 1-2 prospectos reales |
| 5 | Ship a KR | Deploy en `103.199.187.246`; Victoria/Andrés corre el wizard con chip KR; canary KR |

## Ship a KR (Fase 5)

1. `scp`/git del motor + router + frontend al VPS KR.
2. `npm install` en el dir del motor, systemd unit `wa-baileys.service` en KR (mismo patrón).
3. Migrar tabla `outreach_settings` en la DB de korean-root.
4. Correr el wizard logueado como korean-root → chip nuevo de KR → configurar → activar.
5. Canary a 1-2 números antes de soltar batch.

## Riesgos / cosas a no olvidar

- **Baneo en frío es real.** WhatsApp no oficial + outreach frío = riesgo. Por eso chip quemable dedicado, aislado de la WABA. Warm-up obligatorio (arrancar ~10/día y subir). Monitorear baneo.
- **El handler "ok N" no está verificado** — es la pieza que hace que la aprobación realmente envíe. Cerrar en Fase 4 antes de cantar victoria.
- **KR comparte canal B2B con SF** (dietéticas/naturistas AR) — son competidores de canal. Cuidado si ambos hacen outreach al mismo padrón. Ver `project_kr_smartfoods_channel_overlap`.
- **specialandres** podría tener su propio chip como segunda sesión en el VPS SF (el motor multi-sesión ya lo soporta) — opcional.
- Encaja en la narrativa del **Content Hub SaaS** (tier Enterprise = + WhatsApp Bot). Este wizard es parte de ese producto. Ver `project_content_hub_status`.

## Archivos clave (referencia para el build)

- Motor: `/root/.openclaw/workspace/wa-baileys/server.js` + `wa-baileys.service`
- Proxy backend: `dashboard/packages/smartbot/backend/routers/wa_web.py`
- Registro routers: `dashboard/backend/main.py`
- DB / tablas: `dashboard/backend/db.py` (`_resolve_db_path`, `outreach_templates` ya existe)
- Pipeline: `skills/outreach_engine/*`
- Molde wizard: `dashboard/frontend/src/components/crm/UnifiedSequenceWizard.tsx`
- Ruteo: `dashboard/frontend/src/App.tsx` (helper `gated()`)
