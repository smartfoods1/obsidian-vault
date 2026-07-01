---
date: 2026-06-17
type: auditoria
tags: [korean-root, smartbrain, auditoria-ceo, usabilidad, impacto-negocio, contraste]
status: activo
relacionado: [[auditoria-funcional-jun17]]
---

# Auditoría CEO — SmartBrain Korean Root (área por área)

> Revisión desde la silla del CEO de KR: usabilidad real + impacto de negocio de cada módulo/submódulo, con checks en vivo (endpoints + DB). 8 áreas, 30+ submódulos. Negocio real KR: e-commerce monoproducto (Limonada Cuántica + Shakti) en Tienda Nube, ~$63M ARS/mes, AOV 71k, recompra real 19.8%, email = 8.5% del revenue, mayorista a dietéticas. Equipo chico no-técnico (Victoria, Jorge, asistente).

## TL;DR para el CEO

**El sistema NO tiene un problema de capacidad — tiene un problema de activación y de ruido.** Lo que mueve plata funciona de verdad (Cerebro, Ecommerce, Campañas/email, Meta Ads, Bot). Las palancas más grandes están construidas pero **apagadas** (Retención $40M potenciales sin enviar; Salto Cuántico en dry-run; 637 leads B2B sin trabajar). Y hay **ruido que hace ver el sistema roto** (tabs vacíos, módulos contaminados con datos de Smart Foods, 3 lugares distintos para mandar el mismo WhatsApp). El dato más comercial: el cuello de botella de KR es **el CLICK, no la conversión** (Histórico: CTR 0.1%).

## Scorecard por área

| Área / módulo | ¿Funciona? | Impacto | Veredicto |
|---|---|---|---|
| **Cerebro (home)** | ✅ real | 🟢 alto | Mantener (joya: lista de acciones diaria con plata) |
| Objetivos | ⚠️ vacío (0 OKRs) | 🔴 bajo | Ocultar o sembrar 2-3 metas |
| **Ecommerce · Overview** | ⚠️ parcial | 🟢 alto | Mejorar (bug nav 'acciones', 2 KPIs muertos) |
| Ecommerce · Clientes | ✅ real (38.5k) | 🟢 alto | Mantener |
| **Ecommerce · Segmentos** | ✅ real | 🟢 alto | Mantener (mejor tab: segmento→campaña) |
| Ecommerce · Pedidos | ✅ real (55.9k) | 🟡 medio | Mantener (renombrar botón "Shopify"→TN) |
| Ecommerce · Productos | ❌ vacío | ⚫ nulo | **Eliminar** (0 filas + monoproducto) |
| **Retención · Motor 360** | ✅ real, honesto | 🟢 alto (si se activa) | Mantener + **ACTIVAR** ($40M dormidos) |
| **B2B · Pipeline** | ⚠️ leads ok, flujo muerto | 🟢 alto | Mantener leads, trabajar los 637 |
| **B2B · Contactar leads** | ❌ no envía | 🟢 alto | Mejorar (cablear canal + ✅contraste) |
| B2B · Clientes/Ventas | ❌ vacío (0 órdenes) | 🟡 medio | Mantener dormido |
| B2B · Landing mayoristas | ⚠️ tráfico sí, 0 conv | 🟡 medio | Mejorar (brand_id + captura ?ref) |
| B2B · Prospecting | ❌ sin PLACES_API_KEY | 🔴 bajo | Ocultar (sobran leads ya) |
| **Campañas · Plan Quincenal** | ✅ real, KB-grounded | 🟢 alto | Mantener (dar permiso a ops) |
| **Campañas · Mis Campañas** | ✅ end-to-end email | 🟢 alto | Mantener (18 enviadas, probado) |
| Campañas · Cola WA | ⚠️ indicador miente | 🟡 medio | Mejorar (detector cron + wa_sent_at) |
| Campañas · Segmentos/Histórico | ✅ real | 🟢 alto | Mantener (Histórico grita CTR 0.1%) |
| **Conversaciones · Inbox** | ✅ bot vivo | 🟢 alto | Mantener + que un humano lo trabaje |
| **Conversaciones · Bot/KB** | ✅ real (10 docs) | 🟢 alto | Mantener (evita alucinaciones) |
| Conversaciones · Bot métricas | ⚠️ thin | 🟡 medio | Simplificar (3 KPIs) |
| Conversaciones · Difusión WA | ❌ vacío, redundante | 🔴 bajo | **Eliminar** (dup de Campañas) |
| Conversaciones · Outreach B2C | ❌ vacío + 404 | 🔴 bajo | **Eliminar** (dup de Campañas) |
| **Analytics · Facturación** | ✅ real | 🟢 alto | Mantener (nominal vs real = ✓) |
| Analytics · Estacionalidad | ✅ real | 🟡 medio | Mantener |
| Analytics · Productos | ✅ real | 🔴 bajo | Simplificar (monoproducto) |
| **Analytics · Clientes** | ✅ real (19.9%) | 🟢 alto | Mantener |
| Analytics · Geografía | ❌ vacío (bug query) | 🔴 bajo | Arreglar (datos en tn_orders) o ocultar |
| Analytics · Tendencias | ✅ real | 🔴 bajo | Simplificar (dup Facturación; q1-q4 roto) |
| **Meta Ads** | ✅ real, sync hoy | 🟢 alto | Mantener (ROAS 2.43, recs accionables) |
| **Inteligencia (competidores)** | ❌ vacío + contaminado SF | ⚫ nulo | **Eliminar** (competidores de SF + 422) |
| **Operaciones (stock/tareas/fin)** | ❌ vacío + contaminado SF | ⚫ nulo | **Eliminar/ocultar** (Flexit/Shopify/Florencia) |
| **Contenido (IG)** | ⚠️ copy ok, no publica | 🟡 medio | Mejorar (conectar IG o reencuadrar) |
| **Marca (Brand Context)** | ✅ real | 🟢 alto | Mantener (fuente de verdad anti-alucinación) |
| **Salto Cuántico** | ⚠️ en dry_run | 🟢 alto (si se activa) | **ACTIVAR** (único motor recompra) |
| Settings/Integraciones | ✅ honesto | 🔴 bajo | Mejorar (agregar "Conectar") |

