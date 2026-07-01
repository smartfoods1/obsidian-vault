---
date: 2026-05-31
type: audit
tags: [smartbrain, b2b, b2b-core, multi-tenant, code-review, deuda-tecnica, korean-root, smart-foods]
status: saneado-tier0-3-deployado
derivado_de: b2b-shared-core-submodule
---

> **ACTUALIZACIÓN 31 may 2026 — Tier 0, 1, 2 y 3 cerrados; core en `b5bf0bd`, deployado y verificado en ambos VPS.**
> - **Tier 0** (des-hardcodear + 2 bugs activos + sacar skills muertos del core) → HECHO.
> - **Tier 1** (3 crashes TS + react-dom/router peer+dedupe + ErrorBoundary) → HECHO.
> - **Tier 2** (aislamiento brand_id) → DESCARTADO: el aislamiento es FÍSICO (`_resolve_db_path` da DB por tenant, sin contaminación verificada). Parchar ~130 queries era redundante. El hardening real (fail-closed) es host-level, para el Content Hub futuro.
> - **Tier 3** (frontend 100% por `@host/api`, `host_contract.py`, `module.json` tables) → HECHO.
> - Verificado: SF `/b2b` en browser (cero errores), KR backend (endpoints 422). Detalle del proceso en memoria `project_b2b_shared_core.md`.

# Auditoría `b2b-core` — panel de 4 revisores (31 may 2026)

> Review arquitectónico del paquete compartido `b2b-core` (submódulo git consumido por SF y KR), hecho con 4 agents especializados en paralelo (architect, frontend-developer, typescript-reviewer, python-reviewer) sobre el código en `c06c7e1`.
>
> **Gatillo:** Andrés preguntó si estaba usando los skills de arquitectura. No los estaba usando — había cantado "robusto/nivel McKinsey" tras verificar solo *build verde + render*. El panel destapó deuda crítica que esa verificación no podía ver.

## Veredicto consolidado: RIESGOSO

3 de 4 revisores dijeron **RIESGOSO** (arquitectura, TypeScript, backend); 1 dijo **ACEPTABLE-CON-RESERVAS** (frontend). Consenso: el core **compila y renderiza pero NO es portable ni aislado**. Funciona hoy solo porque SF y KR son "gemelos"; el primer cambio asimétrico o un 3er tenant lo quiebra.

**Causa raíz:** "KR canónico" se extrajo *fiel* — con los hardcodes de KR y su config de un solo tenant adentro. La base estructural (submódulo compartido) está OK; faltó **sanear el contenido**.

**Mitigante:** el B2B todavía NO está activo en producción → cero daño hoy, estamos a tiempo de arreglarlo antes de activarlo.

---

## Hallazgos por tier de prioridad

### Tier 0 — Rompe SF apenas se active el B2B (barato, alto impacto)
Hardcodes de tenant en código compartido (verificado por grep):
- `backend/routers/crm.py:707,712` — outreach firmado **"Andres de Korean Root"**.
- `crm.py:733` — **"compra minima es $360,000"** (mínimo de KR).
- `crm.py:858` — `filename = "koreanroot_leads_klaviyo.csv"`.
- `crm.py:2124` — `https://srv1319033.hstgr.cloud/crm` hardcodeada en endpoint público `/lead-form`.
- `crm.py:2642` — `brand_id = user.get("brand_id", "korean-root")` (fallback peligroso → debe fallar, no asumir tenant).
- `crm.py:205,209,289,330,2113` + `meetings.py:245` — assignees `"andres"/"florencia"` hardcodeados.
- `skills/b2b_prospecting/b2b_config.py` — **100% KR**: ICP K-beauty "mujeres 34-55", zonas CABA/GBA, competidores KR (cosrx, innisfree). Viola el README del propio core ("never shared: brand_context").
- `skills/outreach_engine/message_builder.py:79`, `outreach_main.py`, `gemini_qualifier.py:89,107` — prompts de Gemini dicen "Korean Root".
- **Fix:** todo string de marca/monto/URL/assignee → `brand_context` (`GET /api/brand/prompt-context`). Sacar `b2b_config.py` del core (per-tenant en cada VPS; `prospecting.py` ya hace `importlib.reload` correcto, solo cambia la ubicación del archivo).

### Tier 1 — Próximos crashes tipo Sidebar (latentes, garantizados con datos)
- `frontend/components/crm/ClassifyView.tsx:34` — `l.zona.toLowerCase()` con `zona` tipada `string` pero null en runtime (lead importado sin zona). `types/crm.ts:10` miente.
- `frontend/Crm.tsx:59,587+` — `miDiaData: any`; `/crm/mi-dia` con `followups: null` o `landing_visitors: null` → `.map()` crashea.
- `frontend/components/crm/SalesView.tsx:133-138` — `k!.revenue_current` (non-null assertion) si `analytics.kpis` es null.
- `frontend/package.json` — **`react-dom` NO está en peerDependencies** (solo devDeps); **`react-router-dom` falta del `dedupe`** en `CONSUMING.md:19`. Mismo linaje del crash Sidebar (doble instancia React/Router).
- `frontend/components/crm/UnifiedSequenceWizard.tsx:1` — `// @ts-nocheck` (componente entero fuera del typechecker).
- Cero `ErrorBoundary` en todo el árbol → un undefined blanquea toda la sección `/b2b`.
- **Fix raíz (TS):** el stub `@host/api` defaultea `T = any` → cada `get<T>()` es fe sin validación. Quitar el default + schema validation runtime (zod) en los 5-6 tipos de mayor riesgo (`CrmLead`, kanban, `mi-dia`, `Analytics`, `Customer`). Tipar honesto los campos nullable. Error boundary por tab.

