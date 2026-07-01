---
date: 2026-06-21
type: handoff
tags: [lead-machine, v2, tier1, fase0-4, deployado, handoff]
status: activo
derivado_de: v2-vision-arquitectura.md
---

# Lead Machine v2 — Handoff COMPLETO (Fases 0→4 deployadas)

> Documento autocontenido para continuar en una ventana nueva. Esto + la memoria `project_lead_machine.md`
> (v1–v19, autocarga) + `v2-vision-arquitectura.md` alcanza para seguir sin la conversación anterior.

## 0. Estado en una línea
**Toda la visión v2 (Fase 0→4) está implementada, revisada adversarialmente, deployada y verificada en prod.**
El producto pasó de "scraper que cobra por pasada" a "base de datos viva con ficha Tier-1, enricher on-demand,
worker de fondo (apagado) y loop de aprendizaje k-anónimo (dormido)". Falta SOLO mergear la branch a `main`.

## 1. Cómo arrancar (leé en este orden)
1. `cd ~/lead-machine` — Claude Code lee `CLAUDE.md`(=`AGENTS.md`) solo.
2. Leé `HARNESS.md` (operación: tests/deploy/worker/restaurar backup) + este handoff + `v2-vision-arquitectura.md`.
3. **Regla de oro: nunca deployar a mano → `./deploy.sh`** (build SPA → tests → backup → rsync DB-excluida → smoke → rollback). Antes de cambios: `./run-tests.sh` (132 checks sin red).

## 2. Accesos / harness
- **Repo:** `~/lead-machine/` en git. **Branch `feat/tier1-leads-react`** (sin remote). Base `e190bda` (Fase 0).
  Backend single-file `app.py` (~2400 líneas). Frontend vanilla `static/index.html` (`/`, lo que cobra) + SPA React en `webapp/` → dist commiteado en `static/app/` (`/app`). Tests `tests/test_app.py`.
- **Prod:** VPS `root@76.13.228.77`, service `lead-machine.service` (uvicorn 127.0.0.1:8200), https://leadmachine.76.13.228.77.nip.io. Dir `/opt/lead-machine/`. Admin `/admin` (key `LM_ADMIN_KEY` en `.env`). `.env` lo carga app.py solo (loader propio, no EnvironmentFile).
- **Commits de la branch (sobre `e190bda`):**
  - `adec9e1` SF0+SF1 — SPA React en `/app` (grilla densa)
  - `0954c03` SF2 — ficha premium 6 secciones + PipelineEditor
  - `b86ae36` SF3 — rutas `/app` en FastAPI + tests
  - `4a69e65` SF4 — deploy.sh (build + smoke /app + excludes)
  - `1d05989` Fase 2 — enricher on-demand (capa global)
  - `21fa6f6` Fase 3 — worker de fondo (nace apagado)
  - `4d3578c` Fase 4 — loop que aprende (k-anónimo, en vivo)
- `main` quedó en `e190bda`. **deploy.sh rsyncea el working tree (branch-agnóstico)** → prod corre la branch igual.
- Node v24 (OK Vite). Build local: `cd webapp && npm ci && npm run build` (lo hace deploy.sh step 0).

## 3. Arquitectura — qué hay y dónde

### Frontend (SPA Tier-1 en `/app`, convive con `/` vanilla intocable)
- `webapp/` React 19 + Vite 8 + TS + Tailwind v4 + react-router 7. `base:'/app/'`, build a `static/app/` (dist COMMITEADO).
- Design system claro índigo `#4F46E5` / Inter self-hosted / tokens `@theme` (`webapp/src/index.css`).
- `webapp/src/api.ts` — cliente tipado, `credentials:'include'`, 401→`/`.
- `webapp/src/pages/LeadsPage.tsx` — grilla densa (sort=accion, filtros, KPIs, bulk).
- `webapp/src/pages/LeadDetailPage.tsx` + `webapp/src/components/ficha/*` — ficha de 6 secciones (Hero, Contactabilidad, Redes, Inteligencia, Timeline, PipelineEditor) + `DossierBar` (Fase 2) + `primitives` (SectionCard/FactStamp/EnrichHint/HeroFitBadge).
- `webapp/src/lib/` — score.ts (bandChip/bandFill/bandFillAxis), contact.ts (hrefs/handle/dominio/maps), format.ts.

### Backend (`app.py`) — endpoints clave
- `GET /api/my-leads` (grilla), `GET /api/lead/{id}` (ficha: global+pipeline+facts+`completeness`+`enriched_at`), `PATCH /api/my-leads/{id}` (pipeline; al setear outcome alimenta el loop Fase 4), `POST /api/my-leads/{id}/followup`, `POST /api/my-leads/bulk`, `DELETE`.
- `POST /api/lead/{id}/enrich` (Fase 2 on-demand).
- `GET /app` + `GET /app/{full_path:path}` (catch-all con file-check → sirve asset real o cae a index.html; anclado a /app, nunca global).
- `GET /api/admin/stats?admin_key=` → suma `worker {budget,armado,gastado_hoy,cola}` + `segmentos {total,activos_k,k_anon}`.

### Tablas (SQLite, migraciones aditivas en `init_db`)
- `saved_leads` (privado por marca), `global_places` (factual compartido; +cols `enriched_at`, `segment_key`), `lead_facts` (procedencia+confianza).
- `enrich_jobs` (cola Fase 3; índice UNIQUE PARCIAL idx_jobs_active WHERE status IN queued/claimed = dedup), `cost_ledger` (presupuesto worker).
- `lead_events` (audit append-only Fase 4, INTERNO), `segment_stats` (cache display k-anónimo, SIN identidad).

