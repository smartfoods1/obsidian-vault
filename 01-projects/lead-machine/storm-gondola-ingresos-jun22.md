---
date: 2026-06-22
type: project
tags: [gondola, lead-machine, ingresos, monetizacion, storm, validacion]
status: validacion
derivado_de: "[[brand-gondola]]"
---

> Generado con metodología STORM (harness multi-agente: 8 lentes + 3 red team + síntesis = 12 agentes). Insumo de decisión, no decisión tomada. Dato de DB verificado a mano por Andrés/Claude el 2026-06-22.

# STORM — Góndola y sus formas de generar ingresos

## 0. El dato que ancla todo (verificado en `leadmachine.db`)

- **1.027 leads guardados, 1.024 en "nuevo" (99,7%).** 1 contactado, 1 a visitar, 1 descartado.
- **0 outcome cargado, 0 deal_value, 0 wa_conversations, 0 "won" en segment_stats.**
- 30 brands. (Caveat: es la DB local/dev — `mp_payments=0` — prod en VPS tiene DB separada; la facturación real no se confirmó desde acá.)

**Implicancia:** Góndola captura **descubrimiento** (input: qué comercio merece tu producto) y es **ciega al output** (resultado: abrí/repuse la cuenta). El que paga, paga por el output. Los 3 streams premium (#3 inteligencia, #5 success fee, #6 recompra) se construyen sobre una base que hoy está vacía. El cuello de botella real no es elegir el modelo de ingreso: es **cerrar el loop del output**.

## 1. Veredicto

Góndola **no es una empresa de software, es un servicio de canal de alto margen con una herramienta adentro** — el STORM padre tenía razón y las 8 lentes lo confirman. Hay **dos negocios peleando por el roadmap**: un cash business de prospección (streams 1-2-3, techo USD 0,5-1M ARR, correcto) y un riel transaccional embrionario (5-6, lo único venture, baja probabilidad de ejecución). Dejá de fantasear con el múltiplo SaaS y la suscripción. El único MRR honesto nace de la **recompra (#6)**, no de cobrar acceso al buscador.

## 2. Ranking de las 6 formas de generar ingresos

| # | Stream | Score | Naturaleza | Veredicto | Por qué |
|---|--------|:---:|---|---|---|
| 1 | **DFY / Gestionado** | 8/10 | servicio | **doblar** | Único stream con WTP CALIENTE validada (KR paga ~$1,4M/mes por esto, no por packs). Resuelve el JTBD real ("abrime cuentas"). Contracara: headcount lineal, topa en cliente #8-10, reintroduce la dependencia del fundador. Es tu ancla de CASH, NO tu motor de escala. Subir piso de $350k. |
| 2 | **Packs self-serve** | 7/10 | software | **mantener** | Única CAJA real hoy, margen ~90%, cobrabilidad perfecta (prepago MP). PERO one-and-done (LTV ≈ 1 pack), el 5% convierte tibios que ya te conocen, el frío convierte MÁS bajo. Motor de adquisición y lead-magnet para upsell a DFY, no la tesis. |
| 3 | **Recordatorios de recompra** | 6/10 | dato | **doblar** | El sleeper. La guita B2B está en el 2º/3er pedido. Único camino legítimo a recurrencia (la recurrencia de USO precede a la de COBRO), captura el único dato no-replicable (re-pedido verificado), semilla obligada de #5. Hoy 100% hipótesis: 0 outcomes en DB. Inversión de producto #1. |
| 4 | **Inteligencia de canal / benchmarks** | 4/10 | dato | **rediseñar** | El MÁS sobrevalorado: creés que es el moat y es lo más débil. Foso de agua: (a) base vacía (0 won, autoreportado), (b) gate n≥5 deja casi todo el grid AR en blanco, (c) sell-through inmedible en canal informal sin POS. No es SKU vendible: es un LAYER de percepción de precio en el paywall, que se densifica SOLO cuando #6 capture re-pedidos. |
| 5 | **Riel transacción + success fee / % GMV** | 3/10 | software | **diferir** | Paradoja: lo ÚNICO venture-scale (take-rate sin humanos, resuelve sell-through) Y hoy estructuralmente incobrable (la transacción vive en WhatsApp/efectivo, a veces ARCA; el cliente no tiene incentivo para meterla en la app). NO matar: es el norte arquitectónico. Se enciende DESPUÉS de que #6 pruebe que el re-pedido pasa por adentro. |
| 6 | **Suscripción recurrente** | 2/10 | software | **matar** | Error de ARQUITECTURA, no "todavía no". Recurrencia de cobro sobre uso EPISÓDICO (prospectás en ráfagas, agotás zona, no volvés) = churn del mes 2. WTP validada = CERO (ya sacaste el badge mensual). Saltear el escalón. |

## 3. Modelo de ingresos recomendado — barbell de dos motores (NO un continuo)

**Motor de CASH (hoy):**
- **DFY como producto ancla**, piso subido a **$500-600k/mes** (KR ya paga ~$1,4M; $350k está regalado).
- Tier intermedio **"DFY Arranque" ~$350-400k** (setup + primeras 10-15 cuentas trabajadas) para quien quiere manos pero no banca el ticket full.
- Tope **8-10 cuentas DFY por persona**; escalás contratando SDRs, no usuarios.
- **Packs** = filtro/lead-magnet que calienta el upsell a DFY. Renombrar de "X leads" a **"X PDV calificados listos para abrir"** (mismo producto, eje de valor en OUTPUT). Inteligencia de canal embebida en el paywall de Pro/Expansión como justificador de precio (no SKU aparte).

**Motor de FUTURO (única apuesta venture):**
- Construir el puente **#6 → #5**. Instrumentar YA la **captura de outcome obligatoria** en el CRM (botón gordo "gané/perdí esta cuenta + valor").
- Después, recordatorios de recompra por WhatsApp.
- Solo cuando N re-pedidos pasen naturalmente por adentro, encender el success fee sobre ESE GMV ya capturado.

**Números base:** 8 DFY a ~$450k promedio = ~$3,6M ARS/mes (~USD 2.500) + packs como capa variable. #3 y #5 NO facturan solos hasta que el loop de output esté instrumentado.

## 4. Qué doblar / qué matar

**Doblar:** DFY (ancla de cash) · Recordatorios de recompra #6 (inversión de producto #1) · Instrumentación del OUTPUT (botón "gané/perdí + valor") · Conversión free→pago vía AHA real (meter la línea de inteligencia en los 5 gratis).

**Matar:** Suscripción recurrente self-serve (#4) · La fantasía de que la inteligencia de canal es EL moat y un SKU vendible · El target 8-15% como supuesto sin experimento · Cobrar success fee antes de tener el riel.

## 5. Riesgos asesinos

1. **[fatal] Demanda FRÍA nunca validada.** El 5% es tráfico cálido que ya conoce a Andrés; con frío pago baja a 1-2% y el CAC se come el ticket. El self-serve no eliminó la dependencia del fundador, le puso una UI. → Test de demanda fría aislada antes de gastar en ads.
2. **[fatal] One-and-done.** El pack se consume una vez por zona, LTV ≈ 1 pack, TAM de bajas centenas que se agota en meses. → #6 como razón estructural de volver, antes de escalar adquisición.
3. **[fatal] Loop de output roto** (0 outcomes / 1027 leads). El dato propietario nunca se acumula. → Captura de "ganado/perdido + valor" obligatoria esta semana.
4. **[alta] Commoditización del motor** (Places+Gemini) en 12-18 meses mientras el dato vendido caduca. → El único activo no-replicable es el re-pedido verificado; carrera contra reloj.
5. **[alta] Riel imposible por física del canal** (efectivo, sin POS, ARCA). #5 puede ser inejecutable, no solo difícil. → Test de falsabilidad en 90 días.

## 6. Experimentos a correr YA (gates de decisión)

| Pregunta | Experimento | Éxito | Plazo |
|---|---|---|---|
| ¿La demanda fría compra o es solo tu red cálida? | Ads ($50-100k) a audiencia 100% fría → freemium; medir conversión del frío aislada | ≥3% (si <2%, negocio = relación pura) | 3 sem |
| ¿El 5% es framing/AHA o no creen en la calificación? | A/B: 5 leads crudos vs 5 con inteligencia + zona guiada; renombrar a "PDV calificados" | B ≥1,5x A | 2 sem |
| ¿Hay segunda compra? | Retroactivo: % de Buscador→Pro/Expansión y a qué intervalo | Recompra ≥25% (si <10%, one-and-done) | 1 sem |
| ¿Registran el OUTPUT? | Botón outcome obligatorio + cerrar 3-5 DFY a mano forzando registro | ≥10 outcomes con deal_value | 4 sem |
| **¿La transacción puede pasar por adentro?** (test venture binario) | Recordatorios de recompra + cerrar re-pedido en 1 tap con success fee chico | ≥3 marcas pasan un re-pedido y pagan el fee sin quejas | 90 días |

## 7. Techo realista

- **Base (alta prob.):** cash business AR-only, USD 25-40k MRR (~USD 0,3-0,5M ARR), 30-55 clientes, 18-24 meses. Idéntico al padre.
- **Venture (baja prob., <20%):** solo si el puente #6→#5 funciona y la transacción pasa por adentro — rompe el techo con take-rate sobre GMV recurrente. Depende de superar la física del canal informal.
- **Malo (si la fría no valida):** topa en cliente #8-10 a mano, ~USD 8-12k MRR, agencia de un hombre.

## 8. Recomendación final

Aceptá la verdad incómoda que coinciden las 8 lentes y los 3 red-teams: **esto NO es una startup de software, es un servicio de canal de alto margen con una herramienta adentro — y está perfecto, pero dejá de perseguir el múltiplo SaaS.** Tu sesgo #1: creer que el moat es la inteligencia de canal — es lo más débil del stack, foso de agua sobre DB vacía. Sesgo #2: creer que el self-serve te liberó de la dependencia del fundador que marcó a Smart Foods — no, le puso UI; los dos streams con WTP real descansan en RELACIÓN, no en producto.

**La jugada:** DFY = motor de cash YA (subí el piso). Packs = filtro/lead-magnet con inteligencia embebida como justificador de precio. Matá la suscripción sin culpa. Toda tu energía de producto en UNA cosa: **instrumentar el OUTPUT** (botón "gané esta cuenta") y construir el **recordatorio de recompra (#6)** — único camino a recurrencia honesta y único dato que no te copian.

**El test que decide tu próximo año es binario, no incremental:** en 90 días, ¿pasás 3 re-pedidos por adentro de la app con success fee y sin quejas? Si sí, tenés tesis venture y vale levantar capital. Si no, es lifestyle business excelente — facturás, vivís bien, cerrás el capítulo del unicornio sin drama. **No construyas nada de Fase 2 (#4, #5) hasta tener ese loop de output prendido.** Sin él, todo lo premium es a confianza, y la confianza es lo único que no podés volver a comprar.