### Tier 2 — Aislamiento multi-tenant (deuda, hoy no explotable)
- `backend/routers/crm.py` — `brand_id = user["brand_id"]` se asigna y **nunca se usa en el WHERE** en `list_leads:366`, `mi-dia:571`, `metrics:1426`, `outreach-messages:669`, `filter-options:758`, `deduplicate:2276`, `auto-merge:2509`, y todas las escrituras por ID (PUT/DELETE/bulk). Solo `/kanban` filtra.
- `create_lead:875` — INSERT lista `brand_id` en columnas pero (según python-reviewer) faltaría en los valores → NULL/error. **VERIFICAR antes de afirmar.**
- `_create_task:156` — tasks con `brand_id = None`.
- `zona_mapping.py:117` — `UPDATE crm_leads SET zona ... WHERE zona = ?` sin `brand_id`.
- **Hoy NO explotable** entre SF/KR (VPS separados, DB por archivo, `_resolve_db_path` request-scoped). Riesgo real: `specialandres` (mismo VPS que SF) y Content Hub multi-cliente futuro. El CEO brand-switch (`?brand_id=X`) cambia el archivo DB → ok hoy, pero el patrón inconsistente es bomba de tiempo.
- **Fix:** decidir el modelo explícito. Si DB-por-tenant: `_resolve_db_path` debe fallar cerrado + test. Si se quiere defensa en profundidad (enterprise): `AND brand_id = ?` en TODA query + guard que rechace queries sin scope.

### Tier 3 — Deuda arquitectónica
- **Contrato backend ficticio:** routers hacen `from db/config/deps/wa_notify/blacklist import ...` (26 imports top-level del host, no documentados en CONSUMING.md ni module.json). El core asume que el host expone esos módulos con firmas exactas. **Fix:** `backend/host_contract.py` (Protocol/stub) análogo a `@host/api`.
- **Frontend bypasea el contrato:** `SalesView.tsx:734`, `CustomersTab.tsx:189`, `ImportModal.tsx:70` usan `fetch` directo + `localStorage.getItem('sb_token')` + ruta `/api/` absoluta. Si otro tenant usa otro key/base-url, quedan sin auth/404. **Fix:** todo por `@host/api` (agregar `download()` al contrato).
- **Endpoints fuera del core:** frontend llama `/sales/orders|product-costs|analytics|margins` que NO existen en routers del core (viven en el host) + `/zona-mapping` (singular) vs `/zona-mappings` que sirve `zona_mapping.py` → bug latente. **Fix:** documentar el contrato de API completo (endpoints + shapes) o mover `/sales/*` al core.
- **`module.json` prefix+attr = curita:** los routers ya declaran prefix en código (`APIRouter(prefix="/api/crm")`); `module.json` los pone en `""`. Dos loaders divergentes (`prefix` vs `attr`) permiten que las rutas diverjan entre VPS silenciosamente. **Fix real: unificar los `module_loader.py`** (extraer a `core` compartido o mínimo leer las mismas claves).
- **Submódulo sin versionado de schema:** `module.json` dice `tables: []` pero el core depende de ~14 tablas (`crm_leads`, `crm_interactions`, `customers`, `orders_b2b`, `wa_*`, etc.). `prospecting.py:248` ya tiene `except CHECK constraint failed` parcheando drift de schema en runtime. **Fix:** declarar tablas + `MIGRATIONS.md` con orden de migración que cada host corre ANTES de mover el pin del submódulo; `core_version` que el host loguee al arrancar; CI (`tsc --noEmit` + import-check backend) en ambos hosts antes de mover el pin.
- **Submódulo vs paquete publicado:** para 2 tenants internos, submódulo es defendible. Para 3+ o clientes externos (Content Hub SaaS), migrar a paquete versionado (npm privado front + wheel back) con semver.

### Detalles BAJO (no bloqueantes)
- N+1 requests: `LeadCard.tsx:47` dispara `GET /crm/leads/{id}/wa-status` por card → 200+ requests al montar el kanban. Mover a campo en la respuesta del kanban o batch.
- `del` como nombre de export del contrato (reservado en Python, borde en JS) → renombrar.
- `key={i}` en listas reordenables (`CustomersTab.tsx:341,394,507`).
- `prompt()/confirm()/alert()` (36 ocurrencias) → modales controlados.
- `import os` duplicado + docstring tras código + `brand_id` redeclarado 2x en ~20 funciones de `crm.py`.

---

## Plan recomendado (orden)
1. **Tier 0** antes de activar B2B en SF — des-hardcodear marca/montos/URL/assignees + sacar `b2b_config.py` y prompts del core a `brand_context`/per-tenant.
2. **Tier 1** — blindar los 3 crashes TS + `react-dom`/`react-router-dom` en peer+dedupe + Error Boundaries + quitar `@ts-nocheck`.
3. **Tier 2** — decidir modelo multi-tenant + `_resolve_db_path` fail-closed; `brand_id` consistente si se quiere defensa en profundidad.
4. **Tier 3** — contrato backend explícito, unificar loaders, versionar schema + migraciones, frontend 100% por `@host/api`.

**Pendiente de verificar antes de afirmar:** el INSERT de `create_lead` (19 cols vs 18 valores) — si es bug activo, sube a Tier 0.

Relacionado: [[b2b-shared-core-submodule]], [[wizard-outreach-multitenant]].
