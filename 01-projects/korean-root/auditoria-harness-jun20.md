---
date: 2026-06-20
type: auditoria
tags: [korean-root, smartbrain, harness, llm-gateway, observabilidad, content-judge, evals, confiabilidad]
status: activo
relacionado: [[harness-llm-gateway-handoff-2026-06-20]]
derivado_de: [[harness-llm-gateway-handoff-2026-06-20]]
---

> Auditoría de ingeniería independiente, **read-only y adversarial**, del "harness engineering" de SmartBrain Korean Root. Tratamos el handoff [[harness-llm-gateway-handoff-2026-06-20]] como hipótesis a verificar, no como verdad. Cada afirmación está confirmada por código (`ruta:línea`), salida de comando o filas de DB sobre el sistema real del VPS `103.199.187.246` (branch `korean-root`). Corrí los 3 runners sancionados (gateway self-test, content-judge evals det+LLM, bot baseline); único efecto de escritura = unas pocas filas de `api_usage` que esos runners generan por diseño. No toqué código, DB de negocio ni servicios.

# Auditoría de Harness — SmartBrain Korean Root

## Veredicto global: L2 (Gestionado) en diseño — L1–L2 en realización verificada

El harness es **ingeniería real, no humo**: el gateway está endurecido de verdad (retry/backoff, finish_reason, truncation-retry, fail-safe), el ContentJudge es tenant-agnóstico y a prueba de fallos, los evals corren y pasan, y el cerebro del bot está grounded. Pero es un harness que fue **construido y todavía no operado**: el enforcement está apagado, la tabla de telemetría tiene 8 filas, el fallback cruzado es **código muerto en KR**, y no hay CI, backups ni rollback. Parece maduro por la calidad del código; no ha *demostrado* madurez en producción. La distancia entre "está cableado" y "está funcionando y verificado en prod" es donde se cae casi una banda entera.

Escala: **L0** Ad-hoc · **L1** Básico (existe pero parcial/manual) · **L2** Gestionado (consistente, observable) · **L3** Endurecido (fail-safe, verificado, reversible) · **L4** Auto-mejorante (evals en CI, gating automático, feedback loop).

---

## Tabla por dimensión

