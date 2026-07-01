---
date: 2026-05-31
type: report
tags: [smartbrain, b2b, ux, usabilidad, arquitectura, outreach, whatsapp, informe]
status: parcialmente-implementado
derivado_de: b2b-core-auditoria
---

> **IMPLEMENTADO (31 may 2026, core `9618bcb`, deployado SF+KR):** El "gran win" (señalización de WhatsApp) + los 2 canales de outreach separados + el N+1. Concretamente: tab "Contactar" con selector Chip-frío vs API-oficial (chip con estado real); botones honestos ("Abrir en mi WhatsApp" / "Enviar desde el sistema" / "Ya le escribí"); ventana 24h en lenguaje de negocio; jerga de la 1ª pantalla traducida (Para contactar / con permiso / Sin contacto +7d / Entregados / Fallidos); endpoint batch wa-status (N+1 eliminado). **Pendiente:** jerga en tabs secundarias (LTV/churn/AOV), virtualización de listas, Crm.tsx god-component, confirm/alert nativos, consolidar las 3 vistas de "Clientes". Detalle del trabajo en memoria `project_b2b_shared_core.md`.

# Informe de arquitectura + usabilidad — Sección B2B (SmartBrain)

> Encargado por Andrés (31 may 2026): detectar mejoras de usabilidad, funcionamiento y todo lo que confunda a usuarios inexpertos. Método: 2 agents de desarrollo (crítico UX research-backed + arquitecto frontend) + investigación propia del flujo de mensajería en el código real (no de memoria). Usuario objetivo: dueño de PyME / vendedor, NO técnico.

## Veredicto

La sección es **funcionalmente potente pero está escrita para quien programó el backend, no para quien vende.** Dos problemas dominan, y los dos nacen del mismo lugar — la mensajería de WhatsApp:
1. **Confusión "¿mandé el mensaje o no?"** — hay 3 canales de WhatsApp con botones casi idénticos que hacen cosas opuestas (uno abre tu celular, otro registra sin enviar, otro envía por el sistema). Un vendedor cree que contactó 30 leads cuando en realidad solo apretó "Contactado" (que no manda nada).
2. **Jerga técnica sin traducir** en la pantalla de uso diario (`stale`, `churn`, `opt-in`, `outreach`, `template`, `ventana`, `LTV`, `AOV`).

La buena noticia: **el 70% se arregla con copy/microcopy** — bajo esfuerzo, alto impacto, sin tocar lógica.

---

## 0. Cómo funciona la mensajería B2B hoy (base para entender todo lo demás)

Son **3 canales distintos**, y cuál se usa NO está señalizado en la UI:

| Canal | Quién lo dispara | Estado | Uso |
|---|---|---|---|
| **Manual (wa.me)** | Vos, botón "WA" en el pipeline → tu WhatsApp personal | Activo | Outreach frío 1-a-1, a mano. "Contactado" SOLO registra, no envía. |
| **WABA oficial (API)** | Journeys, campañas, y Secuencias B2B (wizard→borrador→aprobás→`cron_sequences_runner` cada hora→`graph.facebook.com` con templates) | Activo | Seguimientos con plantillas aprobadas, por el número oficial |
| **Chip ZTE / Baileys** (`5491165857832`, `wa-baileys:8787`) | *(nada)* | **HUÉRFANO** | Se montó para outreach frío masivo; ningún flujo lo usa hoy |

**Contradicción central:** se invirtió en el chip ZTE para hacer outreach frío sin arriesgar el número oficial, pero **ningún flujo lo toca** (su único cron, `cron_cold_outreach_b2b.py`, está desagendado y apunta a "Evolution API", infra vieja pre-Baileys). Mientras tanto, las Secuencias B2B mandan por el **número oficial con templates** — exactamente el riesgo de ban que el chip ZTE debía evitar.

---

## 1. Confusiones para usuarios inexpertos (UX)

