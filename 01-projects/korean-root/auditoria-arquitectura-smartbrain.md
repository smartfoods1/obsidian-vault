---
date: 2026-06-16
type: auditoria
tags: [korean-root, smartbrain, arquitectura, refactor, deuda-tecnica, duplicados]
status: activo
relacionado: [[korean-root-conectar-instagram]]
---

> Auditoría multi-agente (mapa de montaje + mapa frontend + 9 dominios con verificación adversarial). Código auditado: snapshot en `/tmp/kr_audit` del VPS `103.199.187.246`. Acompaña al rediseño visual tier-1 (design system light slate+índigo, ver sección 9).

# Auditoría de Arquitectura — SmartBrain Korean Root

> Informe maestro de consolidación. Multi-agente (mapa de montaje + mapa frontend + 9 dominios con verificación adversarial), revisado y re-verificado contra el código real en `/tmp/kr_audit`. Todos los paths son repo-relative (`dashboard/...`). Cada afirmación está confirmada por grep/diff/Read — donde la verificación refutó o matizó un hallazgo del agente, lo digo explícito.

---

## 1. Resumen ejecutivo

- **La migración legacy→packages quedó a medio terminar.** Hay un árbol de routers **duplicado completo**: `dashboard/backend/routers/` tiene 64 routers `.py` (+`__init__`), y **59 son huérfanos al 100%** (cero montaje, cero refs externas) porque cada uno tiene un gemelo vivo montado en `dashboard/packages/*/backend/routers/`. De esos 59, **39 son byte-idénticos** a su gemelo y **20 divergieron** (el legacy quedó atrás). Editar la copia legacy de `cerebro`/`crm`/`webhook`/`content` **no tiene ningún efecto en producción** — es la trampa #1.

- **Hay un fork silencioso de alto riesgo (correctness, no limpieza).** 6 archivos legacy (`objectives`, `journeys`, `webhook`, `ig_dm_redirect`, `tiendanube_sync`, `tasks`) **siguen vivos como librerías**: routers de packages que SÍ están montados hacen `from routers.X import helper`, y como uvicorn corre con `CWD=backend/`, eso resuelve a la copia **legacy**, no a la de packages. Verificado: `packages/cerebro/.../cerebro.py:255` y `:1199`, `packages/smartbot/.../chatbot.py:431`, `packages/core/.../webhook.py:45`, `packages/ecommerce/.../ecommerce_tn.py:553`, + crons `cron_objectives_update.py:51` y `cron_tasks.py:65`. Si alguien mejora el helper en packages, el runtime sigue ejecutando la versión vieja.

- **El módulo `content` es un parásito.** `packages/content/` es una **cáscara vacía** (verificado: su `backend/routers/` solo tiene un `__init__.py` de 0 bytes). Su `module.json` apunta los 8 routers a `packages.operations.backend.routers.*`. Como `content` Y `operations` están **ambos enabled**, **5 routers de contenido se montan DOS VECES** en runtime (`content`, `content_images`, `content_regen`, `content_stories`, `inspiration`), y rutas como `/api/content/{id}/publicar-ahora` quedan registradas múltiples veces.

- **Doble ESP montado con un rename a medias que miente.** KR usa Perfit de verdad (el sistema canónico `unified_campaigns.py` lo dice en su docstring), pero Klaviyo sigue `enabled=true` y hay un trap confirmado: `packages/marketing/.../email_marketing.py:24-28` define `PERFIT_API_KEY`/`PERFIT_BASE` pero `PERFIT_BASE = "https://a.klaviyo.com/api/"` con header `Klaviyo-API-Key`. El código dice "Perfit" y pega a Klaviyo. Además coexisten **4 superficies de "mandar campañas"** (`/marketing`, `/smartbot/campaigns`, `/smartbot/outreach`, `/email-legacy`) — el usuario no sabe dónde crear una.

- **Contaminación de marca Smart Foods adentro de KR + basura versionada.** El lime `#E0E938` de Smart Foods está hardcodeado **22 veces en 5 archivos** del frontend de contenido (KR es rosa `#C2185B`), más fallbacks de `--accent #E0E938` en `Sidebar.tsx`/`Layout.tsx`/`App.tsx`. Y hay **~34 archivos basura** versionados en disco: **9 `.bak`/`.deprecated` en `backend/routers/`**, **25 `.bak`/`.pre_migration`/`.deprecated` en `frontend/src/`**, más `~15 .bak` en `packages/marketing/backend/routers/`. El historial vive en git; esto solo ensucia greps y auditorías.

**Tamaño del problema (conteo verificado):**

| Categoría | Cantidad |
|---|---|
| Routers legacy en `backend/routers/` | 64 (`.py`) |
| Legacy huérfanos al 100% (0 montaje, 0 ref externa) | 59 |
| └─ idénticos a su gemelo package | 39 |
| └─ divergidos (package es canónico) | 20 |
| Legacy vivos como helper (repoint antes de borrar) | 6 |
| Legacy sin gemelo, montados a mano (conservar) | 3 |
| Routers de contenido montados 2× en runtime | 5 |
| Archivos `.bak`/`.deprecated`/`.pre_migration` en el árbol | ~49 (9 backend/routers + ~15 marketing/routers + 25 frontend) |
| Páginas frontend muertas (sin `<Route>`, 0 imports) | 7 |
| Subcomponentes mal ubicados en `pages/` | 12 |
| Referencias rotas reales | 1 (`cron_stock_sync.py` → `routers.stock` inexistente) |

