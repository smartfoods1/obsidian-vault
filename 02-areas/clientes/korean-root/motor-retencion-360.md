---
date: 2026-06-07
type: diseño-sistema
tags: [korean-root, retencion, smartbrain, lifecycle, orquestacion, content-hub]
status: diseño-para-revisión
cliente: The Korean Root
derivado_de: auditoría de touchpoints Perfit + Salto Cuántico + unified_campaigns (jun 2026)
---

# Korean Root — Motor de Retención 360

> **Diseño para revisión de Andrés antes de tocar nada.** Principio rector: el motor NO agrega ruido — orquesta lo que ya existe y llena solo los huecos. Cero modificación a los flujos actuales.

## 0. El problema en una línea
KR tiene **38.280 compradores y una recompra de 19,8%** (1,32 órdenes/cliente) sobre un producto que *se consume y debería recomprarse*. La máquina de automatización existe (14 flujos Perfit + Salto Cuántico + broadcasts), pero **nadie es dueño del cliente que se enfría**: 6.652 "Por Perder" + 1.656 "En riesgo" no los trabaja ningún sistema. El motor cierra ese hueco sin tocar lo que funciona.

## 1. Principio rector — orquestar, no agregar
El error a evitar es sumar un flujo #15 que compita con los 14 existentes y termine saturando (es lo que quemó la lista: apertura 27%→8% en 4 años). El motor es **una capa de coordinación + los 3-4 flujos que faltan**, gobernada por reglas transversales. SmartBrain es el orquestador único: ya tiene los datos (Tienda Nube), ya manda (PerfitClient), y puede leer el estado de todos los touchpoints.

**Regla de oro:** cada estado del cliente tiene UN dueño. El motor solo actúa donde no hay dueño, o como capa explícitamente complementaria con exclusión.

## 2. Mapa de ciclo de vida + ownership (la vista 360)

| # | Estado del cliente | Dueño HOY | Canal | ¿Hueco? |
|---|---|---|---|---|
| 1 | Suscriptor / lead (no compró) | Perfit: 3 bienvenidas | Email | Parcial — "bienvenida 4 pasos" apagada |
| 2 | Navegó sin comprar | Perfit: remarketing visita | Email | ✅ cubierto |
| 3 | Carrito abandonado | Perfit: carrito + cupón | Email | ✅ cubierto |
| 4 | Pago pendiente / rechazado | Perfit: pago pendiente ($55M) | Email | ✅ cubierto |
| 5 | Comprador nuevo (día 0-30) | **Salto Cuántico** + cross-sell Perfit | WA + Email | ⚠️ SC en dry_run |
| 6 | Ventana de recompra (consumible ~día 25-35) | SC M5/M6 *solo si inscripto* | WA | 🔴 **HUECO** — los no-inscriptos |
| 7 | Enfriándose (En riesgo, 45-90d) | Perfit: winback 45d (1 email genérico) | Email | 🟠 **débil** — sin profundidad |
| 8 | Frío / dormido (Por Perder, 90d+) | **NADIE** | — | 🔴 **HUECO PRINCIPAL** (6.652) |
| 9 | Alto valor (Campeones/Leales/No perder) | **NADIE** (abandonados desde 2024) | — | 🔴 **HUECO** (~230, LTV alto) |
| 10 | Churned (180d+) | Nadie | — | 🟠 hueco menor |

## 3. Los flujos nuevos (solo los huecos)

### H1 · Reposición por ciclo de producto  *(estado 6)*
- **Quién:** compradores que NO están en Salto Cuántico, cuyo producto está por agotarse.
- **Inteligencia:** SmartBrain calcula la fecha de "se te acaba" por cliente, usando producto + cantidad de la orden (la Limonada en presentación X dura ~Y días). Esto Perfit no puede hacerlo — es la ventaja del motor.
- **Canal:** Email (deliberado — SC ya ocupa WhatsApp en este estado).
- **Timing:** ~día 25-30, *antes* del winback genérico de 45d.
- **Oferta:** SIN descuento — reposición natural ("tu ritual continúa"). Recompra a precio lleno = protege margen.
- **Tono KR:** continuidad del ritual / hábito, no urgencia de venta.

### H2 · Reactivación de la cola fría  *(estados 7-8) — EL HUECO GRANDE*
- **Quién:** "Por Perder" (6.652) + "En riesgo" (1.656) = ~8.300, que el winback de 45d no recuperó.
- **Canal:** Email.
- **Estructura:** secuencia de 3 toques con incentivo *escalonado* (no tirar cupón de entrada):
  1. **Toque 1 — re-enganche sin oferta:** recordá por qué empezaste (beneficio, no precio).
  2. **Toque 2 — prueba social + razón:** resultados de otras, "tu cuerpo extraña el aporte".
  3. **Toque 3 — incentivo final acotado:** recién acá un cupón con vencimiento corto.
- **Frecuencia:** 1 toque cada 4-5 días; quien compra o clickea, sale de la secuencia.
- **Cadencia de campaña:** correr sobre la cola que se va llenando cada trimestre (no blast único).

### H3 · Programa de alto valor  *(estado 9)*
- **Quién:** Campeones (18) + Leales (195) + No se pueden perder (18) = ~230.
- **Canal:** Email + WhatsApp selectivo (alto valor justifica el canal premium).
- **Oferta:** NO descuento — reconocimiento, acceso anticipado, producto de regalo (usar los rewards tier3 que ya existen en SC). Subir frecuencia y LTV, no erosionar precio.
- **Esfuerzo:** bajísimo (230 personas), margen altísimo.

