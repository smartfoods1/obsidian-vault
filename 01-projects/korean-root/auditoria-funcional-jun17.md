---
date: 2026-06-17
type: auditoria
tags: [korean-root, smartbrain, auditoria-funcional, bugs, qa]
status: activo
relacionado: [[auditoria-arquitectura-smartbrain]]
---

# Auditoría funcional SmartBrain Korean Root — qué NO funciona + contraste

> QA sistemático (jun 17 2026). Se testearon **351 endpoints GET** con JWT CEO + se verificó contraste en **16 páginas** (todas las secciones) + consola JS + estado de integraciones/servicios. **Ninguno de los problemas fue causado por el trabajo de refactor/rediseño** — todos son preexistentes (bugs de DB/código o credenciales externas).

## 0. ESTADO POST-FIX (jun 17, después de "arreglá todo")
**Antes:** 273/351 OK, **14 endpoints 5xx (rotos)**. **Ahora:** **281/351 OK, 0 errores hard (500/502)** — los 8 bugs de código/DB arreglados; los 4 restantes degradan con 503 limpio (dependen de creds/infra externas).

**Bugs ARREGLADOS:**
- `analytics/customers,trends,cohorts` — bug `+ cf_p` (params SQL concatenados a valores) ×4. ✅
- `retention/stats,campaigns,campaigns/{id}` — faltaban columnas en `ecom_retention_recipients` (converted, customer_name, phone, error_message, preferred_product) + `_rows([None])` no guardaba el 404. ✅
- `b2c/sync-status` — faltaba `get_sync_status` en el stub `shopify_sync.py`. ✅
- `templates/sync-all` — INSERT con 9 columnas y 8 valores (faltaba `brand_id`). ✅
- `chatbot/flows/{id}/steps` — faltaba columna `orden` en `chatbot_steps`. ✅
- `/mayorista` — abría un HTML inexistente; ahora redirige a `/mayoristas/` (landing real). ✅
- `journey-proxy` — NO estaba roto: el webhook WA lo maneja la API (nginx→8080); el unit es legacy obsoleto (script inexistente), se dejó stopped. ✅

**Degradan con gracia (503, NO crashean) — requieren acción del cliente:**
- `wa-web/*` — servicio Baileys (8787) no corre. KR usa la API oficial de WA, no Baileys → vestigial. Para activarlo: levantar Baileys + chip.
- `canva/authorize` — falta `CANVA_CLIENT_ID` (Canva no conectado).

Backups: `/root/kr_codefix_bak/` (4 archivos) + `/root/kr_db_bak_*.db` (DB pre-migración).

## 1. Resumen original de la auditoría (pre-fix)
- **Endpoints:** 273/351 OK · 18 auth/validación · **14 dan 5xx** · 2 timeouts → **resuelto, ver §0**.
- **Integraciones:** Tiendanube ✅ y WhatsApp Cloud API ✅; **Instagram ❌ y Google Sheets ❌ desconectadas** (creds).
- **Contraste:** ✅ adecuado en las 16 páginas verificadas, sin errores de consola.
- **Causadas por el refactor:** **0**.

## 2. Endpoints ROTOS (5xx) — causa raíz

| Endpoint | Código | Causa raíz | Tipo |
|---|---|---|---|
| `/api/retention/stats` | 500 | `sqlite3: no such column: converted` | **DB schema** |
| `/api/retention/campaigns` | 500 | `sqlite3: no such column: r.converted` | **DB schema** |
| `/api/analytics/customers` | 500 | `TypeError: can only concatenate str (not "list")` | **Bug código** |
| `/api/analytics/trends` | 500 | `TypeError: unsupported operand +: float y list` | **Bug código** |
| `/api/analytics/cohorts` | 500 | `TypeError: ...str (not "list")` | **Bug código** |
| `/api/b2c/sync-status` | 500 | `ImportError: cannot import 'get_sync_status' from shopify_sync` (stub) | **Bug código** |
| `/api/templates/sync-all` | 500 | `sqlite3.ProgrammingError: bindings 9 vs 8` | **Bug SQL** |
| `/mayorista` | 500 | `FileNotFoundError: backend/static/mayorista.html` (legacy; landing real = `/mayoristas/`) | **Archivo falta** |
| `/api/canva/authorize` | 500 | Canva OAuth (config/creds) | **Config** |
| `/api/wa-web/qr` `/screenshot` `/bulk-status` | 502 | Servicio wa-web (upstream) caído | **Infra WA** |
| `/api/b2c/segments/detailed` | timeout | Query pesada/colgada | **Performance** |
| `/api/tiendanube/orders` | timeout | Query pesada/colgada | **Performance** |

> Los **3 grupos de "bug código"** (analytics TypeError, b2c ImportError, templates SQL) son arreglables sin tocar DB. Los de **DB schema** (retention `converted`) requieren una migración/ajuste de query. Los de **infra/cred** (wa-web, canva, IG) requieren servicio o credenciales.