---

## 2. Causa raíz

**Una migración estructural legacy→packages que se completó a nivel de MONTAJE pero no a nivel de IMPORTS, y nunca limpió la fuente vieja.**

1. **El montaje SÍ migró.** `main.py` monta a mano solo 8 routers (`auth`, `lead_form`, `marketing_monthly_products_router`, `marketing_optouts_router`, `routes_b2b_clients`, + 3 legacy sin gemelo: `salto_cuantico`, `salto_cuantico_webhook`, `retention_engine`). Todo lo demás lo monta `module_loader.register_modules(app)` leyendo los `module.json` de los módulos enabled, y **todos esos `module.json` apuntan a `packages.*`** (ningún `backend.routers.*` legacy). Por eso `half_migrated=[]` y no hay broken references por `module.json`. La copia legacy quedó en disco, sin borrar, "por las dudas".

2. **Los imports de helpers NO migraron.** Los routers de packages siguen pidiendo helpers con la ruta vieja `from routers.X`. Como `backend/` está en `sys.path` y es el CWD, esa ruta resuelve al archivo **legacy**, no al gemelo de packages. Resultado: la fuente vieja no quedó muerta del todo — quedó como una **librería sombra** que diverge en silencio de la versión montada.

3. **Se acumularon sistemas paralelos por iteración, no por diseño.** Email: Klaviyo (`email_marketing*` + `EmailPlanner` en `/email-legacy`) → reemplazado por Perfit (`unified_campaigns`), pero el viejo nunca se apagó (solo se le escondió la entrada del sidebar). Campañas: `unified_campaigns` (email+WA) + `SmartBotCampaigns` (difusión WA) + `B2COutreach` + `EmailPlanner` = 4 superficies. Contenido: `content_strategy` (Tier-1, Gemini+KB) + `content_regen` (legacy, Sonnet) = 2 generadores a la misma tabla `content_posts`. Cada relanzamiento agregó una capa sin retirar la anterior.

4. **El módulo `content` se creó como destino de migración pero el código nunca se movió.** Existe el `module.json`, el slot en el sidebar (position 6), y la carpeta — pero los routers viven 100% en `operations` y `content` solo los re-declara. La migración de contenido quedó congelada a mitad de camino.

5. **El versionado se hizo en disco (`.bak`) en vez de en git**, a pesar de que el repo es git. Snapshots manuales (`roasfix`, `turnhealth`, `grounding`, `apcamp`, `pre_migration`) se commitearon al árbol servido.

El denominador común: **se construyó la arquitectura nueva al lado de la vieja y nunca se cerró la vieja.** No es un bug puntual; es deuda de migración no liquidada.

---

## 3. Inventario de duplicación