### H4 · Reactivar la bienvenida de 4 pasos  *(estado 1)*
- La automation "Secuencia de bienvenida en 4 pasos" existe en Perfit pero está **apagada**. No es del motor — es un quick-win para el equipo de KR: revisarla y encenderla (o que el motor la suplante para compradores). Lo dejo señalado, no es prioridad del motor.

## 4. La capa de gobernanza (el corazón — esto hace que sea 360 y no pise)

Antes de enviar CUALQUIER mensaje, el motor pasa por estas reglas centrales:

1. **Customer State único:** SmartBrain computa por cliente su estado de lifecycle (de `tn_orders` + segmentos RFM Perfit + `salto_cuantico_enrollments`). Single source of truth, recalculado a diario.
2. **Exclusiones duras (anti-colisión):**
   - ❌ Flujo transaccional vivo (carrito / pago pendiente activo en Perfit) → no tocar, Perfit lo maneja.
   - ❌ Enrollment activo en Salto Cuántico → no tocar (SC es dueño del primer ciclo).
   - ❌ Recibió el winback 45d en los últimos N días → esperar.
   - ❌ Tiene un cupón vivo (SC coupons o campaña) → no emitir otro.
3. **Frequency cap global CROSS-CANAL:** máx. **2 contactos comerciales / cliente / semana**, contando email + WhatsApp juntos. Esto es lo que evita re-quemar la lista. Transaccionales (pago, envío) no cuentan.
4. **Prioridad de canal por estado:** primer ciclo → WhatsApp (SC). Cola fría / reposición → Email. Alto valor → Email + WA selectivo. Nunca email + WA el mismo día al mismo cliente.
5. **Cupón único / no-stacking:** un cliente jamás con 2 cupones activos. Chequeo previo obligatorio.
6. **Send window:** 08:30-20:00 ART (la misma que ya usa Salto Cuántico).
7. **Suppression list:** desuscriptos, rebotes duros, quejas → exclusión permanente (salud de lista).

## 5. Medición — probar incremental, no atribuir humo
- **Holdout del 10%** en cada flujo nuevo: grupo de control que NO recibe nada → mide el incremental REAL (no el "touched by email" que infla).
- **KPIs por flujo:** tasa de reactivación, recompra rate por segmento, días-a-recompra, revenue y margen incremental vs holdout, opt-out rate (guardrail de salud).
- **North star:** mover la recompra global de **19,8% → 23-25%** en 12 meses. Cada punto ≈ ARS 27M/año.

## 6. Arquitectura técnica (cómo se construye sin tocar nada)
- **Dónde:** módulo nuevo en SmartBrain (`packages/marketing` o `packages/retention`). No toca el módulo de Perfit automations ni Salto Cuántico.
- **Lee:** `tn_orders`/`tn_products` (ciclo de consumo), segmentos RFM de Perfit (API read-only), `salto_cuantico_enrollments`, stats de automations Perfit, cupones vivos.
- **Computa:** `customer_state` + `next_best_action` por cliente + chequeo de gobernanza.
- **Ejecuta:** vía `PerfitClient` (email a segmentos/individuos) — el canal que YA funciona. WhatsApp solo vía el dispatcher existente, respetando el protocolo de masivas.
- **NO toca:** ninguna automation de Perfit, ningún setting de Salto Cuántico, ningún broadcast. Puramente lectura + envío aditivo.
- **Tabla de gobernanza:** `retention_contact_log` (frequency cap) + `retention_exclusions` + reglas versionadas.

## 7. Roadmap por fases (riesgo creciente, nunca rompe)

| Fase | Qué | Riesgo | Por qué primero |
|---|---|---|---|
| **0** | Customer State + gobernanza en **shadow mode** (calcula, NO envía) | Cero | Valida que el motor no pisaría antes de mandar nada |
| **1** | **Cola fría** (Por Perder/En riesgo) con holdout | Mínimo | Nadie más los toca → cero colisión, máximo ROI |
| **2** | **Reposición por ciclo** (no-inscriptos SC) | Bajo | Coordinar con SC ya activo |
| **3** | **Alto valor / VIP** | Bajo | Pocos clientes, alto margen |
| **4** | **Activar Salto Cuántico** + integrarlo al frequency cap global | Medio | Requiere arreglar antes el generador que alucina skincare → [[project_kr_chatbot_kb_fix]] |

## 8. Proyección de impacto (conservadora, con MACO 70%)
- **Cola fría (H2):** 8.300 × 3% reactivación × AOV 71k = **ARS ~17,7M** revenue / ARS ~12,4M margen (primer ciclo, recurrente por trimestre).
- **Reposición (H1):** +2-3 pts de recompra sobre cohortes mensuales ≈ **ARS ~23M/año** revenue.
- **Alto valor (H3):** no cuantificado, alto margen/bajo esfuerzo.
- **Total año 1 (conservador):** ~ARS 40-55M revenue incremental ≈ ARS 28-38M margen, vs costo SB anual ~ARS 15M (USD 12k). **El motor es el "cómo se captura" del rango de recompra del resumen ejecutivo (ARS 41-82M).**

## 9. Lo que NO hace el motor (límites explícitos)
- No tira cupones por default (protege margen — incentivo solo como último toque de cola fría).
- No manda por WhatsApp en frío masivo (respeta protocolo WABA + [[feedback_wa_campaign_protocol]]).
- No toca a quien está en otro flujo (exclusiones duras).
- No reemplaza a Salto Cuántico — lo complementa y, cuando se active, lo integra al cap global.

---
Relacionado: [[resumen-ejecutivo-email-2026]], [[reference_kr_business_data]], [[project_kr_email_overhaul]], [[project_kr_chatbot_kb_fix]].
