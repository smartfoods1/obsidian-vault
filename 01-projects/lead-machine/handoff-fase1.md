---
date: 2026-06-21
type: handoff
tags: [lead-machine, fase1, tier1, react, handoff]
status: completado
derivado_de: v2-vision-arquitectura.md
---

> ✅ **FASE 1 COMPLETADA + DEPLOYADA (jun 21 2026).** SF0→SF4 hechos en branch `feat/tier1-leads-react` (5 commits, base `e190bda`): SPA en `/app` (grilla + ficha 6 secciones + PipelineEditor PATCH-optimista), 2 rutas `/app` en app.py (catch-all file-check), tests verde, `deploy.sh` con build+smoke `/app`, deployado a prod y verificado en vivo (`/` cobra, `/app/leads` carga, assets 200, deep-link OK). Diseño + review por workflows multi-agente. **Pendiente: merge branch→`main`.** Próximo: **Fase 2 — enrichers multi-fuente** (ver `v2-vision-arquitectura.md`).

# Lead Machine — Handoff para Fase 1 (ficha Tier-1 en React)

> Documento autocontenido para continuar en una ventana nueva. Lo de abajo + la memoria `project_lead_machine.md` (v1–v16, se autocarga) alcanza para ejecutar Fase 1 sin la conversación anterior.

## 0. Cómo arrancar (leé en este orden)
1. `cd ~/lead-machine` — Claude Code lee `CLAUDE.md`(=`AGENTS.md`) solo.
2. Leé `HARNESS.md` (operación) + este handoff + `01-projects/lead-machine/v2-vision-arquitectura.md` (la visión completa y las decisiones lockeadas).
3. **Regla de oro: nunca deployar a mano → `./deploy.sh`** (tests→backup→rsync DB-excluida→smoke→rollback automático). Antes de cualquier cambio: `./run-tests.sh`.

## 1. Qué es / estado
SaaS de prospección B2B para marcas de alimentos AR. **VIVO en prod y cobrando.** Agnóstico de marca.
Estamos re-arquitecturando a producto **Tier-1 con base de datos propia + efecto de red** (visión v2). **Ya desplegado y commiteado:** P0, P1, P2 (de buscador a CRM de venta) + **Fase 0 v2** (base global compartida + split de privacidad). **Próximo: Fase 1** (la ficha Tier-1 en React — el primer salto VISIBLE).

## 2. Accesos / harness
- **Repo:** `~/lead-machine/` en git (branch `main`, **sin remote**). Backend single-file `app.py` (~1900 líneas). Frontend HOY: `static/index.html` (vanilla JS, oscuro neón). Tests `tests/test_app.py` (~96 checks sin red, TestClient, siembra con `app._save_leads`, NO pega a Places/Gemini).
- **Prod:** VPS `root@76.13.228.77`, service `lead-machine.service` (uvicorn 127.0.0.1:8200), https://leadmachine.76.13.228.77.nip.io. `/opt/lead-machine/`. Admin `/admin` (key `LM_ADMIN_KEY` en `/opt/lead-machine/.env`).
- **Flujo obligatorio:** editar → `./run-tests.sh` → `./deploy.sh`. Migraciones SOLO aditivas (`CREATE IF NOT EXISTS` + loop `ALTER` con try/except). `gemini-2.5-flash`, máx 10/batch. App request/response (workers = Fase 3, no ahora).
- Local: `.venv/bin/uvicorn app:app --reload --port 8000`. `node -v` = v24.15.0 (OK para Vite). DB local `leadmachine.db` (no commitear).

## 3. Lo ya hecho (lo que Fase 1 consume)
**P0–P2** (commit `c83e4d4`): oferta mayorista al icebreaker, multicanal email/IG, WhatsApp honesto (`_infer_whatsapp` normaliza a +549, `wa_verificado`), pipeline por `outcome`, `touch`, demo pre-login, vencidos/`sort=accion`, editar icebreaker (`message_override`), no-recobrar (`_split_candidates`), `deal_value`+ROI (`revenue_won`/`revenue_pipeline`), generador 2º mensaje (`/followup`).
**Fase 0 v2** (commit `e190bda`): `global_places` (comercio FACTUAL compartido, merge no-clobber) + `saved_leads` = capa PRIVADA por marca (linkeada por `global_place_id`) + `lead_facts` (procedencia `source`+`fetched_at` por dato) + backfill idempotente al boot. En prod: ~1956 comercios globales, 0 unlinked, 0 fugas.