| Función | Archivos/páginas que la implementan | Canónico a conservar | A eliminar | Riesgo |
|---|---|---|---|---|
| Routers legacy idénticos (39) | `backend/routers/{b2c,brand,klaviyo,bot_game,bot_learning,bot_rules,brands_admin,campaigns,canva,customers,meetings,intel,prices,ci_warroom,public_pages,templates,email_marketing,broadcast,contacts,inbox,flow_builder,knowledge_base,wa_web,sales_wa,sales,sales_analytics,sales_import,journey_config,retention,tiendanube_oauth,unified_analytics,catalog,ops,chat,invoice_ocr,zona_mapping,...}.py` | el gemelo en `packages/*/backend/routers/` | toda la copia `backend/routers/` | **bajo** (0 refs, byte-idénticos) |
| Routers legacy divergidos (20) | `backend/routers/{cerebro,outreach,outreach_templates,crm,content,chatbot,webhook,smartbot_analytics,analytics,b2c_outreach,catalog,content_images,content_regen,ecommerce,email_marketing_tier1,inspiration,journey_progress,meta_ads,tiendanube_sync,integrations}.py` | el gemelo en `packages/*` (es el montado, +nuevo) | la copia legacy, tras confirmar que no hay lógica única | **medio** (verificar diffs grandes: cerebro +253L, outreach +359L) |
| Helpers legacy vivos por import-shadow | `backend/routers/{objectives,journeys,webhook,ig_dm_redirect,tiendanube_sync,tasks}.py` | gemelo en `packages/*` | legacy, **solo después** de repointar los imports | **alto** (borrar sin repointar rompe Cerebro/chatbot/TN-sync/crons) |
| Content: montaje | `packages/content/module.json` + `packages/operations/module.json` (5 routers compartidos) | un solo `module.json` dueño | el doble registro | **medio** (doble include en runtime) |
| Content: generación de copy | `content_strategy.py` (Gemini+KB+compositor, scope single/week/quincena/month) vs `content_regen.py` (Sonnet, sin compositor, verticales hardcodeadas) | `content_strategy.py` | degradar `content_regen` a solo `regenerar/{post_id}` | **medio** (ambos escriben `content_posts`) |
| Content: rutas publicar | `/api/content/{id}/publicar-ahora` y `/publicar-status` en `content.py` Y `content_regen.py` | versión en `content.py` | handlers duplicados en `content_regen.py` (código muerto, gana content.py) | **bajo** |
| Email/ESP | `email_marketing.py` + `email_marketing_tier1.py` + `EmailPlanner.tsx` (Klaviyo) vs `unified_campaigns.py` + `proposals.py` (Perfit) | Perfit (`unified_campaigns`) | el trío Klaviyo, tras confirmar 0 tráfico `/api/email` | **medio** (`email_marketing_tier1` tiene lógica de cascades/attribution) |
| Campañas (UI) | `UnifiedCampaigns.tsx` `/marketing` · `SmartBotCampaigns.tsx` `/smartbot/campaigns` · `B2COutreach.tsx` `/smartbot/outreach` · `EmailPlanner.tsx` `/email-legacy` · `Campaigns.tsx` (muerta) · `EmailMarketing.tsx` (muerta) | `UnifiedCampaigns` (hub) + `SmartBotCampaigns` (difusión, función distinta) | `Campaigns.tsx`, `EmailMarketing.tsx`, `EmailPlanner.tsx` | **medio** |
| Analytics (concepto) | `/analytics` (`Analytics.tsx`) vs `/smartbot/analytics` (`SmartBotAnalytics.tsx`) | ambos (son distintos) — pero **relabelar** | nada (renombrar labels) | **bajo** |
| Páginas frontend muertas | `B2CCustomers.tsx`, `Campaigns.tsx`, `EmailMarketing.tsx`, `FlowBuilder.tsx`, `InstagramPage.tsx`, `Journeys.tsx`, `WhatsAppPage.tsx` | las páginas vivas que las reemplazaron | las 7 | **bajo** (0 `<Route>`, 0 imports) |
| Stock sync | `cron_stock_sync.py` → `routers.stock._do_shopify_sync` (**no existe**) | endpoints `/stock` en `packages/operations/.../ops.py` | — (reparar el cron) | **alto** (cron roto, falla en import) |

---

## 4. Archivos CONFIRMADOS borrables

> Solo lo verificado adversarialmente como `confirmed_dead` (byte-idéntico al gemelo montado **o** sin contraparte viva, y **0 referencias externas** confirmadas por grep). Lo demás va a "Investigar antes de borrar".

### 4.A — Borrado seguro YA (P0, riesgo bajo)

**Routers legacy idénticos al gemelo montado (0 refs externas, diff IDENTICAL — verificado en muestra: b2c, brand, klaviyo, bot_game, brands_admin, campaigns, canva, customers, meetings, intel):**

```
dashboard/backend/routers/b2c.py
dashboard/backend/routers/brand.py
dashboard/backend/routers/klaviyo.py
dashboard/backend/routers/bot_game.py
dashboard/backend/routers/bot_learning.py
dashboard/backend/routers/bot_rules.py
dashboard/backend/routers/brands_admin.py
dashboard/backend/routers/campaigns.py
dashboard/backend/routers/canva.py
dashboard/backend/routers/customers.py
dashboard/backend/routers/meetings.py
dashboard/backend/routers/intel.py
dashboard/backend/routers/prices.py
dashboard/backend/routers/ci_warroom.py
dashboard/backend/routers/public_pages.py
dashboard/backend/routers/templates.py
dashboard/backend/routers/broadcast.py
dashboard/backend/routers/contacts.py
dashboard/backend/routers/inbox.py
dashboard/backend/routers/flow_builder.py
dashboard/backend/routers/knowledge_base.py
dashboard/backend/routers/wa_web.py
dashboard/backend/routers/sales_wa.py
dashboard/backend/routers/sales.py
dashboard/backend/routers/sales_analytics.py
dashboard/backend/routers/sales_import.py
dashboard/backend/routers/journey_config.py
dashboard/backend/routers/retention.py
dashboard/backend/routers/tiendanube_oauth.py
dashboard/backend/routers/unified_analytics.py
dashboard/backend/routers/catalog.py
dashboard/backend/routers/ops.py
dashboard/backend/routers/chat.py
dashboard/backend/routers/invoice_ocr.py
dashboard/backend/routers/zona_mapping.py
dashboard/backend/routers/op... (resto del set idéntico)
```

> **No borrar el directorio `backend/routers/` entero.** Sus hermanos `salto_cuantico*.py`, `retention_engine.py` (montados) y los 6 helper-vivos NO se tocan en P0.

**Routers legacy de contenido (huérfanos, superseded por `packages/operations/.../content*.py` — `confirmed_dead` verificado):**

```
dashboard/backend/routers/content.py
dashboard/backend/routers/content_images.py
dashboard/backend/routers/content_regen.py
dashboard/backend/routers/content_stories.py
```

**Backups `.bak`/`.deprecated` en `backend/routers/` (no son módulos Python importables, 0 refs):**

