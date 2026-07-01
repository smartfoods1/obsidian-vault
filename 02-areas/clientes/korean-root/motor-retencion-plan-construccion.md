---
date: 2026-06-08
type: plan-construccion
tags: [korean-root, retencion, smartbrain, arquitectura, motor-360]
status: plan-para-aprobación
cliente: The Korean Root
derivado_de: motor-retencion-360 + auditoría de arquitectura SmartBrain (jun 2026)
---

# Motor 360 de Retención — Lógica y Plan de Construcción

> **Plan para aprobar antes de tocar código.** Hallazgo clave: NO se construye de cero. El 70-80% de las piezas ya existen en SmartBrain, latentes. El trabajo real es **el cerebro de orquestación que las gobierna** + activar lo que ya está.

## 0. El insight que cambia el alcance
La auditoría del código reveló que casi toda la "inteligencia" ya está construida y corriendo:

| Lo que pensábamos construir | Lo que YA existe |
|---|---|
| Customer State / lifecycle | `b2c_customers` (38.379) con `rfm_segment`, `churn_probability`, `avg_days_between_orders`, **`next_expected_order`** |
| Engine de campañas de cola fría | `ecommerce/retention.py` — engine RFM multi-step (tablas `ecom_retention_campaigns`/`recipients`, vacías, listas) |
| Config de reposición por ciclo | `journey_config.py` + `product_journeys` (`duracion_dias`, `dia_oferta_recompra`, `descuento_recompra_pct`) — vacío, listo |
| Resolución de audiencia | `marketing/audience_resolver.py` |
| Medición / atribución | `cron_campaign_attribution.py` |
| Envío | `PerfitClient` (email) + dispatcher WA (`cron_unified_wa.py`) |
| Patrón de dispatcher | `cron_salto_cuantico_dispatch.py`, `cron_unified_wa.py` |

**Lo que realmente FALTA** (y es el corazón del 360): la **capa de orquestación/gobernanza** que coordina todos los touchpoints para que no se pisen ni saturen. Hoy cada sistema (Perfit automations, Salto Cuántico, retention.py, unified_campaigns) opera **aislado, sin saber de los otros**. Eso es lo que construimos.

## 1. La lógica del motor — 3 capas + 1 gate transversal

```
   ┌─────────────────────────────────────────────────┐
   │  CAPA 1 · ESTADO    (mayormente YA existe)        │
   │  Customer State = b2c_customers (RFM/churn/ciclo) │
   │  + salto_cuantico_enrollments + cupones vivos     │
   │  + contact_log (nuevo)                            │
   └──────────────────────┬──────────────────────────┘
                          ▼
   ┌─────────────────────────────────────────────────┐
   │  CAPA 2 · DECISIÓN  (nuevo, liviano)              │
   │  estado → next_best_action (qué flujo, canal)     │
   │  Reposición / Cola fría / VIP / nada              │
   └──────────────────────┬──────────────────────────┘
                          ▼
   ┌═════════════════════════════════════════════════┐
   ║  GATE · GOBERNANZA  (nuevo — EL CORAZÓN)          ║
   ║  can_contact(cliente, canal, flujo) → sí/no       ║
   ║  · frequency cap 3/sem cross-canal                ║
   ║  · exclusiones duras  · cupón único  · ventana    ║
   └══════════════════════┬══════════════════════════┘
                          ▼
   ┌─────────────────────────────────────────────────┐
   │  CAPA 3 · ENTREGA (el motor NO envía ni escribe)  │
   │  audiencias limpias + briefs → Marketing / SC     │
   │  ellos generan el contenido y ejecutan            │
   └─────────────────────────────────────────────────┘
```

> **Límite de responsabilidad (decisión Andrés, jun 8):** el motor es CEREBRO, no manos. NO genera contenido, NO define formato, NO envía. Marketing sigue creando y mandando los mails (como hoy); Salto Cuántico sigue con su journey. El motor solo aporta **estrategia + gobernanza + métricas**.