## 4. Contrato de API (NO se toca en Fase 1; ya devuelve todo)
- **GET `/api/lead/{id}`** (la ficha): `{lead_id, place_key, global:{nombre,direccion,calle,localidad,provincia,codigo_postal,telefono,whatsapp,wa_verificado,wa_motivo,website,maps,rating,reviews,tipo,lat,lng,price_level,email,instagram,nombre_contacto,reviews_list,place_id,actividad}, facts:[{field,source,fetched_at}], pipeline:{status,outcome,notes,deal_value,next_action_at,last_contacted_at,message_override,primer_mensaje,primer_mensaje_ia,fit_score,fit_reason,score_breakdown,saved_at}, first_seen_at, shared}`. SIEMPRE filtrado por brand_id → marca ajena 404.
- **GET `/api/my-leads?status=&q=&provincia=&localidad=&sort=accion`** (la grilla): `{count,total,leads[],provincias,localidades,status_counts,follow_ups_overdue,new_7d,revenue_won,revenue_pipeline,clusters,credits,pricing}`. Cada lead trae `lead_id,nombre,tipo,localidad,fit_score,fit_reason,status,outcome,deal_value,next_action_at,vencido,priority_reason,whatsapp,wa_verificado,email,instagram,website,rating,...`.
- **PATCH `/api/my-leads/{id}`** `{status?,outcome?,next_action_at?(YYYY-MM-DD),message_override?,deal_value?(int 0..1e12),touch?,notes?}` → `{ok,lead}`.
- **POST `/api/my-leads/{id}/followup`** → `{mensaje}`. **POST `/api/my-leads/bulk`** `{ids,status}`. **DELETE** `/api/my-leads/{id}`. **GET** `/api/me`, `/api/export?format=`. Auth = cookie `lm_session` httponly+SameSite=lax+secure.

## 5. Decisiones v2 lockeadas (de Andrés)
1. **Tier-1 = detalle premium primero, NO rewrite.** Montar Leads+Detalle en React; "Buscar" queda en vanilla.
2. Base comparte dato objetivo + señal agregada k-anónima (k=3, **apagada hasta ≥3 marcas** — Fase 4).
3. Enriquecimiento de fondo = híbrido (lead nuevo lo paga el user; fondo lo paga el sistema; DeerFlow premium).
4. **Smart Foods se autoexcluye** de las señales de red (conflicto de interés).

## 6. FASE 1 — el plan (ejecutable)
**Objetivo:** SPA React de "detalle premium primero" (grilla de Leads densa Apollo/Clay + ficha que respira Stripe/Notion) servida en **`/app`** por el MISMO FastAPI, conviviendo con el Buscar vanilla en `/` **sin tocarlo**. Mata el oscuro-neón con tokens claros índigo/Inter. Mapea 1:1 a los endpoints que ya existen. Backend casi no cambia (2 rutas HTML triviales).