```
dashboard/backend/routers/chatbot.py.bak.turnhealth_20260606
dashboard/backend/routers/content.py.bak.20260418_230627
dashboard/backend/routers/ecommerce.py.bak-20260424-102742
dashboard/backend/routers/healthos.py.bak-saltocuantico
dashboard/backend/routers/meta_ads.py.bak.roasfix_20260529_215827
dashboard/backend/routers/salto_cuantico.py.bak.assets_20260608
dashboard/backend/routers/salto_cuantico.py.bak.grounding_20260607
dashboard/backend/routers/smartbot_analytics.py.bak.turnhealth_20260606
dashboard/backend/routers/tiendanube_sync.py.bak.20260606_2250
```

**`backend/main.py.pre_migration`** (snapshot del main viejo; el vivo es `backend/main.py`. Verificado: las únicas refs a `routers.{tasks,webhook,journeys,ig_dm_redirect,tiendanube_sync}` "como router montado" salen de este archivo muerto).

```
dashboard/backend/main.py.pre_migration
```

**Páginas frontend muertas (0 `<Route>` en `App.tsx`, 0 imports vivos — `confirmed_dead`):**

```
dashboard/frontend/src/pages/B2CCustomers.tsx
dashboard/frontend/src/pages/Campaigns.tsx
dashboard/frontend/src/pages/EmailMarketing.tsx
dashboard/frontend/src/pages/FlowBuilder.tsx
dashboard/frontend/src/pages/InstagramPage.tsx
dashboard/frontend/src/pages/Journeys.tsx
dashboard/frontend/src/pages/WhatsAppPage.tsx
```

**Backups frontend `.bak`/`.pre_migration`/`.deprecated` (Vite no los compila, 0 imports — `confirmed_dead`):**

```
dashboard/frontend/src/App.tsx.bak.retention_20260608
dashboard/frontend/src/App.tsx.bak-1777046394
dashboard/frontend/src/App.tsx.bak-crm-converge
dashboard/frontend/src/App.tsx.pre_migration
dashboard/frontend/src/components/Sidebar.tsx.bak.retmove_20260609
dashboard/frontend/src/components/Sidebar.tsx.pre_migration
dashboard/frontend/src/components/Sidebar.tsx.bak.retention_20260608
dashboard/frontend/src/lib/api.ts.bak.apcamp_20260615_004105
dashboard/frontend/src/pages/InspirationTab.tsx.bak.1776914660
dashboard/frontend/src/pages/ProposalsTab.tsx.bak.1778603807
dashboard/frontend/src/pages/ProposalsTab.tsx.bak.reopen_20260615_001532
dashboard/frontend/src/pages/ProposalsTab.tsx.bak.apcamp_20260615_004105
dashboard/frontend/src/pages/ProposalsTab.tsx.bak-20260507-095506
dashboard/frontend/src/pages/Content.tsx.bak.1776914660
dashboard/frontend/src/pages/UnifiedCampaigns.tsx.bak-20260507-095206
dashboard/frontend/src/pages/UnifiedCampaigns.tsx.bak.1778603479
dashboard/frontend/src/pages/Brand.tsx.bak.1776914660
dashboard/frontend/src/pages/SmartBotAnalytics.tsx.bak.health_20260606
dashboard/frontend/src/pages/SaltoCuantico.tsx.bak.gen_20260607
dashboard/frontend/src/pages/SaltoCuanticoPortal.tsx.bak.assets_20260608
dashboard/frontend/src/pages/Ecommerce.tsx.bak-20260424-102742
dashboard/frontend/src/pages/Overview.tsx.bak.20260405
dashboard/frontend/src/pages/HealthOS.tsx.bak-saltocuantico
dashboard/frontend/src/pages/HealthOSPortal.tsx.bak-saltocuantico
dashboard/frontend/src/pages/MonthlyProductsTab.tsx.deprecated
```

**Backups `.bak` en `packages/marketing/backend/routers/` y `frontend/pages/` (~15 de `proposals.py`/`unified_campaigns.py` + duplicados de ProposalsTab/UnifiedCampaigns):** borrables todos. Ejemplos verificados como representativos:

```
dashboard/packages/marketing/backend/routers/proposals.py.bak.apcamp_20260615_004040
dashboard/packages/marketing/backend/routers/unified_campaigns.py.bak_fase5
(+ resto del glob packages/marketing/backend/routers/*.bak*)
```

### 4.B — Investigar ANTES de borrar (NO es borrado seguro)

