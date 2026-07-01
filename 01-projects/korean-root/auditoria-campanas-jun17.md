---
date: 2026-06-17
type: auditoria
tags: [korean-root, smartbrain, campañas, marketing, ux, arquitectura]
status: completo
derivado_de: auditoria-ceo-jun17
---

# Auditoría — Sección "Campañas" KR (SmartBrain)

> Auditoría de arquitectura + UI + funcionalidad + usabilidad de `/marketing` (lo que la nav llama "Campañas"), desde la piel de un operador de KR. 17 jun 2026.

## Veredicto

Construida por un ingeniero que entiende la máquina de estados y los dos motores de envío: potente pero filtra toda la complejidad al usuario final. El flujo "premium" (Plan IA → aprobar por campaña) es sólido; el resto quedó atrás. Dos bugs en vivo rompen confianza: KPIs blanco-sobre-blanco (invisibles) y WhatsApp casi no envía.

## Mapa del código

- **Nav**: "Campañas" → `/marketing` → `UnifiedCampaigns.tsx` (link único, sin subitems). `/campaigns` redirige a `/smartbot/automations`; `/smartbot/campaigns` → `/marketing`.
- **Frontend**: `dashboard/frontend/src/pages/UnifiedCampaigns.tsx` (2016 líneas) + `ProposalsTab.tsx` (~1500). Embebe el flujo de propuestas.
- **Backend (canónico, vía module_loader)**: `dashboard/packages/marketing/backend/routers/`
  - `unified_campaigns.py` (1468 líneas) — 13 endpoints
  - `proposals.py` (2173 líneas, 95KB) — generación de estrategia IA
  - `templates.py`, `campaigns.py` (legacy), `klaviyo.py` (legacy, KR usa Perfit), `b2c_outreach.py`
- **DB real**: `dashboard/ops_korean-root.db` (203MB). La de `workspace/ops_korean-root.db` es un archivo vacío (0 bytes).
- **Tablas**: `campaign_proposals` (plan IA), `unified_campaigns` (campaña ejecutable, email+WA en misma fila), `kr_perfit_*` (espejo Perfit).
- **Cron WA**: `scripts/cron_unified_wa.py` cada 5 min, `UNIFIED_WA_DRY_RUN=0` (real).

## Estado en vivo (DB hoy)

- unified_campaigns: 28 total → 18 sent, 8 draft, 2 scheduled.
- **email_sent_at: 17 ✅ · wa_sent_at: 1 ❌**.
- proposals: 5 → 1 approved, 1 draft, 3 **refining (trabadas)**.
- 29 segmentos Perfit.
- Cron WA activo en modo real pero cada tick: `checked=None due=None dispatched=None` → no despacha.

## Bugs P0 en vivo

1. **KPIs invisibles** — `UnifiedCampaigns.tsx:1392` `MiniStat`: `color: accent ? KR : "#FFFFFF"` sobre `background:"#fff"` (1390). Solo "Revenue" tiene `accent`. Enviados/Abiertos/Clicks/Conversiones salen blanco sobre blanco en detalle de campaña (405-408), editor (681-684) e Histórico (1345-1348). Introducido por re-skin de colores 17/06. Fix: 1 línea. Verificar build en browser.
2. **WhatsApp no despacha** — 1 envío real en toda la historia vs 17 email. Cron activo (no dry-run) pero reporta None/None/None. La regla "email+WA simultáneo" no se cumple en la práctica.
3. **"Lanzar ya" sin conteo** — `UnifiedCampaigns.tsx:1245`: solo `confirm()` de texto, no muestra a cuántos llega un envío masivo en vivo. El buen patrón existe en `ApproveCampaignModal` (ProposalsTab.tsx:1147+) pero no en el botón más peligroso.

## Arquitectura

### Bien
- **Grounding IA resuelto**: `proposals.py` `_fetch_context` (577-664) inyecta KB (`chatbot_knowledge`) + brand_context, falla loud (500) si vacío (641-649), valida términos prohibidos en gen Y refinamiento (`_validate_no_forbidden_terms` 205-262).
- **Approve por-campaña** (proposals.py:1690): push Perfit all-or-nothing con rollback + estado `push_failed` (1897-1961). Mejor código del módulo.
- Reparación de JSON truncado, fallback de modelo en 429, tope de audiencia en secuencias.

