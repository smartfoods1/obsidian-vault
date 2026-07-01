---
date: 2026-06-21
type: arquitectura
tags: [lead-machine, saas, b2b, tier1, efecto-red, arquitectura, vision]
status: activo
derivado_de: roadmap-contactar-vender.md
---

# Lead Machine v2 — Visión Tier-1: base de datos viva con efecto de red

> Salida de un análisis multi-agente (6 lentes expertas + síntesis) sobre la visión de Andrés. Jun 21 2026.
> **Decisiones-fork tomadas por Andrés (ver §Decisiones).** Estado: plan aprobado en dirección, Fase 0 lista para arrancar. NO construir más allá de lo decidido.

## Principio rector

Lead Machine deja de ser un **scraper que cada marca paga por pasada** (silo, request/response, foto de un momento) y se convierte en una **base de datos PROPIA de comercios argentinos que se enriquece sola con el uso de todos** — donde el **dato factual del comercio es un activo compartido** y la **relación comercial de cada marca es un secreto privado e intocable**.

## La esencia (lo que pidió Andrés)

1. **El dato es el activo, no la búsqueda.** Cada lead que alguien encuentra alimenta la DB propia; más usuarios → base más rica y más defendible. Moat, no feature.
2. **El trato honesto:** el comercio (existe, dónde, reseñas, web, redes) es hecho público → se comparte. A quién contactaste / qué respondió / cuánto cerraste es secreto comercial → jamás cruza al competidor de canal.
3. **Tier-1 = que una marca lo pague sin pensar.** Se nota sobre todo en la ficha de detalle: el lead pasa de fila apretada a **entidad** con su página rica, con **procedencia + frescura** de cada dato a la vista.
4. **Enriquecimiento = dossier que se completa solo:** Places + redes + web search, incremental, con un agente de fondo. (Justo lo que el harness prohíbe hoy — y el miedo a quemar cuota es correcto.)
5. **El outcome es combustible, no un dato muerto:** mejora el score, prioriza al agente, le dice al próximo usuario qué convierte. Agregado, anónimo, sin humo de ML.

## Arquitectura objetivo

| Componente | Rol |
|---|---|
| **API** (mismo app.py single-file) | Request/response como hoy. Sirve JSON + bundle SPA. Gana: encolar jobs de enriquecimiento (no ejecutarlos) y leer facts. Nunca corre el worker. |
| **Worker** (2º modo del mismo app.py, service systemd) | Loop largo (NO cron) que drena la cola con presupuesto diario duro. Reusa Places/Gemini/scrape. Nace APAGADO (budget 0). |
| **`global_places`** (entidad comercio, COMPARTIDA) | 1 fila por comercio, anclada a place_id de Google. Dato factual público: nombre, geo, rating, reseñas, tel, web, redes, resumen. El activo del efecto de red. |
| **`lead_pipeline`** (PRIVADO por marca) | (brand_id, place_id) con status/outcome/notes/deal_value/message_override/fechas. SIEMPRE filtrado por brand_id. Imposible que una marca vea el pipeline de otra. |
| **`lead_facts`** (procedencia+frescura) | Cada dato = hecho atómico con source (places/site/instagram/websearch/deerflow/user) + fetched_at + confianza. Resuelve conflictos (user > scrape > inferencia IA). |
| **`segment_stats`** (señal agregada anónima) | Estadística por ARQUETIPO (rubro × banda reseñas × rating × zona), nunca por comercio identificado. k-anonimato. El moat defendible. |
| **`enrich_jobs` + `cost_ledger`** | Cola durable en SQLite con claim atómico (patrón WhatsApp). Tope de costo duro + kill-switch. Presupuesto system vs user separado. |
| **SPA React/Vite** | Workspace (Buscar / Leads / Pipeline), data-grid denso, slide-over expandible a `/lead/:id`. Reusa design system de SmartBrain con tokens propios. |
| **DeerFlow** (enricher profundo) | Ya desplegado, vía MCP. Enricher tier 'profundo' on-demand (botón en detalle / auto solo alto fit). Crédito premium. |

## Modelo de datos (la partición ES la solución a la privacidad)