## 3. 404s — mayormente FALSOS POSITIVOS
Los 43 "404" del sweep son casi todos rutas `{id}` testeadas con `id=1` inexistente (ej. `/api/crm/leads/1`, `/api/salto-cuantico/portal/1`) → 404 es correcto (el recurso no existe). No son bugs.

## 4. Integraciones (Settings → Integraciones)
- ✅ **Tiendanube** — Conectado (órdenes/productos/stock).
- ✅ **WhatsApp Cloud API (Meta)** — Conectado (pero el servicio receptor `journey-proxy` está caído, ver §5).
- ❌ **Instagram (Graph API)** — Desconectado (faltan `IG_USER_ID`/`IG_ACCESS_TOKEN`). Bloquea publicación de contenido.
- ❌ **Google Sheets** — Desconectado (reportes/pipeline).

## 5. Servicios / infra
- `smartbrain-api` (8080): **active** ✅, 0 errores de boot, todos los routers cargan.
- `journey-proxy` (bot WhatsApp): **inactive** ❌ — inbound WA no se procesa. (Ver [[project_kr_wa_token_dead]].)
- **Token de Meta Ads vence en ~6 días** — renovar pronto (el sistema lo alerta correctamente).

## 6. Contraste — VERIFICADO ✅
16 páginas verificadas en vivo (browser), todas tier-1 light, texto legible, botones correctos, sin errores de consola:
Cerebro · Ecommerce · Analytics(+gráficos) · B2B(kanban+modal) · Campañas · Operaciones · Conversaciones/Inbox · Salto Cuántico · Content · Inteligencia · Meta Ads · Retención · Settings · Login.
Submódulo `b2b` convertido a tokens `var()` tenant-safe (light en KR, oscuro en SF). Sin issues de contraste detectados.