**C1 (CRÍTICA) — "¿Mandé el mensaje o no?"** Los 3 caminos producen estados visuales casi idénticos (mismo verde, mismo 📱) pero hacen cosas opuestas:
- `LeadCard.tsx:71-81` botón "📋 Copiar + WA" → abre tu WhatsApp (NO envía por el sistema).
- `LeadCard.tsx:83-92` botón "✅ Contactado" → `POST /outreach/.../contacted` → **solo marca estado, no envía**. Da feedback de éxito idéntico a un envío real.
- `LeadPanel.tsx:186-201` "📤 Enviar" → SÍ envía por API, pero solo si `window_open`.
- En `LeadPanel.tsx:333-337` conviven "Enviar" (API real) y "Copiar para WA personal" (abre celular) sin una línea que los distinga.
- **Fix (copy):** renombrar verbos → "Abrir en mi WhatsApp" / "Enviar desde el sistema" / "Marcar como contactado (no envía)" + 1 línea de microcopy "esto sale solo" vs "esto lo mandás vos".

**C2 (CRÍTICA) — "¿Qué es una ventana?"** El concepto de la ventana de 24h de WhatsApp se expone crudo (`LeadPanel.tsx:294` "Ventana activa", `:342` "Sin ventana — solo templates"). Un dietético no sabe la política de Meta y cree que la herramienta está rota.
- **Fix:** "Te escribió hace poco — podés responderle directo (gratis)" / "Hace +24h que no te escribe; para reabrir mandá una plantilla o escribile desde tu WhatsApp" + tooltip "?".

**C3 (ALTA) — Jerga sin traducir:** "template/plantilla" (mezcla idiomas), "opt-in", "outreach" — los 3 términos más repetidos del Pipeline, ninguno en idioma de vendedor.

**C4 (ALTA) — Sopa de íconos** 📱/✅/💬/🔒/✓✓ que cambian de significado por contexto, sin leyenda (`LeadCard.tsx:157-200` apila 3-4 badges; el ✅ es "opt-in" en un lado y botón "Contactado" en otro; "delivered" es ✓✓ en la tarjeta y ✅ en el panel).

**C5 (ALTA) — Navegación duplicada:** "Clientes" vive en 3 tabs (Clientes, Inteligencia B2B→Clientes, Ventas→Clientes); "Cobros" en 2; "Pipeline" en 2. Cada uno con endpoints distintos (`/crm/customers/health` vs `/b2b/clients` vs `/sales/ltv-detail`) → **los números pueden no coincidir entre tabs**, lo que rompe la confianza. "Inteligencia B2B" se siente como una app paralela pegada.

**C6 (MEDIA) — Secuestro de navegación:** `Crm.tsx:141-148` cambia de tab solo a "Clasificar" sin pedirlo, y explica con un nombre de archivo interno ("Importados desde CLIENTES MAYORISTAS/24").

## 2. Jerga visible a traducir (español de negocio, consistente)

`stale` → "sin contacto +7 días" · `churn` → "abandono/clientes que dejan de comprar" · `LTV` → "valor total del cliente" · `AOV` → "ticket promedio" (ya se usa en otro lado → unificar) · `opt-in` → "dio permiso" · `outreach` → "primer contacto/contactar" · `template` → "mensaje pre-armado" · `lookalikes` → "negocios parecidos a tus mejores clientes" · `ICP` → "tipo de negocio" · `dry run` → "ver primero sin importar" · `Revenue`/`Facturación` (inconsistente) → elegir uno · `Churned`/`Perdido` (inconsistente) → elegir uno · `health_store` → "tienda saludable" · `Brain (auto)` → "generado por el sistema" · "ejecutar el motor" → "calcular salud de mis clientes".

## 3. Funcionamiento / arquitectura (del review de frontend)

