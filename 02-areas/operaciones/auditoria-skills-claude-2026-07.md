---
date: 2026-07-06
type: auditoria
tags: [claude-code, skills, opus, tooling]
status: ejecutado
---

> **Ejecutado el 2026-07-06**: las 3 fases del plan se aplicaron el mismo día. smartcomfy convertida a skill válida (`smartcomfy/SKILL.md` + `references/pipelines.md`, token de Jupyter removido), `learned/` eliminado, `skill-creator` local movida a `~/.claude/skills-disabled/` (duplicada con el plugin anthropic-skills; el trío seo-audit/email-sequence/content-strategy se dejó por ser parte de un pack cross-referenciado — ver README en skills-disabled). Gates + playbooks agregados a los 4 commands y 6 skills de ops; few-shot + triggers bilingües + guardas de producto en las 8 de marketing. Todas las skills re-registradas OK por el harness.

# Auditoría de skills Claude Code — Opus-proofing (jul 2026)

Objetivo: endurecer las skills custom para que un modelo menos capaz (Opus) las ejecute igual de bien que Fable. Principio: Fable rellena los huecos de una skill con criterio propio; Opus ejecuta lo que está escrito. Cada decisión que la skill deja abierta es un punto de divergencia.

## Notas por skill (robustez ante modelo débil, /10)

| Skill | Nota | Fix #1 |
|---|---|---|
| klaviyo | 8 | Ya es el gold standard: reglas duras + checklist + references/. Solo falta gate post-schedule (verificar status Scheduled vía API) |
| shopify-discount-codes | 8 | Playbook de errores para userErrors (TAKEN, INVALID) con fix exacto por caso |
| food-cpg-marketing | 8 | Checklist de verificación post-copy (claims ANMAT, formato doypack, 30% beta-glucanos) |
| reel-editor | 7 | Gates intermedios: verificar whisper model existe antes de arrancar; ffprobe del output final (duración ≤90s) |
| b2b-mayorista | 7 | Agregar guarda NUNCA-cápsulas + gate de seguimiento post-propuesta |
| investor-relations | 7 | Few-shot de monthly update completo + targets numéricos CPG |
| deploy-vps (cmd) | 7 | Si `is-active` ≠ active → journalctl -n 20 y NO declarar éxito; grep de .env en el tar antes de subir |
| whatsapp-commerce | 6 | Cart recovery como checklist exacto (1h/24h/48h/72h con copy) + targets numéricos de métricas |
| ecommerce-shopify | 6 | Ejemplo completo de product page (hero, benefit ladder, FAQ) |
| image-gen-contextual | 6 | Copiar el prompt exacto de Stage 1 al SKILL.md (hoy vive solo en el script); gate de fonts presentes |
| sync-sheet (cmd) | 6 | Documentar orden fijo de ejecución + dependencia de resumen_semanal; gate de credenciales gspread |
| atp-enrich | 6 | Convertir "derivar query" y "refinar brief" en reglas if/then; verificar HTTP 200 post-enrich; typo `mcp__Claude_in_Chrome__` → `mcp__claude-in-chrome__` |
| influencer-outreach | 5 | Brief de ejemplo completo (few-shot) con do's/don'ts ANMAT |
| run-ci (cmd) | 5 | Tabla de módulos con tiempos y outputs esperados + gate post-pipeline (archivo de report existe, Sheet actualizado) |
| weekly-briefing (cmd) | 5 | Gate final: contar módulos exitosos, si <2 alertar; documentar formato del resumen WA |
| brand-bible | 4 | Sección "Reglas inquebrantables" (no inventar datos → [VERIFICAR], versionado, único por tenant) + gate post-upload (GET y validar version) |
| csv-data-summarizer | 4 | Árbol de decisión explícito (cómo clasificar sales vs customer data por columnas) en vez de prosa ALL-CAPS |
| marketing-attribution-tiendanube | 3 | Partir los 10 pasos en 3 fases con gate SQL verificable al final de cada una; no asumir acceso al commit 51d527d |

## Defectos transversales (ordenados por impacto)

1. **Sin gates de verificación post-comando** (~75% de las skills de ops). Ejecutan SSH/API y no chequean exit status ni output esperado. Patrón fix: `correr X → esperar Y → si no, Z` después de cada paso que muta estado.
2. **Prosa vaga en decisiones críticas** ("refinar el brief", "derivar query", "determinar qué analizar"). Fix: if/then explícito o pseudo-código.
3. **Cero few-shot en skills generativas** (7 de 8 skills de marketing tienen estructura pero ningún par input→output). Un modelo débil imita ejemplos mucho mejor que instrucciones abstractas.
4. **Descriptions con triggers débiles o solo en inglés**. El usuario pide en castellano; si la description no tiene las frases literales ("propuesta mayorista", "armame un reel"), la skill no se invoca. reel-editor y shopify-discount-codes son el modelo a copiar.

## Hallazgos estructurales

- 🔴 `~/.claude/skills/smartcomfy.md` — archivo suelto, NO es dir con SKILL.md → **nunca se carga**. Contenido valioso (pipeline IC-Light/Flux) muerto. Convertir a `smartcomfy/SKILL.md` + `references/`.
- 🟡 `~/.claude/skills/learned/` — dir vacío sin propósito. Borrar o documentar.
- 🟡 Colisiones de nombre con plugins: `skill-creator`, `code-reviewer`, `content-strategy`, `seo-audit`, `email-sequence` existen local Y en plugins (anthropic-skills, marketing, small-business). Ambigüedad de invocación.
- 🟡 Staleness de contexto de negocio: varias skills (b2b-mayorista, investor-relations, marketing-attribution) asumen operación normal de SF. Post-disolución, agregar nota "verificar vigencia con Andrés / adaptar a KR".
- ✅ Sin referencias a gemini-2.0-flash (verificado con grep — un agente lo reportó como falso positivo).

## Plan de ejecución propuesto

1. **Fase 1 — cadáveres y colisiones** (15 min): convertir smartcomfy, limpiar learned/, renombrar o eliminar skills locales que colisionan con plugins.
2. **Fase 2 — gates + playbooks** (las 8 skills de ops): agregar sección de verificación post-paso y errores conocidos → fix exacto.
3. **Fase 3 — few-shot + descriptions bilingües** (las 8 de marketing): 1 ejemplo completo por skill generativa + frases gatillo literales en español.
