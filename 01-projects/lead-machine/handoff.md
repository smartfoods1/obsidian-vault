---
date: 2026-06-21
type: handoff
tags: [lead-machine, mvp, saas, b2b, handoff]
status: activo
---

# Lead Machine — Handoff completo (continuar en ventana nueva)

> SaaS freemium de prospección B2B para marcas de alimentos/suplementos AR. **VIVO y cobrando.**
> Agnóstico de marca (sirve para cualquier marca, no solo Smart Foods).
> Este doc es la **fuente de verdad**. Memoria: `project_lead_machine.md` (v1–v10). Ops: repo `~/lead-machine/HARNESS.md`.

## 0. Cómo arrancar en la ventana nueva (leer esto primero)
1. `cd ~/lead-machine` — Claude Code lee `CLAUDE.md` (=AGENTS.md) automáticamente.
2. Leer `HARNESS.md` (operación) y este handoff (contexto).
3. **Flujo de trabajo obligatorio:** editar → `./run-tests.sh` → `./deploy.sh`. **NUNCA deployar a mano** (corrompió la DB 2 veces). El deploy hace backup+rollback solo.
4. La app es **single-file**: toda la lógica en `app.py` (~1.300 líneas). Frontend en `static/`.

## 1. Qué es (una línea)
La marca carga su URL → la IA detecta productos → elige zona (autocomplete Google) → scrapea Google Maps, **califica** cada comercio (fit score con pesos, posicionamiento premium/granel, marcas que ya vende, actividad, reseñas) → arma icebreaker de WhatsApp + ruta → los leads **quedan en la cuenta del user** (acumulan) → exporta CSV/Excel/JSON/PDF. Freemium: 5 leads gratis, después packs por MercadoPago.