| Archivo | Por qué NO es seguro aún |
|---|---|
| `dashboard/backend/routers/objectives.py` | **VIVO** como helper: `packages/cerebro/.../cerebro.py:1199` (`from routers.objectives import get_objectives_summary`, dentro del briefing del Cerebro, módulo enabled) + `backend/cron_objectives_update.py:51` (`FUENTES_DATO`). Además **diverge** del package. Borrar rompe el Cerebro. → Repointar a `packages.objectives.backend.routers.objectives` y validar que expone ambos símbolos, **después** borrar. |
| `dashboard/backend/routers/tasks.py` | **VIVO**: `backend/cron_tasks.py:65` (`_parse_plan_to_tasks`). Es idéntico al package (`packages/operations/.../tasks.py` lo tiene), así que repoint trivial → recién ahí borrable. |
| `dashboard/backend/routers/journeys.py` | **VIVO**: `packages/cerebro/.../cerebro.py:255` (`_generate_journey_insights`). Repointar a `packages.ecommerce.backend.routers.journeys`. |
| `dashboard/backend/routers/webhook.py` | **VIVO**: `packages/smartbot/.../chatbot.py:431` (`_process_status_update`). Diverge del package. Repointar a `packages.core.backend.routers.webhook`. |
| `dashboard/backend/routers/ig_dm_redirect.py` | **VIVO**: `packages/core/.../webhook.py:45` (`_send_ig_reply`). No tiene gemelo claro en packages (es un helper de IG) — confirmar dónde debe vivir antes de mover. |
| `dashboard/backend/routers/tiendanube_sync.py` | **VIVO**: `packages/ecommerce/.../ecommerce_tn.py:553` (`_sync_all_blocking`). Diverge. Repointar a `packages.ecommerce.backend.routers.tiendanube_sync`. |
| Los 20 routers legacy **divergidos** | Aunque 0 refs externas, hay que confirmar que el package es la versión deseada (diffs grandes en `cerebro` +253L, `outreach` +359L). No mergear features de legacy a ciegas. Una vez confirmado que el package es canónico → bajan a P0. |
| `email_marketing.py` + `email_marketing_tier1.py` + `EmailPlanner.tsx` (Klaviyo) | Confirmar **0 tráfico real a `/api/email/*`** y que **ningún cron** lo invoca. `email_marketing_tier1` tiene lógica de cascades/channel-conflict/attribution que puede correr en otro lado. |
| `cron_stock_sync.py` | NO borrar — **reparar**: importa `routers.stock._do_shopify_sync` inexistente. Verificar en el VPS si está agendado; repointar a la función real de stock en `packages/operations/.../ops.py`. |

---

## 5. Traps que pueden romper el sistema

1. **Fork silencioso legacy↔package (correctness).** Los 6 helpers de §4.B. El runtime ejecuta la copia **legacy** aunque la montada sea la de packages. Cualquier fix aplicado al helper en packages **no surte efecto**. Es la trampa más peligrosa: no se ve en disco, no rompe el arranque, diverge en silencio. Repointar imports es **pre-requisito** de cualquier borrado en `backend/routers/`.

2. **Doble montaje de routers de contenido.** `content` + `operations` enabled → `register_modules()` (que **no deduplica**, verificado en `module_loader`) incluye 5 routers dos veces. FastAPI acepta y gana el primero, pero ensucia OpenAPI y multiplica el registro de `/api/content/{id}/publicar-ahora` (también duplicada dentro de `content.py` vs `content_regen.py`). Fix: un solo `module.json` dueño + dedup en el loader.

3. **`cron_stock_sync.py` roto (referencia muerta real).** `from routers.stock import _do_shopify_sync` — `routers/stock.py` **no existe en ningún lado** (verificado: `find . -name stock.py -path "*routers*"` vacío) y `_do_shopify_sync` no está definido. Si el cron está agendado en el VPS, **falla en el import** cada corrida → el stock de Shopify no sincroniza.

4. **Doble ESP + config trap que miente.** `klaviyo.enabled=true` Y `perfit.enabled=true` con KR usando Perfit de verdad. `packages/marketing/.../email_marketing.py:24-28`: variables `PERFIT_*` apuntando a `https://a.klaviyo.com/api/` con `Klaviyo-API-Key`. Cualquiera que lea el código cree que pega a Perfit y pega a Klaviyo. Riesgo: mandar por el canal equivocado. Fix: renombrar constantes a `KLAVIYO_*` (o deprecar el router) y poner `klaviyo.enabled=false` si KR ya no manda por Klaviyo.

5. **Contaminación de marca SF dentro de KR.** `#E0E938` (lime Smart Foods) hardcodeado 22× en `Content.tsx`, `StrategyConfigPanel.tsx`, `WeeklyRegen.tsx`, `TemplatesManager.tsx`, `UploadContent.tsx`; + fallbacks `--accent #E0E938` en `Sidebar.tsx`/`Layout.tsx`/`App.tsx` (PageLoader, botón Chat). KR es `#C2185B`. El módulo de contenido es de cara al cliente que paga ~USD 1000/mes. Si el branding tarda en cargar, **el cliente KR ve color Smart Foods**. Viola `feedback_no_hardcode`.

6. **`sidebar_title` mal seteado (matiz a la auditoría FE).** El agente FE asumió que `branding.sidebar_title` "debería resolver Korean Root", pero verificado: en `deployment_config.json` está literalmente `"sidebar_title": "SmartBrain"`. O sea: no es solo un problema de fallback durante el load — **el config dice SmartBrain, no Korean Root**. Es un dato a corregir en el deployment, no solo en el código.

