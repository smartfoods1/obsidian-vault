---
date: 2026-05-30
type: design-spec
tags: [smartbrain, b2b, multi-tenant, git-submodule, refactor, korean-root, smart-foods]
status: diseñado-pendiente-build
---

# B2B Core compartido (submódulo git) — SF + KR

> **Objetivo:** que el área B2B sea **idéntica en SF y KR y se mantenga así**, vía un repo compartido `b2b-core` consumido como submódulo git por ambos VPS.
>
> **Decisión (30 may 2026):** KR = fuente de verdad del B2B. Odoo y Copiloto son **features huérfanas** (ya no se usan) → se BORRAN de SF, no se preservan. Esto elimina la "bifurcación" y hace el B2B genuinamente común. Build DIFERIDO — ejecutar con go explícito de Andrés. Fase 1 no toca prod.

## Hallazgos del análisis (30 may 2026)

- SF y KR son **repos git separados** (`smartfoods1/smartbrain` branch `multi-tenant` vs `KRsrl/KRBRAIN` branch `korean-root`), con backport **a mano** → re-divergen siempre.
- Ambos ya usan arquitectura `dashboard/packages/`. KR lidera features B2B (commit "guided Google Places scraper wizard"); SF backporteaba de KR.
- **Routers backend B2B (`packages/b2b/backend/routers/`):**
  - Común: `crm.py`, `zona_mapping.py`
  - Solo SF (HUÉRFANOS → borrar): `odoo_b2b.py`, `copiloto_leads.py`, `copiloto_plantillas.py`
  - Solo KR (CANÓNICOS → adoptar): `outreach.py`, `outreach_templates.py`, `prospecting.py`, `meetings.py`, `invoice_ocr.py`, `email_outreach.py`
- **Frontend:** divergió. SF movió `Crm.tsx` a `packages/b2b/frontend/`; KR lo tiene en `pages/`. `components/crm/`: 18 idénticos, 9 difieren, `LeadWizard.tsx` solo-SF (huérfano), `ProspectingWizard.tsx` solo-KR (canónico).
- **Skills:** `b2b_prospecting` (7 archivos) + `outreach_engine` (5 archivos). Difieren 7; KR canónico. ⚠️ `outreach_config.py` difiere y **DEBE seguir difiriendo** (config por tenant).
- Ninguno de los `packages/b2b` es git propio todavía (`NO_GIT`).

## Qué entra / qué NO entra al `b2b-core`

**ENTRA (lógica/features, versión KR canónica):**
- `packages/b2b/backend/` (routers: crm, outreach, outreach_templates, prospecting, meetings, invoice_ocr, email_outreach, zona_mapping)
- Frontend B2B: `components/crm/*` + `Crm.tsx` (consolidar en `packages/b2b/frontend/`)
- Skills B2B: `b2b_prospecting/`, `outreach_engine/` (sin `outreach_config.py`)

**NO ENTRA (per-tenant, jamás se comparte):**
- `outreach_config.py`, `brand_context`, las `.db`, credenciales, `deployment_config.json`, env.
- Estos quedan en cada repo y los lee el core por interfaz/parámetro, no hardcodeado.

**SE BORRA de SF (huérfano):**
- routers `odoo_b2b`, `copiloto_leads`, `copiloto_plantillas`
- page `OdooCrm.tsx`, componente `LeadWizard.tsx`
- `packages/b2b/frontend/Crm.tsx` viejo de SF (reemplazado por el canónico de KR)

## Arruga técnica: submódulo = 1 directorio

El B2B vive en 3 lugares (`packages/b2b/`, `frontend/src/components/crm/`, `skills/`). Solución: **consolidar todo el B2B canónico en `packages/b2b/` como paquete full-stack** (`backend/` + `frontend/` + `skills/` adentro), y que ESE único dir sea el submódulo `b2b-core`. Requiere actualizar import paths de los consumidores (pages que importan `components/crm`: en SF `OdooCrm`(se borra)/`WhatsAppPage`; en KR `Campaigns`, `Crm`, `WhatsAppPage`, `B2CCustomers`).

## Plan de migración por fases

| Fase | Qué | Riesgo prod | Aceptación |
|---|---|---|---|
| **1. Crear `b2b-core`** | Extraer el B2B canónico de KR a un repo nuevo `b2b-core` con layout final (`backend/`/`frontend/`/`skills/`). Solo staging. | **Cero** (no toca ningún VPS) | Repo arma; árbol de archivos definido |
| **2. KR consume submódulo** | Reestructurar KR para consumir `b2b-core` en `packages/b2b/` (mover components/crm + skills adentro, fix imports). Contenido NO cambia (KR es canónico) → bajo riesgo. | Bajo | KR B2B anda igual; submódulo enlazado |
| **3. SF cutover** | Borrar huérfanos (Odoo/Copiloto/LeadWizard). Reemplazar B2B de SF por el submódulo. Fix imports. **Migrar schema DB** de SF para que matchee lo que espera el código de KR (tablas crm/outreach). | **Alto** | SF B2B anda con features de KR; datos de SF intactos; tenants OK |
| **4. Proceso anti-drift** | Cambios B2B van a `b2b-core` → ambos hacen `git submodule update`. Documentar en runbook. CI opcional. | — | Un cambio se propaga a ambos con 1 flujo |
| **5. Verificación** | Probar B2B punta a punta en los dos tenants; monitorear. | — | Checklist OK en SF y KR |

## Reglas de seguridad de ejecución

- Backup de cada repo + cada `.db` ANTES de tocar (los dos VPS ya tienen backups `.bak`, sumar uno fresco).
- Trabajar en branch, no en `main`/`multi-tenant`/`korean-root` directo.
- **Un VPS a la vez.** KR primero (bajo riesgo, es canónico), SF después (alto riesgo).
- Verificar tenant por tenant antes de pasar al siguiente.
- Rollback preescrito: revertir el submódulo + restaurar `.db` del backup.
- NUNCA mover config/datos/credenciales al core compartido.

## Preguntas abiertas (resolver al arrancar)

1. **¿Dónde vive `b2b-core`?** ¿Repo nuevo en `smartfoods1`, en `KRsrl`, o una org neutral? (Ambos VPS necesitan deploy key de lectura.)
2. ¿El schema B2B de SF (leads existentes) mapea limpio al de KR? Auditar antes de Fase 3.
3. ¿`specialandres` (3er tenant en VPS SF) usa B2B? Si sí, también hereda el core.

## Archivos clave (referencia)

- KR canónico B2B: `dashboard/packages/b2b/backend/routers/*` (KR `103.199.187.246`)
- Frontend B2B: `dashboard/frontend/src/components/crm/*` + `packages/b2b/frontend/Crm.tsx`
- Skills: `skills/b2b_prospecting/`, `skills/outreach_engine/`
- Huérfanos SF a borrar: `packages/b2b/backend/routers/{odoo_b2b,copiloto_leads,copiloto_plantillas}.py`, `pages/OdooCrm.tsx`, `components/crm/LeadWizard.tsx`

Relacionado: [[wizard-outreach-multitenant]] (el wizard de outreach se apoya en este core), Content Hub SaaS.