## Las 3 palancas dormidas (la plata que está sobre la mesa)

1. **Retención Motor 360 — ~$40M ARS potenciales, hoy $0.** 11.280 clientes dormidos segmentados + en Perfit, secuencia win-back de 3 toques escrita (proposal #23). Falta UNA cosa: que Victoria/Jorge la aprueben y envíen. Es el ROI más alto del dashboard.
2. **Salto Cuántico — único motor de recompra construido, en dry_run.** Corrió un piloto real en mayo, ahora simula (0 envíos reales, $18k atribuidos, parado desde 31/5). Pasar de dry_run a vivo (con canary) sobre la recompra del 19.8%.
3. **B2B — 637 leads mayoristas calificados, sin tocar.** 636/637 congelados en 'prospecto', 0 secuencias enviadas. El "Contactar leads" genera el copy pero **no tiene canal de envío cableado para KR** (el chip es de Smart Foods, Perfit sin list_id). Cablear un canal + trabajar los leads.

## Ruido a eliminar (hace ver el sistema roto)

- **Productos (Ecommerce)** — tab 100% vacío, sin sentido para monoproducto.
- **Inteligencia (competidores)** — vacío + sembrado con competidores de Smart Foods (ENA Sport, creatina) + endpoint 422.
- **Operaciones** — stock/finanzas/órdenes vacíos o sin tablas; UI muestra Flexit/Shopify/"Florencia" (sistemas de SF que KR no usa).
- **Difusión WA + Outreach B2C** — 2 canales de WhatsApp vacíos y redundantes con Campañas (hay 3 puertas al mismo cuarto).
- **Objetivos** — scaffolding OKR vacío.

## Bugs de confianza (rápidos, alto valor)

- Cerebro saluda **"Buenos días, Andrés"** en KR (fuga cross-tenant; debe ser Victoria/Jorge) — `Overview.tsx:442`.
- Alerta de Ecommerce apunta al tab **'acciones'** (eliminado) → pantalla en blanco al clickear.
- **Cola WA dice "inactiva"** con el envío prendido (detector lee `crontab -l` desde el API).
- Bot corre 100% por OpenRouter a ~5.5s (GEMINI key vacía) → restaurar Gemini = bot más rápido.
- Geografía y `/analytics/cohorts` (500), `/b2c-outreach/stats` (404) rotos.
- Contenido no publica a IG (sin token).

## Contraste — RESUELTO (jun 17) ✅

El B2B era un **tema oscuro entero mal portado** al tema claro: `bg-white/5`, `border-white/10`, `text-gray-600`, `text-*-400` → inputs/bordes/botones invisibles sobre blanco. **Re-skin sistemático: 414 reemplazos en 20 archivos** de `packages/b2b/frontend` (Crm, KanbanBoard, SalesView, LeadPanel, UnifiedSequenceWizard, OutreachHub, CustomersTab, etc.). Verificado en vivo: "Contactar leads" ahora tiene cajas/bordes/labels visibles.
Además: Retención (barras índigo visibles + badges verde-600/ámbar-600 + bordes), UnifiedCampaigns (empty-state navy-sobre-navy → claro), Analytics (C.muted #94a3b8→#475569, ~55 textos), Ops (re-skin), Cerebro (banner #93c5fd→#1d4ed8). Backups en `/root/kr_theme_bak/`. Build verde.

## Recomendación de foco (1 mes)

1. **Activar las 3 palancas dormidas** (Retención, Salto, B2B) — ahí está el crecimiento real.
2. **Atacar el CLICK** (CTR 0.1%) — formato visual de email, no más volumen. Ver [[project_kr_email_overhaul]].
3. **Eliminar el ruido** (5 módulos) — menos laberinto = el equipo no-técnico usa lo que importa.
4. **Bugs de confianza** (saludo, alerta rota, Cola WA) — para que el equipo confíe en los números.