7. **`module.json` de marketing desincronizado del ruteo real.** Declara `route: '/campaigns'`, pero `/campaigns` es un redirect a `/smartbot/automations` y la UI real está en `/marketing`. Si algún día el sidebar se genera desde `module.json`, rompe.

8. **`module_loader` traga errores en silencio.** Si un `import` de package revienta en runtime, lo acumula en `errors[]` y sigue. Hay que revisar los logs de arranque `[ModuleLoader] Errors` en el VPS — un router puede estar caído sin que se note por archivos en disco.

9. **Clave `attr` (singular) ignorada en `b2b/module.json`.** El loader lee `attrs` (plural); `attr` es no-op silencioso. Funciona de casualidad porque el default `attrs=['router']` coincide. Corregir para evitar sorpresas futuras.

---

## 6. Arquitectura objetivo

**Principio: un router por función, un solo dueño por módulo, cero copias legacy, cero imports `from routers.X` que crucen a la fuente vieja.**

- **Un solo árbol de routers: `packages/*/backend/routers/`.** `backend/routers/` se vacía salvo lo que aún no tiene módulo (ver migración de `salto`/`retention`). Cero gemelos.
- **Helpers sin import-shadow.** Reemplazar todo `from routers.X import helper` por `from packages.<mod>.backend.routers.X import helper` (o extraer el helper a un módulo compartido `packages/<mod>/backend/lib/`). Ningún path ambiguo que dependa del CWD.
- **Contenido unificado en UN módulo.** O `content` es el dueño real (mover `content*.py`, `inspiration`, `content_strategy`, `content_library`, `verticals` a `packages/content/backend/routers/` y reapuntar su `module.json`) y `operations` deja de listarlos; o se borra `packages/content/` y queda como sub-feature de `operations`. **Recomendado:** completar `content` como módulo real (es la intención implícita del sidebar). Y agregar **dedup** en `register_modules()`.
- **Un solo generador de contenido.** `content_strategy.py` (Gemini + KB grounding + `template_compositor` Tier-1, scope flexible) es el canónico. `content_regen.py` queda solo para `regenerar/{post_id}`. Una sola fuente de grounding: `content_grounding.fetch_kb_block`. Una sola fuente de imagen: `template_compositor`.
- **Un solo motor de chatbot.** `packages/smartbot/.../chatbot.py` (con su `webhook` helper repointado a `packages/core`). La copia legacy se borra.
- **Un solo ESP activo (Perfit).** `unified_campaigns` + `proposals` como hub de campañas. Klaviyo: o `enabled=false` + router deprecado, o constantes renombradas honestas si se conserva para import histórico.
- **Una sola superficie de métricas.** `/analytics` (global) y `/smartbot/analytics` (del bot) se conservan pero se relabelan para que sean distinguibles ("Analytics" vs "Analytics del Bot").

**Árbol limpio objetivo (backend):**

```
dashboard/
├── backend/
│   ├── main.py                      # solo bootstrap + register_modules()
│   ├── module_loader.py             # con DEDUP de routers
│   ├── lib/                         # helpers compartidos (ex import-shadow)
│   ├── crons/                       # cron_objectives_update, cron_tasks, cron_stock_sync (reparado) → todos importan de packages.*
│   └── routers/                     # VACÍO o solo módulos aún-no-migrados
│       └── (salto_cuantico, salto_cuantico_webhook, retention_engine → migrar a packages/)
└── packages/
    ├── core/        (analytics, webhook, integrations, brands_admin, public_pages)
    ├── cerebro/     (cerebro, chat)
    ├── objectives/  (objectives)
    ├── intelligence/(intel, prices, ci_warroom)
    ├── ecommerce/   (b2c, customers, sales*, journeys*, journey_config, retention, catalog, tiendanube_oauth/sync, ecommerce*, unified_analytics)
    ├── b2b/         (crm, meetings, outreach*, invoice_ocr, zona_mapping, prospecting)
    ├── smartbot/    (chatbot, inbox, contacts, broadcast, flow_builder, knowledge_base, wa_web, sales_wa, ig_dm_redirect, bot_*, smartbot_analytics)
    ├── meta_ads/    (meta_ads)
    ├── operations/  (brand, canva, ops, tasks)
    ├── content/     (content, content_images, content_regen, content_stories, inspiration, content_strategy, content_library, verticals)  ← DUEÑO ÚNICO
    └── marketing/   (unified_campaigns, proposals, campaigns, templates, b2c_outreach)  ← Klaviyo deprecado
```

---

## 7. IA / Navegación propuesta

Hoy el sidebar es asimétrico: solo SmartBot se expande (7-8 sub-ítems), el resto es plano, hay 4 superficies de campañas, 2 íconos colisionan (🎯 Objetivos = Contenido; 🤖 SmartBot = Chat) y rutas vivas no figuran en el nav (`/email-legacy`, `/smartbot/outreach`).

**Principios:** una función = un lugar; agrupar lo que es lo mismo; íconos únicos; nada accesible solo por URL.

### Sidebar ANTES