## 2. Accesos / URLs
- **App pública:** https://leadmachine.76.13.228.77.nip.io (HTTPS, sin túnel).
- **Admin:** https://leadmachine.76.13.228.77.nip.io/admin — key `51b7f5915402621f284e` (`LM_ADMIN_KEY`). El panel manda la key por header `X-Admin-Key`.
- **VPS:** `root@76.13.228.77` (mismo que SmartBrain). Servicio systemd `lead-machine.service` → uvicorn `127.0.0.1:8200`. nginx server-block `/etc/nginx/sites-available/lead-machine` (TLS Let's Encrypt auto, `proxy_read_timeout 300s`).
- **Repo (fuente de verdad):** `~/lead-machine/` en la Mac, **en git** (branch `main`). Deploy en VPS: `/opt/lead-machine/`.

## 3. Stack y arquitectura
- **Backend:** FastAPI + SQLite (stdlib, WAL) + Google Places v1 + Gemini 2.5 Flash. Todo en `app.py`. Sin deps pesadas (httpx, fastapi, uvicorn, pydantic, openpyxl, fpdf2).
- **Frontend:** `static/index.html` (vanilla JS, tema oscuro premium, nav por tabs Buscar/Mis leads), `static/admin.html` (panel admin).
- **Auth:** cookie de sesión firmada HMAC (`lm_session`), password pbkdf2, + Google OAuth (con state CSRF). Cookie `Secure` en HTTPS.

### Modelo de datos (SQLite, todas creadas en `init_db`)
- `brands` (id, email, pwd_hash, nombre, telefono, url, profile, products, targets, free_used, paid_credits, unlimited, last_results, created_at). OAuth: pwd_hash="google-oauth".
- `coupons` (code PK, credits, unlimited, redeemed_by, redeemed_at). Claim atómico en redeem.
- `mp_payments` (pay_id PK = idempotencia, brand_id, leads, at).
- `saved_leads` (id, brand_id, **place_key UNIQUE por marca**, data=JSON del lead completo, lat, lng, fit_score, region, **status** [nuevo|visitar|contactado|visitado|descartado], notes, created_at, updated_at). Índices por brand y por status.
- **Créditos:** 5 free (free_used) + paid_credits, o unlimited. 1 lead enriquecido OK = 1 crédito. La búsqueda consume SOLO los que pidió y SOLO los que la IA enriqueció bien.

### Endpoints (app.py)
`/api/{register,login,logout,me,health}` · `/api/auth/google[/callback]` · `/api/detect` · `/api/autocomplete?q=` · `/api/leads` (search+enrich+guarda en cuenta) · `/api/redeem` · **`/api/my-leads`** (GET lista+facetas / `PATCH {id}` status+notas / `POST /bulk` / `DELETE {id}`) · `/api/export?format=csv|xlsx|json|pdf&status=&ids=&provincia=&localidad=` · `/api/checkout/{pack_id}` · `/api/mp/webhook` · `/api/pricing` · `/api/admin/{brands,stats,coupons,coupon}` · `/` `/admin`.

### Flujo `/api/leads` (el core)
Async con concurrencia acotada: Places por rubro (paralelo) → dedupe → fetch sitios (paralelo, anti-SSRF) → enrich Gemini en batches chicos (paralelo) → score ponderado → guarda en `saved_leads` (UPSERT, preserva status/notas) → consume créditos solo de los enriquecidos OK. Lock por marca anti doble-gasto. **18 leads en ~28s.**

## 4. Cómo correr / testear / deployar
```bash
cd ~/lead-machine
# dev local
.venv/bin/uvicorn app:app --reload --port 8201        # (o launch.json "lm-dev")
# tests (rápidos, sin red, DB descartable)
./run-tests.sh
# deploy seguro (tests→backup→rsync DB-excluida→smoke→rollback automático)
./deploy.sh
# backup manual de prod
ssh root@76.13.228.77 /opt/lead-machine/backup_db.sh
```
**Env tuneables (sin tocar código):** `LM_DB`, `LM_RATELIMIT` (0=off), `LM_RL_{REGISTER,LOGIN,DETECT,AUTOCOMPLETE,LEADS}`, `LM_SITE_CONCURRENCY`, `LM_GEMINI_CONCURRENCY`, `LM_PLACES_CONCURRENCY`, `LM_ENRICH_BATCH`, `LM_LEADS_MAX_COUNT`, `LM_COOKIE_SECURE`, `LM_ADMIN_KEY`, `LM_FREE_LEADS`.

## 5. Harness de robustez (5 capas, vivas) — detalle en HARNESS.md
1. **git** (`main`, .gitignore excluye secretos/DB/backups).
2. **tests** `tests/test_app.py` (45 checks sin red).
3. **deploy.sh** (con rollback automático; verifica que NO se transfiera la DB).
4. **monitor** `ops/monitor.py` cron `*/15` en VPS: servicio+health(db_ok)+integrity → alerta WhatsApp a Andrés solo en transiciones. Log `/var/log/lead-machine-monitor.log`.
5. **boot-guard** integrity_check al arrancar → `/api/health` expone `db_ok`.
- **Backups:** `backup_db.sh` cron diario 4 AM (`.backup` consistente, gzip, retención 14d) en `/opt/lead-machine/backups/`.

## 6. Integraciones + credenciales (en `/opt/lead-machine/.env`, chmod 600)
- `PLACES_API_KEY`, `GEMINI_API_KEY` (= SmartBrain `/etc/smartbrain/.env`). **Siempre `gemini-2.5-flash`** (2.0 da 404). Máx 10 items/batch a Gemini.
- `MP_ACCESS_TOKEN` + `MP_PUBLIC_KEY` (MercadoPago PRODUCCIÓN — ⚠ **ROTAR, se compartieron en texto plano**).
- `GOOGLE_CLIENT_ID` + `GOOGLE_CLIENT_SECRET` (OAuth — ⚠ **ROTAR**). Redirect URI en Google: `https://leadmachine.76.13.228.77.nip.io/api/auth/google/callback`. Verificar consent screen (Testing vs publicado).
- `PUBLIC_BASE_URL=https://leadmachine.76.13.228.77.nip.io`, `LM_ADMIN_KEY`.

## 7. Pricing / packs (ARS)
Free 5 · **Probar** 30=$25.000 · **Salir a vender** 100=$70.000 · **Expansión** 250=$150.000 · Mensual $80.000 · Done-for-you desde $250.000. WTP real Almadre/Plante: packs one-off USD 20-55; ARPU alto = done-for-you. COGS ~USD 0.03/lead → precio por valor (lead calificado, no lista cruda).

## 8. PENDIENTES (lo que sigue) — necesitan a Andrés
1. **Validar webhook MP con pago real** (o simulador del panel MP). El código ya valida monto+moneda; falta cerrar el loop con plata real.
2. **Rotar credenciales** MP + Google (texto plano) y actualizar `/opt/lead-machine/.env` (luego `systemctl restart`).
3. **Nombre + dominio** (ver §10) → comprar + repointar (`server_name` nginx + cert + `PUBLIC_BASE_URL` + redirect URI Google).
4. **(Opcional) Captcha** (Cloudflare Turnstile) en register para reforzar anti-abuso.
5. **(Opcional) Plantilla WhatsApp APPROVED** para que las alertas del monitor entren siempre (hoy texto = solo ventana 24h).
6. **(Opcional) Landing/onboarding** claro (qué es, 3 pasos, pricing) para bajar fricción de registro.
7. QA con 2-3 marcas reales (Almadre/Plante) → primeros pagos.

## 9. Estado actual (jun 21 2026, fin de sesión)
- Código nuevo + **DB fresca sana** en prod. Feature "Mis leads" vivo y verificado end-to-end (incl. browser).
- Quedan 2 brands de test del stress de QA (inofensivas; wipe opcional para arrancar pristino).
- El account `andy@smartfoods.ar` se perdió en el wipe de recuperación (era data de test) → **re-registrate** al entrar.
- Para wipe pristino antes de lanzar: `ssh root@76.13.228.77 "systemctl stop lead-machine.service; cd /opt/lead-machine; cp leadmachine.db _predeploy_bak/; rm -f leadmachine.db*; systemctl start lead-machine.service"`.

## 10. Naming (en discusión)
Candidatos CEO: RetailFlow, BrandFit (verificar si están tomados). Sugeridos: **ShelfScout** (tech/global), **Góndola** (ownable LATAM), Fitscout, Calce, ShelfFit, ShelfRadar, Prospecta. Falta chequear dominio + marca (INPI/global).

## 11. Gotchas / lecciones (NO repetir)
- **Corrupción SQLite:** NO rescatar el archivo dañado (arrastra daño latente que se re-propaga al escribir). Restaurar de backup sano o, si los datos no son críticos, DB fresca. El backup diario es la red real. (Pasó 2× esta sesión; entorno verificado sano vía stress test.)
- **Deploy:** SIEMPRE `./deploy.sh` (excluye y VERIFICA que no se transfiera ningún `.db`). El rsync a mano sin `--exclude '*.db'` puede pisar/corromper la DB de prod.
- **Frontend:** `.hide` usa `!important` (si no, `.bulkbar{display:flex}` lo pisaba).
- **Gemini:** `gemini-2.5-flash` siempre; máx 10 items/batch (más trunca el JSON).
- **Agnóstico de marca:** no hardcodear Smart Foods/rubros/zonas → todo configurable por el user.
- **No commitear** la DB ni `.env` (ya gitignoreados). **No** cambiar el esquema sin migración aditiva (`CREATE TABLE IF NOT EXISTS`).

## 12. Changelog condensado
v1 flujo base · v2 calificación (vibe check, marcas, actividad, clusters) · v3 scoring transparente con pesos + geo + contacto · v4 WhatsApp 1-clic + filtros + PDF ruta · v5 packs + MercadoPago + admin signups + app pública · v6 panel admin + alta enriquecida + Google OAuth · v7 control de cantidad + fix 504 · **v8 async /api/leads (paralelo) + batch seguridad (rate-limit, cupón atómico, MP monto, anti-SSRF, admin header, cookie secure, OAuth state, WAL) + backup** · **v9 feature "Mis leads" (saved_leads, detalle, status, PDF a paridad)** · **v10 harness 5 capas (git, tests, deploy.sh, monitor, boot-guard)**.

## Notas de negocio
Pivote: Smart Foods (CPG de Andrés) **ya no opera**; Lead Machine es el producto nuevo, agnóstico, para venderle a marcas del segmento (KR, Plante, Maquiphenol, etc.). Relacionado: [[project_smartfoods_crisis_may2026]], [[project_deerflow_smartbrain]] (motor "dossier profundo" futuro, tier premium).