- **Global compartido** (`global_places` + `lead_facts`): el comercio como hecho público (público en Maps/web igual). Se enriquece una vez, se amortiza entre todas. Cada dato con fuente+fecha+confianza (sin eso, un email viejo/alucinado envenena la base de todos).
- **Privado por marca** (`lead_pipeline`): a quién contactaste, qué respondió, cotizaste, cerraste, notas, icebreaker, tu fit relativo a TU oferta. Nunca cruza entre marcas. Tabla propia siempre filtrada por brand_id.
- **Señal agregada anónima** (`segment_stats`): el puente. No "la dietética X respondió"; sí "dietéticas premium 200+ reseñas CABA convierten 38%". Arquetipo, respaldado por ≥k marcas. **Línea roja: nunca guarda identidad de comercio ni de marca compradora.**

## El punto de inflexión (sin vueltas)

Esto deja de ser single-file/request-response puro: el agente de fondo es incompatible con request/response. PERO el cruce respeta el espíritu del harness: (1) worker = 2º sombrero del mismo app.py (`python app.py worker`), no microservicio/Redis/Celery; cola = tabla SQLite con claim atómico. (2) loop con presupuesto, NO cron. (3) migraciones aditivas; `saved_leads` intacto, solo-lectura, backfill idempotente. (4) deploy.sh sigue rsync+restart, ahora 2 services + build SPA. El 80% del salto sensorial sale de la ficha de detalle, NO de reescribir el frontend.

## Secuencia (cada fase deployable sola)

- **Fase 0 — Cimientos de datos** ✅ **DEPLOYADA+verificada+commiteada (e190bda, jun 21)**: `global_places` (factual compartido, merge no-clobber) + `saved_leads` como capa privada linkeada por `global_place_id` + `lead_facts` (procedencia+frescura) + `GET /api/lead/{id}` (JOIN global+privado filtrado por brand_id) + backfill idempotente al boot. Prod: 1956 global_places, 0 unlinked, 0 fugas reales, integrity ok. 2 blockers de privacidad cazados en review (campos brand-relativos fuera del global; merge no clobber). **OJO chequear fugas por CLAVE JSON, no por LIKE/substring.**
- **Fase 1 — Ficha Tier-1 + efecto de red mínimo (MVP)** ✅ **DEPLOYADA+verificada+commiteada (jun 21, branch `feat/tier1-leads-react`)**: SPA React/Vite/TS/Tailwind v4 en `/app` conviviendo con el `/` vanilla que cobra (coexistencia por prefijo, sin tocar lo que factura). Grilla densa de leads (`/app/leads`) + ficha de 6 secciones (`/app/lead/:id`, deep-link OK): identidad, contacto multicanal, redes, inteligencia de marca (fit_reason + score_breakdown), timeline de relación, pipeline editable inline (PATCH optimista + rollback) + FactStamp fuente/frescura. Backend: 2 rutas `/app` con catch-all file-check (sirve asset real, sino index.html — NO "siempre index.html", eso daba white-screen). Diseño + review adversarial vía workflows multi-agente (6 hallazgos fixeados). Privacidad: la ficha solo muestra data del contrato; separación física global(izq)/pipeline(der); cero texto brand-relativo. Prod: `/` cobra, `/app/leads` carga logueado, assets 200. **Pendiente: merge a `main`** (deploy salió de la branch).
- **Fase 2 — Enrichers multi-fuente** ✅ **DEPLOYADA+verificada+commiteada (jun 21, `1d05989`)**: `POST /api/lead/{id}/enrich` completa el contacto factual de la capa GLOBAL on-demand (re-scrape sitio + Serper opcional + 1 síntesis Gemini), confidence por fuente, facts negativos, completeness en la ficha (DossierBar "Completar dossier"). Anti-quema-cuota (review de 5 hallazgos): CLAIM ATÓMICO sobre enriched_at, `soft_error` (fallo transitorio NO sella TTL ni graba negativos falsos), TTL por cutoff UTC, caps por-marca + global. No cobra crédito. Serper/DeerFlow opcionales (no configurados aún). Verificado en prod: completeness 75%, sellos de procedencia, privacidad OK.
- **Fase 3 — El worker** ✅ **DEPLOYADA+commiteada (jun 21, `21fa6f6`), NACE APAGADO**: worker = 2º modo (`python app.py worker`), drena `enrich_jobs` (claim atómico + dedup por índice parcial + backoff) con `cost_ledger` (tope diario DURO) + kill-switch (.worker_kill) + reaper de boot. API encola (gateado en budget>0). Review de 6 hallazgos (BUDGET-1 critical: costo registrado SIEMPRE; CONC-1: reaper). systemd OPT-IN en `ops/lead-machine-worker.service` — **deploy.sh NO lo instala**; en prod el worker NO corre (budget 0). Para armarlo: instalar el service + `LM_WORKER_BUDGET=<USD/día>`.
- **Fase 4 — Loop que aprende** ✅ **DEPLOYADA+commiteada (jun 21, `4d3578c`), DORMIDA (k=3)**: `lead_events` (audit) + `segment_stats` (cache display) + `segment_key` por comercio. El GATE consume **EN VIVO** (no del agregado materializado, que quedaba rancio): `_segment_signal_live` con k-anonimato (excluidas + observador no cuentan) + n + **anti-dominancia** (max-share) → corrección bayesiana SUAVE (≤15%) del fit. Review de 8 hallazgos cerrados con la arquitectura live (stale-gate, exclusión-no-purga, outcome-clear, migración-arquetipo, dominancia, self-inclusion, fail-soft, rollback). Smart Foods se autoexcluye (no contribuye ni consume). Con pocos clientes ningún arquetipo llega a k=3 → señal dormida (verificado en prod: 0 activos).