### Worker de fondo (Fase 3) — NACE APAGADO
- 2º modo: `python app.py worker` (no microservicio). systemd OPT-IN `ops/lead-machine-worker.service` — **deploy.sh NO lo instala**.
- `LM_WORKER_BUDGET=0` (default) → no claima nada. Para armarlo: instalar el service + `LM_WORKER_BUDGET=<USD/día>` en `.env` + restart.
- Kill-switch en caliente: `touch /opt/lead-machine/.worker_kill` (borrar para reanudar). Reaper de boot re-encola 'claimed' huérfanos.

### Loop que aprende (Fase 4) — DORMIDO (k=3)
- El GATE consume **EN VIVO** (`_segment_signal_live`) desde saved_leads, NO del agregado materializado. 3 capas: k-anonimato (≥3 marcas DISTINTAS, excluidas + observador no cuentan) + n≥10 + anti-dominancia (1 marca no aporta >50%). Corrección bayesiana SUAVE (≤15%) del fit, con traza `segment_signal`.
- **Smart Foods se autoexcluye** (no contribuye ni consume): `LM_SEGMENT_EXCLUDED=<emails>` en `.env`. Con pocos clientes ningún arquetipo llega a k=3 → señal dormida.

## 4. Decisiones / gotchas NO-obvios (no repetir lo ya peleado)
- **Catch-all `/app/{path}` DEBE servir el archivo real si existe** y recién caer a index.html. "Siempre index.html" = white-screen (los assets se piden a `/app/assets/*`, el mount `/static` no los cubre).
- **No tocar `/` ni `static/index.html`** — es lo que cobra. La SPA vive en `/app`.
- **`vencido`/fechas las da el backend en hora AR** — NO recalcular con `new Date()` en el browser.
- **Privacidad ficha:** `posicionamiento`/`marcas_complementarias`/`ecosistema` NO van en `global` (son brand-relativos). Validar fugas por CLAVE JSON, no por substring.
- **Enrich (Fase 2):** claim atómico sobre `enriched_at`; `soft_error` cuando no hay fuente / Gemini falla (NO sella TTL ni graba negativos falsos); `_gather_enrich_signals` devuelve `(extracted, spent)` → costo SIEMPRE contabilizado.
- **Worker (Fase 3):** nace apagado; costo registrado aunque el job falle; reaper de boot; `import sys` es necesario (lo usa el `__main__`).
- **Loop (Fase 4):** gate EN VIVO (no confiar en `segment_stats` materializado, queda rancio); anti-dominancia además de k; auto-exclusión del observador; consumo fail-soft en `/api/leads`.
- **deploy.sh** excluye `webapp` + `node_modules` del rsync; el dist `static/app/` SÍ viaja. Build = step 0.

## 5. PRÓXIMOS PASOS (en orden de prioridad)
1. **Merge `feat/tier1-leads-react` → `main`** (cierre de repo; prod ya corre la branch). Local, sin remote: `git checkout main && git merge feat/tier1-leads-react && git checkout feat/tier1-leads-react` (o quedarse en main). NO requiere re-deploy.
2. **(Opcional) Configurar `SERPER_API_KEY`** en `/opt/lead-machine/.env` para que el "Completar dossier" rinda cuando el comercio no tiene sitio scrapeable (hoy da `soft_error` grácil en esos casos). Es websearch pago, barato.
3. **(Cuando se quiera) Armar el worker de fondo:** instalar `ops/lead-machine-worker.service` + `LM_WORKER_BUDGET=<USD/día>`. Vigilar `cost_ledger` vía `/api/admin/stats`. Decisión de costo/riesgo del CEO.
4. **(Futuro, cuando haya ≥3 clientes/arquetipo)** la señal de red Fase 4 se enciende sola (k=3). Setear `LM_SEGMENT_EXCLUDED` con el email de la cuenta de Smart Foods ANTES de que contribuya, para no contaminar la señal.
5. **(Futuro) DeerFlow como tier de enrich "profundo"** on-demand (ya desplegado vía MCP, ver `project_deerflow_smartbrain`). No cableado aún en app.py.
6. **(Verificación opcional)** browser login en prod a `/app/leads` (la verifiqué local con runner throwaway + curl en prod; el flujo logueado-en-browser-prod no lo hice por fricción de sesión).

## 6. Notas operativas
- El enrich on-demand en prod da `soft_error` para leads sin texto en el sitio (correcto, grácil; no congela el dossier). La búsqueda normal SÍ enriquece (Gemini OK en prod, fit reales).
- Worker apagado + señal dormida = estado correcto verificado en prod (`armado:false`, `activos_k:0`).
- La DB LOCAL de dev (`~/lead-machine/leadmachine.db`) quedó con mutaciones de verificación (algunos status/enriched_at/segmentos sembrados). Es local, no commiteada, inofensiva. Prod intacta.
- Runner throwaway de verificación local: `/tmp/lm_preview.py` (app real + dev-login + rutas /app) — NO commiteado; entry `lm-preview` en `~/.claude/launch.json` (gitignored). El `app.py` real ya tiene las rutas /app, así que el runner es solo para login rápido en local.

## 7. Mensaje sugerido para la ventana nueva
> Continúo Lead Machine v2. Toda la visión (Fase 0→4) ya está deployada y verificada en prod, en la branch
> `feat/tier1-leads-react` (ver `01-projects/lead-machine/handoff-v2-completo.md` + memoria `project_lead_machine.md`).
> Próximo paso: mergear la branch a `main`. Después, según prioridad: configurar SERPER_API_KEY, o armar el worker.
> Regla de oro: nunca deploy a mano → `./deploy.sh`; antes de cambios `./run-tests.sh`.