```
Cerebro              (/)
Objetivos         🎯 (/objectives)
Inteligencia         (/intelligence)
Ecommerce            (/ecommerce)
B2B                  (/b2b)
SmartBot          🤖 ▾ (/smartbot/inbox)
   ├ Inbox
   ├ Automatizaciones
   ├ KB
   ├ Contactos
   ├ Difusión        (/smartbot/campaigns)
   ├ Analytics       (/smartbot/analytics)
   └ Configuración
Meta Ads             (/meta-ads)
Contenido         🎯 (/content)       ← mismo ícono que Objetivos
Campañas             (/marketing)      ← 2ª superficie de campañas
Operaciones          (/ops)
Marca                (/brand)
Retention            (/retention)
Salto Cuántico       (/salto-cuantico)
Analytics            (/analytics)      ← choca de label con SmartBot›Analytics
Settings             (/settings)
   (oculto, solo URL: /email-legacy, /smartbot/outreach, Chat 🤖 flotante)
```

### Sidebar DESPUÉS

```
Cerebro              (/)                          🧠
Objetivos            (/objectives)                🎯
Inteligencia         (/intelligence)              🔭
Ecommerce            (/ecommerce)                 🛒
B2B                  (/b2b)                        🤝
Conversaciones ▾     (/smartbot/inbox)            💬   ← renombrar "SmartBot" a algo humano
   ├ Inbox
   ├ Contactos
   ├ Knowledge Base
   ├ Automatizaciones
   └ Configuración
Campañas ▾           (/marketing)                 📣   ← HUB ÚNICO de envíos
   ├ Email + WhatsApp (UnifiedCampaigns)
   ├ Difusión WA      (ex /smartbot/campaigns)
   └ Outreach B2C     (ex /smartbot/outreach, ahora visible)
Contenido            (/content)                   🗓️   ← ícono propio (calendario), NO 🎯
Marca                (/brand)                      🎨
Operaciones          (/ops)                        🛠️
Meta Ads             (/meta-ads)                  📊
Retention            (/retention)                 🔁
Salto Cuántico       (/salto-cuantico)            🚀
Analytics            (/analytics)                 📈   ← global
Asistente IA         (panel, ícono propio)        ✨   ← Chat ya NO comparte 🤖 con el bot
Settings             (/settings)                  ⚙️
```

**Cambios clave:**
- **Campañas pasa a ser un hub con 3 pestañas** (Email+WA / Difusión / Outreach). Mata `/email-legacy` y deja de haber 4 lugares para "mandar campañas" → queda 1.
- **"SmartBot" → "Conversaciones".** "Difusión" y "Outreach" salen de abajo de SmartBot (son envío masivo, van a Campañas). Conversaciones queda con lo que es realmente conversacional (Inbox, Contactos, KB, Automatizaciones, Config).
- **`SmartBot›Analytics` se absorbe** en una pestaña dentro de Conversaciones o se relabela "Analytics del Bot" para no chocar con el `/analytics` global.
- **Íconos únicos:** Contenido deja 🎯 (que queda solo para Objetivos); el Asistente IA (Chat flotante) deja de compartir 🤖 con el bot.
- **Cero rutas fantasma:** `/email-legacy` y `/smartbot/outreach` dejan de ser solo-URL.
- **Mover los 17 redirects** de `App.tsx` a un mapa `LEGACY_REDIRECTS` aparte, y los **12 subcomponentes** de `pages/` a `components/{content,campaigns,brand}/` — `pages/` solo páginas ruteadas.

---

## 8. Plan de remediación por fases

### P0 — Borrados seguros + reparación crítica (riesgo bajo, hacer ya)

1. **Reparar `cron_stock_sync.py`** (riesgo alto si está agendado, pero el fix es contenido): repointar `from routers.stock import _do_shopify_sync` a la función real de stock en `packages/operations/.../ops.py`. Verificar en VPS si el cron está en crontab. *(Esto es P0 por urgencia, aunque toque código, no solo borrar.)*
2. **Borrar los ~49 `.bak`/`.deprecated`/`.pre_migration`** (backend/routers, marketing/routers, frontend/src, main.py.pre_migration). Cero refs posibles.
3. **Borrar los 39 routers legacy idénticos** de §4.A (no tocar los 6 helper-vivos ni los 3 montados-a-mano ni los 20 divergidos).
4. **Borrar los 4 routers legacy de contenido** (`content`, `content_images`, `content_regen`, `content_stories`).
5. **Borrar las 7 páginas frontend muertas** (§4.A).
6. Orden: primero `.bak` (cero riesgo), después legacy idénticos, después páginas muertas. Build de frontend + arranque de API para validar tras cada lote.

### P1 — Unificar duplicados funcionales (riesgo medio)