> **Estado jun 21 2026: TODA la visión v2 (Fase 0→4) está DEPLOYADA y verificada en prod.** Branch `feat/tier1-leads-react` (pendiente merge a `main`). Worker de fondo apagado (opt-in). Señal de red dormida hasta k=3.

## Decisiones tomadas por Andrés (lockeadas, jun 21 2026)

1. **Arranque Tier-1 → Detalle premium primero.** Montar Leads + ficha de detalle en React (donde está el salto); 'Buscar' después. Evita la trampa del rewrite.
2. **Base compartida → Objetivo + señal agregada k-anónima.** Andrés quiere la señal de uso desde temprano, no solo en Fase 4. ⚠ TENSIÓN: con 2-3 clientes al arranque, k=3 no se cumple → se CONSTRUYE `segment_stats` con k=3 desde el día 1, pero queda APAGADA/invisible hasta que haya ≥3 marcas por arquetipo. Hasta entonces, solo vive el efecto de red de dato objetivo. (Honra la decisión sin exponer a nadie.)
3. **Quién paga el fondo → Híbrido.** Lead nuevo lo paga el user (como hoy); refresh/social/web de fondo lo paga el sistema, topado; DeerFlow = crédito premium aparte.
4. **Conflicto de interés → Smart Foods se autoexcluye.** SF no consume señales agregadas de la red. Máxima confianza con clientes que compiten con el CPG. Se comunica por escrito.

Pendiente derivado: el umbral **k** quedó en **3** (estándar; con 2 hay de-anonimato por descarte, con 5 la base tarda meses en dar señal).

## Riesgos principales

1. **Fuga de pipeline entre competidores** (#1, de confianza no técnico): un JOIN sin filtrar brand_id expone outcome/deal de otro. lead_pipeline SIEMPRE filtrada, testeado.
2. **Romper la app que factura**: solo migraciones aditivas, backfill idempotente que no borra saved_leads.data, deploy.sh con backup+smoke+rollback, validar sobre copia de prod.
3. **Quemado de cuota por el worker**: presupuesto duro + separación system/user + kill-switch = condición de existencia del agente.
4. **Base envenenada**: sin procedencia+confianza, un email malo/alucinación se propaga a todas. Modelo de facts = prerequisito.
5. **De-anonimato con pocas marcas**: señales agregadas APAGADAS hasta k=3 robusto.
6. **Trampa del rewrite / scope creep**: fases deployables solas; detalle premium antes que SPA completa; DeerFlow y scoring-que-aprende fuera del MVP.
7. **Erosión de margen**: cada fuente nueva sube el costo/lead; modelar costo-por-lead-100% antes de prender enrichers por default.