| Dim | Nivel | Evidencia concreta | Gap principal |
|---|---|---|---|
| **(a) Consolidación gateway** | **L3** | `backend/llm_client.py`: `llm_call:376`, `allm_call:480`, `allm_chat:616`, `or_tool_chat:655`. 18 archivos importan el gateway, 25 sitios `track=`. Self-test live: `chain=['openrouter']`, `✓ SUCCESS`. Bypasses reales (`chatbot_engine._do_call:948`, `packages/b2b/.../invoice_ocr.py:90` genai, image_generators) **requieren GEMINI_API_KEY → muertos en KR**. `proposals.py`/`sales_ai.py` tienen constantes de URL muertas pero llaman al gateway. | Los bypasses muertos en KR están **vivos en SF** (destino de replicación). API backward-compatible = reversible. |
| **(b) Observabilidad** | **L2** | `backend/api_tracker.py`: tabla `api_usage` con todas las columnas, `track_usage` fail-safe (try/except, nunca lanza), tabla de pricing, ALTER idempotente. Endpoints `GET /costs/summary`, `/{brand_id}/costs` en `packages/core/.../brands_admin.py:171,254`. **Pero: 8 filas totales, 3 de ~18 ops** (`chatbot.ask`, `content_judge`, `chatbot.flow_ai_step`), todas de hoy 00:36–02:05, costo total **$0.03**. `ops.db` y `ops_korean-root.db` = mismo inode (1322789). | 15 ops cableadas con `track=` **sin una sola fila** → cobertura efectiva no probada. Sin volumen histórico. |
| **(c) Confiabilidad** | **L2** | Retry+backoff `[0,2,5]`, `MAX_RETRIES=3`, en sync **y** async (`_openrouter_acall:416`). `_retryable`: 5xx/429/408. Truncation-retry (`_bump:148`). Tracking y `judge()` ambos fail-safe. | **Fallback cruzado INERTE en KR**: sin GEMINI/ANTHROPIC key, `_provider_chain` devuelve `['openrouter']` solo → **OpenRouter es SPOF duro**. El feature estrella de confiabilidad no puede dispararse nunca. |
| **(d) Verificación & evals** | **L2** | `run_content_judge_evals.py` live: **determinística 18/18, semántica 12/12** (con LLM vivo: kbeauty→hard_block, adaptógeno→hard_block, ingrediente-inventado→hard_block, soft-tone→soft_warn). Gate determinístico 100% reproducible (sin red). 30 golden cases desde incidentes reales. | **Sin CI, sin cron, 100% manual.** Con `--no-llm` el runner marca `[PASS]` aunque `obs≠exp` ("llm no disponible") → infla el verde. Evals validan *lógica* sobre fixtures sintéticos, no la data de prod. |
| **(e) Guardrails / seguridad contenido** | **L2** | `backend/content_judge.py` tenant-agnóstico confirmado (literales de marca solo en docstrings `:73,88` y `__main__` `:1057–1112`, **cero en lógica ejecutable**). `judge()` fail-safe verificado (`:916` outer try, `:990` red última → degrada a soft_warn). Brand_context real **poblado** (forbidden_claims, format_rules, mushrooms_we_do_NOT_sell, donts, portfolio_critical, words_no). Enforcement de incidentes críticos ya vive en la capa de dispatch (Perfit SDK / `_sanitize_param`). | **ContentJudge bloquea NADA**: shadow puro, **0 enforcement**, y degrada **fail-open** si crashea. Landmine para cuando prendan a2.3. |
| **(f) Grounding / anti-alucinación** | **L2** | `bot_brain_baseline.sh` live: KB-grounded (ingredientes Limonada correctos), anti-halluc (niega Melena/Reishi, dispara `search_kb`), tool-order (dispara `lookup_order`). Cero K-beauty. Capa groundedness vs KB en el juez (`content_grounding.fetch_kb_block`). | En generación de contenido, `unsupported_claims → soft_warn` (nunca bloquea) y depende de OpenRouter vivo. Grounding probado en el bot, advisory en el resto. |
| **(g) Reproducibilidad & deploy** | **L1** | Branch sincronizado con `origin/korean-root`, commits del harness pusheados. **Sin secretos hardcodeados** en archivos del harness (todo `os.environ`). Servicio `active`, "Application startup complete" a las 23:05 (post último deploy). | **`_harness_backups/` NO existe** (claim falso; solo `.backups/` viejo). Sin script de deploy, sin runbook, sin rollback. Working tree sucio (submódulo `packages/b2b` + `CLAUDE.md`/`docs/` untracked). |
| **(h) Testabilidad aislada** | **L2** | 3 runners independientes que no tocan prod: `run_content_judge_evals.py` (hermético, siembra su propia DB fixture), `bot_brain_baseline.sh` (corre el cerebro **sin enviar WA**), self-tests `__main__` en `llm_client.py` y `content_judge.py`. | El bot baseline **no tiene asserts** (juicio a ojo, sin exit-code). La capa LLM del eval pega a la red y escribe `api_usage` (no 100% offline). |

---

## Top 5 riesgos priorizados

1. **OpenRouter = single point of failure (fallback es código muerto).** Toda la IA de KR cae si OpenRouter da 5xx persistente; los 3 reintentos se agotan y no hay segundo proveedor. **Fix (1 línea):** cargar `GEMINI_API_KEY` (y/o `ANTHROPIC_API_KEY`) en `/etc/smartbrain/.env` de KR → `_provider_chain` pasa de `['openrouter']` a `['openrouter','gemini']` y el fallback ya escrito se activa. Agregar test que mate OpenRouter y verifique la caída al 2º proveedor.

2. **Observabilidad sin evidencia (8 filas, 3/18 ops).** No se puede afirmar "observable" cuando 15 operaciones nunca registraron una fila. **Fix:** ejercer una vez cada path silencioso (script de smoke), confirmar que emiten, y exponer `get_brand_costs` en el frontend. Hasta entonces, la observabilidad es una promesa, no un hecho.

3. **ContentJudge no protege nada + 0 veredictos + fail-open.** `judge_verdict_json` existe pero **0 de 28 campañas** lo tienen poblado: el shadow no generó *una sola* evidencia, que era literalmente su propósito. **Fix:** (a) aprobar N campañas reales para juntar veredictos; (b) **prender el gate determinístico a enforcement** (es reproducible y de bajo riesgo) dejando la capa LLM advisory; (c) decidir fail-open vs fail-closed **antes** de a2.3 — hoy un bug del juez deja pasar todo.

4. **Contradicción de data viva en prod.** `voice.words_yes` incluye `"adaptógeno"` mientras `portfolio_critical`/`donts` lo prohíben. La capa determinística **no puede** marcarlo (está whitelisted); solo lo agarra el LLM, que además no bloquea. **Fix (1 UPDATE):** sacar `"adaptógeno"` de `words_yes` en el `brand_context` de KR → el gate duro lo cubre solo.