### Mal
- **God-files**: `proposals.py` 2173 líneas, 6 responsabilidades (router + LLM client + render HTML email + validación + URLs + wizard). Render de email importado cross-module con hacks `sys.path` (unified_campaigns.py:116, 206). Extraer `email_renderer.py` y `llm_client.py`.
- **Mono-brand de facto** pese a "unified": dominio `koreanroot.com.ar` hardcodeado ×5 (proposals.py:390,497,528,546,551), sender "Maria Victoria Sueldo"/"krootstore@gmail.com" (unified_campaigns.py:230-231), paleta (339-340), nombre marca (519,527). Viola regla no_hardcode.
- **Inconsistencia de generadores**: `draft_content` (unified_campaigns.py:142-171) tiene "cosmética coreana" hardcodeado, SIN KB, SIN brand_context, SIN validador → vector de alucinación que el resto cerró.
- **Opt-outs ignorados**: existen tablas `wa_optouts`, `retention_suppression`, `pending_optout_confirmations`, pero el path de envío no las consulta antes de armar audiencia (unified_campaigns.py:1299; proposals.py:1858). Riesgo compliance.
- **Sin idempotencia**: `send-to-perfit` (1249) y `launch-now` (1328) no chequean si ya se envió → re-disparo duplica. `send-to-perfit` sin rollback → zombie en Perfit si falla schedule (1304-1311).
- **Subject sin validar** contra límite Perfit 150 en frontera (solo confía en SDK).
- **Código muerto**: `BroadcastWizard.tsx` (719) + `InboundCampaignDetail.tsx` (496) no se importan en ningún lado = 1215 líneas.
- **Aislamiento de tenant**: endpoints por-id sin `AND brand_id=?`. NO es P0 (DB física por tenant + resolución por JWT lo contiene hoy), pero es deuda de defensa-en-profundidad si alguna vez se consolidan DBs.

## UI / usabilidad (piel del operador no técnico)

- **Jerga de dev cruda**: "Push a Perfit", estados en inglés como badge (`draft`, `pushed_to_perfit`, `pending_approval` — `UnifiedCampaigns.tsx:464` renderiza `{c.status}` sin mapa ES), y **comando SSH literal en la UI** (966-971) para activar WA (encima obsoleto, dry-run ya off).
- **"Aprobar" ambiguo**: crea borradores (ProposalsTab.tsx:483) vs programa envío real (622 / UnifiedCampaigns.tsx:1188), mismo color verde.
- **~6 acciones + 3 confirmaciones + 2 fechas tipeadas a mano** (`prompt()` nativo, formato `AAAA-MM-DD HH:MM`, líneas 1200,1215) para una campaña email+WA. Email y WA se programan separados → riesgo de fechas distintas.
- **Errores como `alert()` crudo** (UnifiedCampaigns.tsx:1160; ProposalsTab.tsx:493,1347). Único bien tratado: `ApproveCampaignModal` (parsea push_errors).
- **No cancela lo que programó**: confirm de borrar admite "NO la cancela en Perfit, hacelo manual" (1257-1258); WA "desde la base" (1209).
- **Dos caminos de creación que compiten**: "+ Nueva campaña" (manual) es el más prominente; empty state apunta al manual en vez del Plan Quincenal IA.
- **Sobrecarga**: editor gigante (cupón completo, markdown a mano para email, warning de API Meta "no \n ni 4 espacios" tirado al usuario — ProposalsTab.tsx:897).
- **Plomería expuesta**: tab "Cola WA" muestra estado del cron / próximo tick / dry-run; tab "Reenvío" del detalle es dump de variables (`SmartBrain · resend_enabled`, `Perfit · RESEND_DELAY` — 862-868).

## Plan de acción priorizado

| # | Sev | Qué | Esfuerzo |
|---|-----|-----|----------|
| 1 | P0 | Fix `MiniStat` blanco-sobre-blanco (KPIs invisibles) | 1 línea |
| 2 | P0 | Investigar por qué cron WA despacha 0 | medio |
| 3 | P0 | "Lanzar ya"/"Push": mostrar conteo de destinatarios antes (reusar ApproveCampaignModal) | bajo |
| 4 | P1 | `STATUS_LABELS` en español junto al `STATUS_COLORS` (119) | bajo |
| 5 | P1 | Sacar comando SSH de la UI → toggle o esconder a no-admin | bajo |
| 6 | P1 | Consultar opt-outs/suppression antes de audiencia | medio |
| 7 | P1 | Separar "Crear borradores" (gris) vs "Programar y enviar" (verde) | bajo |
| 8 | P1 | `draft_content`: cargar KB+brand_context + validador | medio |
| 9 | P2 | Idempotencia + rollback en send-to-perfit/launch-now | medio |
| 10 | P2 | Borrar código muerto; empezar a partir proposals.py | medio |

**Primero**: P0 #1-3 + #4 + #5. Con eso pasa de "necesita técnico al lado" a "usable con 20 min de capacitación". La refactorización de god-files es para mantenibilidad (sentirla vos, no el equipo). El bug más estratégico es #2: vendés "email+WA" y el WA no sale.

---

## FIXES APLICADOS Y DEPLOYADOS (17 jun 2026, tarde)

Backup: `/root/kr_campaigns_fix_bak_20260617_194314`. Build frontend verde (`tsc -b && vite build`), API reiniciada (health 200, router OK), todo verificado en vivo.

