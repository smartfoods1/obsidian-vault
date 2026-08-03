---
date: 2026-07-05
type: analisis
tags: [gondola, lead-machine, saas, inversor, growth, dfy, decision]
status: activo
---

# Góndola — Análisis de inversor / SaaS (5 jul 2026)

> Análisis sobre **datos reales de producción** (`/opt/lead-machine/leadmachine.db` en VPS `root@76.13.228.77`). OJO: la DB local de la Mac (`~/lead-machine/leadmachine.db`) es solo dev/test — el deploy la excluye del rsync. Siempre analizar la del VPS.

## Números reales (excluidas 28 cuentas test/deploysmoke/catalog + 5 del dueño)

- **25 marcas de alimentos reales** registradas. Oleadas: 23-jun (15), 5-jul (6); hueco de 9 días sin signups en el medio → adquisición 100% push del fundador, cero orgánico.
- **Activación superficie:** 76% (19/25) consumió y guardó ≥1 lead.
- **Activación de negocio:** 16% (4/25) contactó algún lead (Santana, Recado Salteño, Dani Gabaldón, Namaste).
- **Realización de valor:** 0/25 cerró góndola / reportó deal_value.
- **Retención:** ~0 (1/25 activa 2 días; nadie se relogueó entre 23/6 y 5/7).
- **Monetización:** **0 pagos MercadoPago, $0 ARS histórico.** Todos los `paid_credits` son regalados (cupones PLANTE/RECADO/ANDY50/GONDOLA10 + bonos + grants admin). **Willingness-to-pay NUNCA testeada.**
- **Costos variables:** ~USD 41 total → margen bruto potencial ~99%. El cuello NO es COGS, es demanda pagante.
- Cuentas con uso profundo: Planté (55 leads, todos en "visitar" — ni contactó), DMC Masala (12).

## Diagnóstico

No es falta de tráfico. El funnel se muere entre **"guardó lead" → "usó lead para vender"**. El aha real es *cerrar una góndola*, no *ver 5 leads*. El valor se materializa semanas después, fuera de la app, sin loop de re-enganche (`recovery_log=0`). Free tier de 5 leads sacia curiosidad pero no produce un WIN. Producto ciego a su propio outcome (no captura venta/deal_value).

## Veredicto

- **Como venture: PASS.** 0 pagos + 0 retención = sin señal de PMF. Core (Places+Gemini) commodity, modelo one-off sin MRR, TAM AR chico.
- **Como negocio de dueño: sí, vía DFY.** El único motor de ingreso año-1 con matemática defendible es el servicio gestionado, no los créditos self-serve.

## Expectativas de facturación año 1 (todo condicionado a encender GTM)

| Escenario | Total año 1 | De dónde |
|---|---|---|
| Piso (nada cambia) | $0–450k ARS | trayectoria real hoy |
| **Base (GTM real)** | **$3–6M ARS (~USD 2–4k)** | 80–90% de 4–7 DFY a $350k+; self-serve $0–1M |
| Optimista self-serve | millones | **hipótesis no validada** — requiere caso de éxito que hoy no existe |

Run-rate mes 12 (base): ~$600k–1,2M ARS/mes, mezcla DFY + créditos, NO MRR puro.

## Acciones (prioridad)

1. **P0 — Cobrar un peso real esta semana:** vender DFY a mano por WhatsApp a las 6 calientes (Santana, Recado, Gabaldón, Namaste, Planté, DMC). Desambigua en días si el bloqueo es funnel o demanda. Costo $0.
2. **P0 — Frenar el rediseño de frontend.** El diseño no es el cuello (76% activa). Rehacerlo el 4-5/7 en vez de vender = evitación del test comercial.
3. **P0 — Instrumentar outcome loop** (pipeline nuevo→contactado→…→EN GÓNDOLA + monto). Sin esto no hay testimonio ni iteración.
4. **P1 — Nurture WhatsApp/email atado al calendario de valor** (recovery_log=0 hoy). Simular al account manager.

## Riesgo de fondo

Puede que las marcas chicas de alimentos AR no puedan/quieran operar venta mayorista aunque tengan el contacto (canal histórico a pulmón). Si es así, ningún ajuste de funnel salva el self-serve y el negocio real es DFY/consultoría. La venta manual (acción 1) lo resuelve gratis.

Relacionado: [[handoff]]