5. **Sin CI / sin backups / sin rollback / evals a mano.** Un deploy que rompa el juez no tiene red automática que lo agarre. **Fix:** git-hook o cron que corra `run_content_judge_evals.py --no-llm` + bot baseline con exit-code gating en cada deploy; snapshot a `_harness_backups/` pre-deploy; runbook de rollback (revert + restart de `smartbrain-api`).

---

## Lo que el handoff afirma pero NO pude verificar / encontré distinto

- **`_harness_backups/` + "patrón de deploy seguro, rollback"** → **No existe.** Solo `.backups/wizard-quincenal-2026-05-21` (viejo). No hay script de deploy ni runbook. `deployment_config.json` es un manifiesto de feature-flags, no un procedimiento.
- **"Cross-provider fallback OpenRouter→Gemini/Anthropic"** → existe en código, **inerte en runtime KR** (`chain=['openrouter']`, ambas keys NOT SET, confirmado por el self-test).
- **"~18 call-sites migrados con track="** → 18 archivos importan el gateway, pero **solo 3 ops emitieron filas**. Los otros 15 están cableados *sin prueba* de que disparen.
- **"Tracking sin dashboard/reporting consumiéndolo"** → **parcialmente falso**: `brands_admin.py` expone `/costs/summary` y `/{brand_id}/costs` con `cost_per_post`. La capa API sí consume; lo que falta es data y render en UI.
- **Shadow "persiste el veredicto"** → la columna existe pero **0/28 campañas** pobladas. El shadow nunca corrió sobre una campaña real.
- **"Semánticos 12/12"** → cierto **solo con LLM vivo**. Con `--no-llm`, el runner marca `[PASS]` aunque `obs≠exp` → el verde reproducible (sin red) es solo la capa determinística.
- **`deployment_config.json`** declara `gemini.enabled:true` / `anthropic.enabled:true` con keys que **no existen** → manifiesto ≠ runtime.

---

## Roadmap de 3 pasos para subir a L3

1. **Cerrar el SPOF y hacer real el fallback** *(sube Confiabilidad → L3)*: cargar las API keys de fallback en KR; test de inyección de fallo OpenRouter→2º proveedor. Es la corrección de mayor impacto y menor esfuerzo del informe.
2. **Probar telemetría + prender el gate determinístico** *(sube Observabilidad y Guardrails)*: ejercer los 15 ops mudos para poblar `api_usage` y exponerlo en UI; flip del gate determinístico de shadow→enforce (fail-closed, reproducible); juntar ≥1 semana de `judge_verdict_json` antes de enforzar la capa LLM. Arreglar `words_yes`.
3. **Automatizar** *(sube Verificación y Reproducibilidad hacia L3/L4)*: CI/git-hook que corra evals `--no-llm` + bot baseline con exit-code en cada deploy; `_harness_backups/` snapshot pre-deploy; runbook de rollback. Esto es lo único que separa este harness de "auto-mejorante" (L4).

---

## Evidencia cruda (apéndice)

**Gateway self-test (live, KR):**
```
USE_OPENROUTER: True | GEMINI_API_KEY: NOT SET | ANTHROPIC_API_KEY: NOT SET
chain for gemini-2.5-flash: ['openrouter']
llm_call ok provider=openrouter model=gemini-2.5-flash tok=5/1 finish=stop 1593ms  ✓ SUCCESS
```

**api_usage (8 filas, mismo inode ops.db/ops_korean-root.db):**
```
chatbot.ask           korean-root  5  $0.0266  fails=0
content_judge         korean-root  2  $0.0023  fails=0
chatbot.flow_ai_step  korean-root  1  $0.0000  fails=0
```

**Content-judge evals (LLM vivo):** Determinísticos 18/18 PASS · Semánticos 12/12 concuerdan (kbeauty hard_block, adaptógeno hard_block, ingrediente-inventado hard_block, soft-tone soft_warn).

**Bot baseline (live):** KB-grounded ✓ (ingredientes Limonada correctos) · anti-halluc ✓ (niega Melena/Reishi, `search_kb`) · tool-order ✓ (`lookup_order`).

**Shadow:** `unified_campaigns.judge_verdict_json` existe (col 39) · 28 campañas, **0** con veredicto · wiring no-bloqueante vía `background_tasks.add_task(shadow_judge_and_store, ...)` en `proposals.py:1512,1858` · cero enforcement.

**Commits del harness (branch korean-root, pusheado):** `7762f7c` bot transport→gateway · `1cea732` ContentJudge SHADOW · `f2c488b` ContentJudge + golden evals · `7f73bba` observabilidad por-tenant (18 call-sites).