**Causa raíz WA (la importante):** el cron `cron_unified_wa.py` NO sourceaba `/etc/smartbrain/.env`, así `WA_ACCESS_TOKEN`/`WA_PHONE_NUMBER_ID` quedaban vacíos → `run_once` cortaba temprano (línea 427 del dispatcher) y el log daba `checked=None due=None dispatched=None`. Por eso solo 1 WA se envió en toda la historia. **Fix:** el script ahora auto-carga el `.env` con `_load_env_file()` (setdefault, antes de importar el dispatcher). Verificado con `env -i`: ahora da `checked=2 due=0`. El dispatcher en sí estaba bien (ya tenía opt-outs garantizados, exclusión CEO/Florencia+CSV, cap 500, idempotencia) — el agente de la auditoría lo marcó como faltante porque auditó los endpoints API, no el path real de envío.

**Frontend (UnifiedCampaigns.tsx + ProposalsTab.tsx):**
- 5 fixes de texto/botón invisible (`#FFFFFF` sobre blanco): `MiniStat` (KPIs), PeriodPill, botón "Editar campaña" (estaba 100% invisible), burbuja WA draft, botón Guardar. (El bubble del chat 1391 NO se tocó: blanco sobre navy, legible.)
- `STATUS_LABELS` en español + `statusLabel()`, aplicado en tabla, cola WA y detalle.
- Comando SSH crudo eliminado de la UI → mensaje no técnico.
- "Push a Perfit" → "Programar email"; "Lanzar ya" → "Enviar ya" con **conteo real de destinatarios** (nuevo endpoint) antes de disparar.
- "Aprobar y crear borradores" → botón secundario outline "Crear borradores" (distinto del verde "Aprobar y programar" que sí envía).

**Backend (unified_campaigns.py):**
- `draft_content`: grounding completo (reusa `_fetch_context` + KB + `_validate_no_forbidden_terms` de proposals.py), saqué "cosmética coreana" hardcodeado, sender desde brand_context con fallback, valida y tira 422 si hay términos prohibidos. Cierra el vector de alucinación.
- `send-to-perfit`: idempotencia (no recrea si ya tiene perfit_id) + persiste el id ANTES de programar (no más zombies) + try/except en schedule.
- `launch-now`: no reenvía si ya `sent`.
- Nuevo `GET /{id}/recipient-estimate` (verificado: campaña 46 → email 9046).
- Guard defensivo `isinstance(parsed, dict)`.

**Código muerto borrado:** `BroadcastWizard.tsx` (719) + `InboundCampaignDetail.tsx` (496). Sin referencias rotas.

**Ronda 2 — contraste (reportado por Andrés: hover de fila se ponía negro):** el re-skin de colores había reemplazado varios fondos claros por navy `#0F172A`. Arreglados 15 lugares: **hover de fila** (UnifiedCampaigns.tsx:461, navy→KR_SOFT), 2 cajas de reenvío disabled, ChannelPill inactivo, 2 botones con texto navy sobre KR, chip "WA: fecha", chip de template (código), y en ProposalsTab: preview de email (header+body markdown), contenedor del editor de campaña (tenía texto navy sobre navy = invisible), chip de fecha ISO, indicador "Pensando", botón de chat, label "When"→"Etiqueta de fecha (visible)". Únicos `#0F172A` que quedan como fondo son chips/burbujas con texto claro explícito (legibles). Verificado en el bundle compilado (`#EEF0FE` presente, `crontab -l` = 0).

**Diferido con fundamento (NO se hizo):**
- Guards `brand_id` por-endpoint: NO explotable hoy (`_db()` abre la DB física del tenant vía `_resolve_db_path()`), regresión-risk por cero ganancia. Hacer como pasada separada testeada si se consolidan DBs.
- Refactor god-files (proposals.py 2173 líneas): refactor puro, riesgo de regresión, cero beneficio de usuario ahora.
- Migración completa de hardcodes (dominio/colores) a brand_context: requiere poblar brand_context primero para no romper emails que andan. El sender ya se migró con fallback.

**ACCIÓN PENDIENTE DE ANDRÉS:** ahora que el cron WA anda, **la campaña 45 ("Energía Real…") dispara mañana 18/06 09:00 ART** y la 46 ("El intestino…") el 20/06 09:00 ART, ambas con template fallback `kr_marketing_link`. Confirmar que son envíos intencionales o desprogramarlas. Caveat: KR tenía un bloqueo Meta-side de WA (code 2 / app de terceros en la WABA, ver [[project_kr_wa_token_dead]]); ahora el cron correrá y logueará el error real por destinatario si Meta sigue rechazando — la entrega real depende de resolver eso en Meta BM (la 46 igual tiene 0 teléfonos).
</content>
</invoke>