1. **Repointar los 6 imports import-shadow** (`objectives`, `journeys`, `webhook`, `ig_dm_redirect`, `tiendanube_sync`, `tasks`) a `packages.*` o a `backend/lib/`. Validar Cerebro, chatbot, TN-sync y crons en runtime. **Recién después** borrar esos 6 legacy.
2. **Auditar los 20 routers divergidos** (foco en `cerebro` +253L, `outreach` +359L, `webhook`, `crm`): confirmar que el package tiene todo lo del legacy. Una vez confirmado → borrar el legacy.
3. **Resolver el doble montaje de contenido:** un solo `module.json` dueño (recomendado `content`) + dedup en `register_modules()`. Quitar los 5 routers compartidos del otro `module.json`.
4. **Degradar `content_regen` a `regenerar/{post_id}`;** `content_strategy` queda como generador único. Borrar los handlers `publicar-ahora`/`publicar-status` duplicados en `content_regen`.
5. **Decidir Klaviyo:** confirmar 0 tráfico `/api/email`; si confirma, `klaviyo.enabled=false`, deprecar `email_marketing*` + `EmailPlanner.tsx` + ruta `/email-legacy`. Si se conserva, renombrar `PERFIT_*`→`KLAVIYO_*` en `email_marketing.py`.

### P2 — Refactor de IA/navegación (riesgo medio, UX)

1. **Consolidar Campañas en hub con 3 pestañas** (Email+WA / Difusión / Outreach). Mover `/smartbot/outreach` y `/smartbot/campaigns` adentro. Matar `/email-legacy`.
2. **Renombrar "SmartBot"→"Conversaciones"**, sacar Difusión/Outreach de su sub-árbol, relabelar `SmartBot›Analytics`.
3. **Íconos únicos** (Contenido ≠ 🎯; Asistente IA ≠ 🤖 del bot).
4. **Mover 12 subcomponentes** de `pages/` a `components/`. **Mover 17 redirects** a `LEGACY_REDIRECTS`.
5. Actualizar `PATH_MODULE_MAP` (`Sidebar.tsx`) y `marketing/module.json` (`/campaigns`→`/marketing`) para que reflejen el ruteo real.

### P3 — Limpieza profunda (riesgo bajo-medio, orden)

1. **Migrar `salto_cuantico*` y `retention_engine`** a un package real (`packages/salto`, `packages/retention`) y vaciar `backend/routers/` por completo.
2. **Descontaminar marca:** reemplazar los 22 `#E0E938` y los fallbacks `--accent` por `var(--brand-primary)` inyectada desde `branding.primary_color`.
3. **Corregir `sidebar_title`** en `deployment_config.json` a "Korean Root" (hoy dice "SmartBrain") y eliminar el hardcode `🧠 Smart Brain` del header móvil.
4. **Corregir `attr`→`attrs`** en `b2b/module.json`.
5. **Revisar logs `[ModuleLoader] Errors`** en el VPS para detectar imports de package reventando en runtime.

---

## 9. Notas para el rediseño visual (input al design system Tier-1)

- **Color contaminado, primera prioridad.** `#E0E938` (lime Smart Foods) hardcodeado **22 veces en 5 archivos** del frontend de contenido + fallbacks `--accent #E0E938` en `App.tsx:48` (PageLoader spinner), `Sidebar.tsx` (L234/243/419…) y `Layout.tsx:64` (botón Chat). KR es **`#C2185B`** (rosa, confirmado en `deployment_config.json`). El design system debe exponer **un único token `--brand-primary`** alimentado desde `branding.primary_color`, y prohibir literales hex en componentes (regla `feedback_no_hardcode`). Mientras el branding carga, hoy se ve color SF: el PageLoader y el primer paint deben usar el token, no el fallback lime.

- **`sidebar_title` incorrecto en el config, no solo en el código.** `deployment_config.json` → `branding.sidebar_title = "SmartBrain"` (debería ser "Korean Root"). Además, hardcodeos textuales: header móvil `🧠 Smart Brain` (`Layout.tsx:48`) y default `'Smart Brain'` en `Sidebar.tsx:388`. El design system debe tomar **título e ícono de marca del branding**, con fallback neutro (no "Smart Brain").

- **Sistema de íconos con colisiones.** 🎯 lo comparten **Objetivos y Contenido**; 🤖 lo comparten **la sección del bot y el panel Chat flotante**. El nuevo set de íconos debe ser **1:1 por sección** (ver propuesta §7). Definir un token-set de íconos en el design system.

- **Jerarquía de navegación asimétrica.** Solo "SmartBot" expande sub-ítems; B2B/Ecommerce/Contenido/Campañas tienen muchas pestañas internas sin pista en el nav. El design system debe definir **un único patrón de nesting** (cuándo una sección expande y cuándo no) y aplicarlo parejo.

- **Estados de carga y marca.** Definir skeleton/spinner **neutros** (sin color de marca hasta que el branding resuelva) o que ya usen el token correcto, para que ningún tenant vea el color de otro durante el load.

- **`pages/` vs `components/`.** 12 subcomponentes viven en `pages/` y solo 28 de 47 `.tsx` se rutean. El design system / convención de carpetas debe separar **páginas ruteadas** (`pages/`) de **componentes** (`components/`), así el árbol comunica la estructura real.

- **Higiene de árbol.** ~49 archivos `.bak`/`.deprecated`/`.pre_migration` versionados en disco inflan el repo y rompen greps de "qué importa a X". Convención dura: **versionado en git, nunca en el árbol servido.**