### Capa 1 — Customer State (ensamblar, casi todo existe)
Una vista por cliente que cruza:
- **De `b2c_customers` (ya computado por su cron):** `rfm_segment` (champions/loyal/regular/new/at_risk/hibernating), `churn_probability`, `avg_days_between_orders`, `next_expected_order`, `total_ordenes`, `comm_frequency`.
- **De `tn_orders`:** última compra, producto ancla, ¿evento transaccional reciente? (carrito/orden < N días → excluir).
- **De `salto_cuantico_enrollments`:** ¿inscripto activo? (excluir).
- **De cupones (SC + campañas):** ¿cupón vivo? (no emitir otro).
- **De `retention_contact_log` (NUEVO):** ¿cuántos contactos esta semana? (frequency cap).

### Capa 2 — Decision Engine (nuevo, simple)
Mapeo determinístico estado → acción:
| Estado del cliente | next_best_action |
|---|---|
| `next_expected_order` próximo + no compró + no en SC | **Reposición** (email, sin desc.) |
| `at_risk` / `hibernating` (churn alto) que el winback no recuperó | **Cola fría** (secuencia 3 toques) |
| `champions` / `loyal` | **VIP** (reconocimiento) |
| en SC / transaccional vivo / cupón activo / supprimido | **nada** (excluido) |

### GATE — Gobernanza (nuevo, el corazón)
Una sola función que **todos** los flujos del motor llaman antes de enviar:
```
can_contact(brand_id, customer_id, channel, flow) -> (allowed, reason)
```
Chequea en orden: supresión → SC enrollment activo → evento transaccional reciente → cupón vivo → **frequency cap 3/semana cross-canal** → send window. Si algo falla, no envía y registra el motivo. **Single source of governance** — nada sale sin pasar por acá.

### Capa 3 — Entrega (el motor NO ejecuta ni crea contenido)
El motor no manda ni escribe mails. En vez de enviar, **entrega** a los emisores existentes:
1. **Audiencias ya filtradas** por el gate (sin SC, sin contactados esta semana, sin cupón activo, respetando el cap) → vía `audience_resolver` que Marketing ya usa. Marketing trabaja sobre listas limpias, no necesita conocer el gate.
2. **Briefs estratégicos** por flujo (objetivo, segmento, timing, ángulo de venta) — SIN copy ni formato. Alimenta el pipeline de `proposals.py` / weekly-plan que ya existe. El equipo de Marketing escribe y manda el mail como hoy.
3. **Registro por observación:** cuando Marketing/SC ejecutan, el motor lee esos envíos (de `unified_campaigns` / Perfit / `salto_cuantico_message_queue`) y los cuenta en `retention_contact_log` para el frequency cap.
- El gate previene el pisado **en origen** (la audiencia entregada ya viene limpia), no bloqueando a Marketing → cero conflicto de control.
- **Holdout:** el motor asigna el 10% de control al construir la audiencia (lo excluye de la lista que entrega).
- **Modo DRY_RUN** (Fase 0): calcula audiencias/briefs y loguea, sin entregar nada a producción.

### Medición — incremental real
- Holdout 10% por flujo (no recibe). `cron_campaign_attribution.py` cruza `retention_sends` con `tn_orders` posteriores → conversión treatment vs holdout = **incremental verdadero**.
- North star: recompra 19,8% → 23-25% en 12 meses.

## 2. Tablas nuevas (mínimas — 3)
- `retention_contact_log` — (brand_id, customer_id, channel, flow, sent_at). El registro unificado del frequency cap. **La pieza más importante.**
- `retention_holdout` — (brand_id, customer_id, experiment, group). Asignación de control.
- `retention_suppression` — (brand_id, customer_id, reason, until). Supresión/cooldown.
- (`product_journeys`, `ecom_retention_campaigns/recipients` ya existen — solo poblar.)