### Stack decidido
- React 19 + Vite + TS + Tailwind v4 + react-router-dom, en **`~/lead-machine/webapp/`** (sub-proyecto aislado, su propio package.json).
- **Coexistencia por PREFIJO**: `/` = Buscar vanilla INTOCABLE; `/app/leads` + `/app/lead/:id` = SPA.
- Vite: `base:'/app/'`, `build.outDir:'../static/app'`, `emptyOutDir:true`. El bundle sale a `static/app/` y lo sirve el `app.mount('/static',...)` existente. `server.proxy` en dev: `/api`→`http://127.0.0.1:8000` (para que la cookie viaje same-origin).
- `app.py` suma SOLO 2 rutas (junto a `index()`/`admin_page()`, ~línea 1938): `@app.get('/app')` y `@app.get('/app/{full_path:path}')`, ambas devuelven `(ROOT/'static'/'app'/'index.html').read_text()`. El catch-all es el SPA-fallback para deep-links — **anclado a `/app`, NUNCA `/{path:path}` global** (secuestraría /api y /static).
- Data-fetching: **fetch nativo** con `credentials:'include'` (wrapper `webapp/src/api.ts`), SIN react-query en Fase 1. 401 → redirect a `/`. La cookie es httponly → NO se lee en JS, NO se toca auth.
- **Commitear el dist `static/app/`** (excepción consciente: el deploy es rsync de disco, sin Node en el VPS). `deploy.sh` igual regenera el build como step 0.
- Design system: tokens SmartBrain (índigo #4F46E5 / Inter / Tabler), paleta clara, `tabular-nums`, CSS vars (regla no-hardcode), Inter self-hosted.

### Sub-fases (cada una deja el repo sano)
- **SF0 — Scaffold + baseline**: `git checkout -b feat/tier1-leads-react`; `./run-tests.sh` (fijar baseline verde). `npm create vite@latest webapp -- --template react-ts`; instalar router + tailwind v4; setear vite.config (base/outDir/proxy). Build de humo → confirmar que `static/app/index.html` referencia `/app/assets/*`. (No deployable aún.)
- **SF1 — Tokens + cliente API + grilla densa**: `webapp/src/index.css` (tokens claros) + `webapp/src/api.ts` (tipos TS exactos, `credentials:'include'`, 401→/). `LeadsPage.tsx` (grilla ~38px, sort=accion default, filtros de `status_counts`/`provincias`, columnas comercio/fit/canales/estado/resultado/próxima-acción(roja si `vencido`)/frescura, click→/app/lead/:id, bulk). Componentes `LeadTable,StatusBadge,FitScore,EmptyState,ErrorState,Skeleton`.
- **SF2 — Ficha premium + PATCH**: `LeadDetailPage.tsx` ← `GET /api/lead/{id}`, 6 secciones (identidad←global, contactabilidad multicanal←global, redes, inteligencia de marca←pipeline.fit/score_breakdown/global.reviews_list, timeline←first_seen_at/saved_at/contacto, pipeline editable inline). `FactStamp` indexando `facts[]` por field (fuente+frescura). `PipelineEditor` con PATCH optimista. Botón followup. Router basename='/app'.
- **SF3 — Integración FastAPI + test de regresión**: agregar las 2 rutas `/app` en app.py. Verificar a mano: `/` vanilla OK, `/app/leads` OK, deep-link `/app/lead/<id>` sin 404. Sumar a tests/test_app.py (bloque `cp`/`plid`): checks de shape de `/api/lead/{id}` (top-level, `global` factual, `pipeline`, y que `posicionamiento`/`marcas_complementarias`/`ecosistema` **NO** estén en `global`) + que `GET /` sigue sirviendo el vanilla + `GET /app` devuelve HTML con `id="root"`. `./run-tests.sh`.
- **SF4 — deploy.sh + deploy real**: a `EXCLUDES` sumar `--exclude 'webapp' --exclude 'node_modules'` (el dist `static/app/` SÍ viaja). Step 0 antes de tests: `cd webapp && npm ci && npm run build && cd ..` (die si falla). En el smoke (paso 7), tras la búsqueda real: `curl $BASE_URL/app | grep -q 'id="root"' || rollback` (grep marcador ESTABLE, nunca el JS hasheado). Commitear webapp/ source + static/app/ dist + app.py + deploy.sh + tests juntos. `./deploy.sh`.

### Criterio de "listo" (verificable)
- `./run-tests.sh` verde (96 previos + shape de `/api/lead/{id}` + regresión: `/` sirve vanilla, `/app` sirve bundle con `id="root"`).
- Local: `/` Buscar vanilla intacto (login+búsqueda funcionan); `/app/leads` grilla React; deep-link `/app/lead/<id>` sin 404; assets cargan 200 detrás de `/app` (no pantalla en blanco).
- Ficha con las 6 secciones + sellos de procedencia (de `facts[]`); PATCH persiste.
- `./deploy.sh` verde de punta a punta (build→tests→...→smoke con curl /app→rollback si falla). En prod `/app/leads` carga logueado; `/` sigue cobrando.

## 7. Gotchas (NO repetir — varios ya nos costaron)
- **NO tocar `@app.get('/')` ni `static/index.html`**: es la app que cobra HOY (login+Buscar). La SPA vive en `/app`, no reemplaza nada en Fase 1.
- Catch-all **`/app/{full_path:path}`, NUNCA `/{full_path:path}` global** (se traga /api y /static). Correr `./run-tests.sh` después de agregarlo.
- Vite `base` mal = pantalla en blanco (assets a `/assets/*` → 404 detrás de /app). DEBE ser `base:'/app/'`. Probar con uvicorn sirviendo el build, no solo `vite dev`.
- **⚠ CORRECCIÓN AL PLAN SF3 (verificado SF0/SF1, jun 21):** el catch-all `/app/{full_path:path}` **NO puede devolver SIEMPRE `index.html`**. Con `base:'/app/'` los assets se piden a `/app/assets/*`, y el mount `/static` sirve en `/static/*` → NO los cubre. Si el catch-all devuelve index.html para todo, los assets bajan HTML → MIME mismatch → **white-screen**. SF3 debe servir el archivo real si existe y recién después caer a index.html (SPA fallback):
  ```python
  @app.get("/app/{full_path:path}")
  def spa(full_path: str):
      fp = ROOT / "static" / "app" / full_path
      if full_path and fp.is_file():
          return FileResponse(fp)            # asset real (mime correcto)
      return HTMLResponse((ROOT/"static"/"app"/"index.html").read_text(encoding="utf-8"))  # deep-link
  ```
  Patrón validado en local con un runner throwaway (`/tmp/lm_preview.py`, NO commiteado): `/app/leads`, deep-link `/app/lead/:id` (carga fría) y `/app/assets/*.woff2` todos 200. `@app.get('/app')` (sin path) aparte para la raíz exacta.
- Cookie en `vite dev` (5173) contra API de prod NO cruza de origen → 401. Dev = `server.proxy /api→127.0.0.1:8000`. NUNCA "arreglar" tocando SameSite/secure en el backend.
- `deploy.sh` rsync sube todo salvo EXCLUDES → agregar `webapp` + `node_modules` o subís cientos de MB. El dist `static/app/` SÍ debe viajar.
- Build ANTES del rsync + dist commiteado; si no, prod sirve `/app` vacío → 404. El smoke `curl /app | grep id="root"` lo atrapa con rollback.
- Ícono WA prende SOLO si `whatsapp && wa_verificado` (no por tener teléfono).
- `vencido` lo calcula el backend en hora AR (UTC-3) → **NO recalcular fecha en el browser** con `new Date()` local. Usar los flags `vencido`/`priority_reason` del response.
- **Privacidad (riesgo #1):** `posicionamiento`/`marcas_complementarias`/`ecosistema` son brand-relativos (salen de `pipeline`, NO de `global`). La ficha NO los expone como factuales del comercio. El test de shape afirma que NO están en `global`. Validar fugas por CLAVE de JSON, **nunca por `LIKE`/substring** (texto de reseña con "ecosistema" da falso positivo).
- NO meter el build de Vite dentro de `run-tests.sh` (su contrato es "tests rápidos sin red en Python"). Build = step 0 de deploy.sh.

## 8. Mensaje sugerido para arrancar la ventana nueva
> Continúo Lead Machine — **Fase 1** (ficha Tier-1 en React). Leé `~/lead-machine/AGENTS.md`, `~/lead-machine/HARNESS.md` y Obsidian `01-projects/lead-machine/handoff-fase1.md` (tiene el plan completo, el contrato de API y los gotchas) + `v2-vision-arquitectura.md`. Regla de oro: nunca deploy a mano → `./deploy.sh`; antes de cambios `./run-tests.sh`. Arrancá por SF0 del plan (branch `feat/tier1-leads-react`, baseline de tests, scaffold `webapp/` con Vite base:'/app/'). NO toques `/` ni `static/index.html` (es lo que cobra). Quiero que arranques con SF0 y SF1.