### 6.1 Barrido sistemático de texto faint (jun 17, post-screenshot CEO)
El CEO reportó "no veo el contraste" en **Campañas**. Causa raíz: `const MUTED = "#E6E9EE"` (color de **borde** casi blanco) usado como **color de texto** en labels/subtítulo de `UnifiedCampaigns.tsx` → invisible. Fix: `MUTED = "#64748B"` (slate legible). El título (#0F172A) y botones (índigo #4F46E5) ya estaban bien — lo que el CEO veía clarísimo/rosa era **cache viejo del browser**.

Tras eso, barrido programático (`/tmp/kr_faint_scan.py`) de **todo el frontend** buscando hex claros usados como `color:` de texto. **55 reemplazos en 7 archivos:**
- `BotLearningTab.tsx` + `SmartChallengeTab.tsx` — tema dark mal convertido: texto `#f1f5f9` (casi blanco) sobre fondo `#FFFFFF`/`#F7F8FA` + bordes `#FFFFFF` invisibles → `#0F172A` + bordes `#E2E8F0`. **(luego borrados, ver §8 — eran dead code)**
- `ProposalsTab.tsx` (8) + `WizardPlanQuincenal.tsx` (3) — `#E6E9EE` como texto → `#475569`.
- `Content.tsx` — placeholder `#E6E9EE` → `#94A3B8`; botón "Guardar LinkedIn" lime `#a3e635`+texto blanco (contraste ~1.25:1) → índigo `#4F46E5`.
- `SmartBotAnalytics.tsx` — texto "Cliente:" `#e5e7eb` → `#334155`.
- `InspirationTab.tsx` — 2 placeholders `#E6E9EE` → `#94A3B8`.

Re-scan final: 0 bugs reales. Los 28 hits restantes son `color: '#F7F8FA'` (blanco) sobre **botones de color** (ACCENT índigo, slate, scoreColor) → correctos. Build verde, verificado en vivo (Campañas + Contenido).

## 9. Feedback de Jorge + fixes (jun 17, tarde)

Jorge (CEO KR) reportó 3 bugs + Andrés sumó 2 temas. Diagnóstico read-only (4 agentes paralelos) + fixes aplicados y verificados. Backups en `/root/kr_fix3_bak/`.

**1. Login (no le llega el OTP) → era MUCHO más grave.** Hallazgo: el dashboard tenía `ENABLE_DEV_BYPASS=true` + `ENVIRONMENT=staging` en `.env` → **aceptaba cualquier código OTP para cualquier teléfono registrado** (login abierto en prod) + un `11111` compartido hardcodeado. El "OTP no llega" era un distractor (el send es texto libre, WhatsApp lo rechaza fuera de 24h). **Fix:** auth por **password bcrypt por usuario** (`brand_users.password_hash`), bypass apagado, `11111` eliminado, frontend con input de contraseña. Verificado: password correcta→token, incorrecta→400. Detalle en `[[project_kr_auth_security]]`.

**2. Marketing "ya generadas".** El guard de `/generate` Q2 contaba una propuesta mensual legacy (id=23, Win-Back del cron `motor-retencion`) que la vista Q2 no muestra → 409 invisible. **Fix:** guard alineado al listado (Q2 choca solo con Q2). NO se archivó id=23 (materializó 3 campañas draft reales).

**3. Plantillas B2B no cambian.** Las ediciones de Vicky se guardan pero el envío usaba textos hardcodeados (`crm.py outreach_messages`). **Fix:** el builder ahora lee la plantilla editable (fallback `generico`). Ojo: categorías de plantilla ≠ tipos de lead reales → casi todo cae a `generico` (Vicky debe editar esa). Pendiente: alinear categorías.

**4. Token WA en DB.** `canal_config.access_token` era duplicado idéntico del de `.env`. Removido (cae a `.env`, cero cambio).

**5. Número de Vicky / Natalia.** El nº de Vicky es solo login, no bot. Natalia llegó al bot, que derivó a humano por diseño (consulta de pago → handoff `+54 9 342 545-5846`). Decisión: dejar handoff así. Problema real = checkout de Tienda Nube sin opción "transferencia" → **Victoria en panel TN**.

## 8. Limpieza de dead code — CRM legacy huérfano (jun 17)
Al barrer contraste se detectó que `frontend/src/components/crm/` es una **copia legacy del CRM** superada por el submódulo `@b2b/Crm` (lazy `import('@b2b/Crm')` en `App.tsx`). De 12 archivos, **11 tenían 0 referencias vivas** (chequeo de cierre incl. transitivos y el paquete b2b):
`BiferiaLeads, BotConfigTab, BotFlowDiagram, BotLearningTab, InboxTab, JourneysView, LandingAnalytics, OutreachView, SmartChallengeTab, TemplatesTab, WhatsAppConfig`.
Único vivo: `CampaignsTab.tsx` (← `pages/UnifiedCampaigns.tsx`). Los 11 borrados (backup en `/root/kr_deadcrm_bak/`), build verde, bundle del CRM real intacto (296 kB sin cambios). Menos laberinto, menos doble función.

## 10. Ecommerce + Retención — orden y limpieza (jun 17, tarde)

**"50 recuperados" vs "Aún sin envíos":** era un MISCOUNT, no data fantasma. `retention_engine.py` contaba como recuperados a cualquiera del segmento dormido que recompró desde el 08/06 sin verificar envío (el holdout, que no recibe nada, también marcaba 8). El motor todavía no envía (`retention_contact_log` y `ecom_retention_recipients` en 0). **Fix:** gateado con `measuring = contact_log_entries > 0` → sin envíos, recuperados/revenue/lift = 0; frontend muestra "—". Verificado en vivo. Pendiente futuro: poblar `retention_contact_log` cuando se activen envíos.

**Tab "Inteligencia" de Ecommerce → eliminado.** Heatmap de cohortes leía `ecom_intelligence_cache` que ningún job llena; el bloque RFM era duplicado roto del tab Segmentos. 4 ediciones en `Ecommerce.tsx`.

**Submódulo "Acciones" → eliminado.** Stub "se movió a Marketing", sin ruta ni backend. Borrado limpio + repunté el cross-link obsoleto de `SmartBotCampaigns.tsx` a `/retention`. NO se tocó el botón de campañas del tab Segmentos (feature viva).

**Verificado en vivo:** Ecommerce queda con 5 tabs (Overview/Clientes/Segmentos/Pedidos/Productos), Overview con datos reales + RFM correcto; Retención coherente ("—" recuperados, "Aún sin envíos"). Build verde. Backups en `/root/kr_fix4_bak/`.

**Deuda anotada (no tocada, riesgo):** `ecommerce.py` y `ecommerce_tn.py` registran ambos `/api/ecommerce` con rutas idénticas (shadowing; para KR/TN debería servir `ecommerce_tn.py`). `/api/analytics/cohorts` tira 500 pero ningún UI lo consume. Resolver el shadowing = tarea aparte (verificar endpoint por endpoint).

## 7. Recomendaciones (prioridad)
1. **Arreglables por código (rápido, alto valor):** analytics customers/trends/cohorts (TypeError list/str), b2c/sync-status (ImportError del stub Shopify), templates/sync-all (SQL bindings). → Funciones de analytics y sync que hoy fallan.
2. **DB:** retention stats/campaigns (`no such column: converted`) — revisar el query vs el schema de la tabla de retención en `ops_korean-root.db`.
3. **Performance:** b2c/segments/detailed y tiendanube/orders (timeout) — paginar/indexar.
4. **Credenciales/infra (cliente):** reconectar Instagram + Google Sheets; levantar `journey-proxy`; renovar token Meta Ads.
5. **Legacy:** `/mayorista` (singular) está roto y es redundante con `/mayoristas/` (nginx) — borrar el endpoint legacy de `catalog.py`.