## 3. El problema técnico honesto: frequency cap "cross-canal real"
El cap cuenta envíos que el motor ve. Pero **las automations de Perfit corren server-side en Perfit** — SmartBrain no se entera en vivo cuándo Perfit manda un email transaccional. Dos niveles de solución:
- **v1 (suficiente):** el motor controla el cap de SUS flujos + broadcasts (unified_campaigns) + WA. Para las automations transaccionales de Perfit usa **exclusión por evento** (SmartBrain SÍ ve la orden/carrito en `tn_orders` → si hubo evento reciente, no contacta). Las automations de Perfit además ya tienen su propio `exec_limit`.
- **v2 (cierre total):** consumir webhooks de envío de Perfit → registrar en `contact_log` → cap 100% unificado. A evaluar si Perfit los expone.

## 4. Plan de construcción por fases

| Fase | Qué se construye | Reusa | Nuevo | Riesgo |
|---|---|---|---|---|
| **0 · Cerebro + Shadow** | Customer State (vista) + GATE `can_contact` + `contact_log` + Decision Engine + `cron_retention_engine.py` en **DRY_RUN** | b2c_customers, audience_resolver | gate, contact_log, decision | **Cero (no envía)** |
| **1 · Cola fría** | Activar `retention.py` engine: secuencia 3 toques para at_risk/hibernating, holdout, email texto plano | retention.py, ecom_retention_campaigns, PerfitClient | secuencias, holdout split | Mínimo (nadie más los toca) |
| **2 · Reposición** | Poblar `product_journeys` (duración real por producto) → flujo que dispara según `next_expected_order` | journey_config, product_journeys, next_expected_order | conexión al dispatcher | Bajo (coordina con SC) |
| **3 · VIP** | Flujo champions/loyal (reconocimiento, sin descuento) | retention engine | copy/oferta VIP | Bajo |
| **4 · Integrar Salto Cuántico** | SC reporta sus envíos al `contact_log` → cap global lo incluye; activar SC | salto_cuantico | hook al contact_log | Medio (requiere arreglar generador SC antes) |

**Fase 0 es el 80% del valor arquitectónico** y no manda un solo mensaje: deja el cerebro y la gobernanza listos, y produce el reporte "a quién contactaría / excluiría y por qué" para que lo valides antes de encender nada.

## 5. Decisiones de arquitectura a tomar ANTES de codear
1. **Módulo:** crear `packages/retention/` (cerebro orquestador, reusa los engines) vs extender `ecommerce/retention.py`. → Recomiendo **módulo nuevo** (separa orquestación de ejecución; retention.py queda como un ejecutor más).
2. **Multi-tenant desde el diseño:** todas las tablas con `brand_id`, config por tenant, rollout KR primero → reusable para SF y Content Hub. → Recomiendo **sí** (costo marginal ahora, caro después).
3. **Frequency cap:** ¿v1 (exclusión por evento) o perseguir webhooks de Perfit ya? → Recomiendo **v1**, evaluar webhooks en paralelo.
4. **Formato email:** el equipo de KR reporta que **texto plano performó mejor que con imágenes**. → Arrancar los flujos del motor en **texto plano**, A/B test visual vs plano con holdout. (Revisar contra el Frente 2 del email overhaul.)
5. **Frequency cap = 3/semana** (confirmado por el equipo de KR), cross-canal.

## 6. Lo que el plan NO hace (guardrails de implementación)
- No modifica ninguna automation de Perfit, ni Salto Cuántico, ni unified_campaigns, ni sus crons.
- Fase 0 corre en DRY_RUN — cero envíos hasta tu OK explícito sobre el reporte sombra.
- No reescribe el RFM ni el churn (ya están computados; el motor los consume).
- Todo cambio en `/tmp` + backups + un tenant a la vez (KR), verificación antes de cada fase.

---
Relacionado: [[motor-retencion-360]], [[reference_kr_business_data]], [[project_smartbrain_module_loader]], [[project_kr_email_overhaul]].