| # | Hallazgo | Impacto | Esfuerzo |
|---|---|---|---|
| 1 | **N+1: cada `LeadCard` pide su propio `/wa-status`** (`LeadCard.tsx:47`) → 50-300 requests al cargar el kanban con 1300+ leads. SQLite hace cola → lentitud/503. Fix: endpoint batch + pasar mapa como prop. | Crítico | Bajo |
| 2 | **`Crm.tsx` God component (784 líneas):** orquesta tabs + fetch + scraper + 3 subcomponentes embebidos (MiDiaView, ZoneMapping, ProductCodeMap). Fix: hook `usePipelineLeads` + extraer subcomponentes. | Alto | Medio |
| 3 | **Filtros Kanban vs servidor desincronizados** (`KanbanBoard` filtra client-side ignorando el fetch del padre). | Medio | Bajo |
| 4 | **Listas de 1300+ leads sin virtualización** (kanban + lista). Fix: `@tanstack/virtual`. | Alto | Medio |
| 5 | `useEffect` deps incorrectas en `SalesView` (no recarga al cambiar `customerId`). | Medio | Bajo |
| 6 | **14 `confirm/alert/prompt` nativos** — bloquean, no se estilizan, el `prompt()` del motivo de descarte deja estado inconsistente si se cancela. Fix: `ConfirmDialog` propio. | Medio | Bajo |
| 7 | `CustomersTab`: 4 fetches en mount sin error state visible → tabla en blanco sin mensaje si falla. | Medio | Bajo |
| 8 | `B2BIntelligence`: doble-fetch de `loadClients` en mount. | Bajo | Bajo |
| 9 | `OutreachTemplate` definida 3 veces (divergente: `LeadPanel` no filtra `activo`). Mover a `types/crm.ts`. | Bajo | Bajo |
| 10 | `filterZona` usa `includes()` con valores exactos del dropdown (matchea "GBA" con "GBA Norte"). | Bajo | Bajo |

Extra UX-técnico: **Mi Día no persiste lo marcado como "hecho"** (`Crm.tsx:591`, estado local) → si recarga, lo pierde. Drag&drop del kanban sin affordance (nadie sabe que se arrastra). Secuencias quedan "en borrador para aprobar" sin link a dónde aprobar. Tipografía 9-10px para datos accionables (ilegible). Texto blanco sobre lima `#E0E938` (falla contraste AA; el propio código ya usa texto oscuro en otro lado → inconsistente).

## 4. Calidad de datos

- 1 lead con placeholder sin resolver `{{first_name}}` (id 1911) se muestra prominente en Mi Día. La data por lo demás está limpia (de 1632: 0 sin nombre, 7 sin zona, 0 sin teléfono). Fix: sanear/ocultar placeholders en el front.
- Riesgo de números contradictorios entre tabs (C5) → una sola fuente de verdad para clientes/cobros.

## 5. Priorización consolidada (impacto × esfuerzo)

**Quick wins — casi todo copy, alto retorno:**
1. Renombrar botones de WhatsApp para que el verbo no mienta + microcopy "sale solo / lo mandás vos" (C1). **El mayor retorno del informe.**
2. Traducir ventana/template/opt-in/outreach/stale/churn a español de negocio (C2, C3, §2).
3. Diferenciar en el timeline "enviado por sistema" vs "copiado para mandar a mano".
4. Persistir o rotular el "hecho" de Mi Día. Sanear el `{{first_name}}`.
5. **N+1 de wa-status (endpoint batch)** — único técnico en quick wins, impacto crítico en velocidad.

**Pronto (impacto alto, esfuerzo medio):**
6. No secuestrar navegación a Clasificar; unificar íconos + leyenda; estados vacíos con CTA; cerrar el loop de Secuencias (link a aprobar); contraste + tipografía.
7. Virtualizar listas; extraer `Crm.tsx`; unificar filtros.

**Estratégico (alto valor, más esfuerzo):**
8. Consolidar las 3 vistas de "Clientes" y 2 de "Cobros" en una sola fuente de verdad; reposicionar/ocultar "Inteligencia B2B".
9. Onboarding de primer uso (replicar el tono de `EmptyPipelineState`, que es el mejor componente para novatos hoy).
10. **Decisión de negocio (no UX):** reconectar el chip ZTE a un flujo real, o jubilarlo y definir que el outreach frío va por wa.me manual. Hoy está en limbo.

## El gran win (si se hace una sola cosa)
Arreglar la señalización de WhatsApp (C1+C2), 100% con copy. Hoy un vendedor cree que escribió a un lead cuando solo abrió su celular o apretó "Contactado" (que no envía). Eso = leads sin contactar + decisiones sobre datos falsos. Renombrar verbos + explicar la "ventana" en idioma de negocio elimina el malentendido más caro, sin tocar lógica.

Relacionado: [[b2b-core-auditoria]], [[b2b-shared-core-submodule]], [[wizard-outreach-multitenant]].
