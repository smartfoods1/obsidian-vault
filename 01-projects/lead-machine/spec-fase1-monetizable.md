---
date: 2026-06-22
type: spec
tags: [lead-machine, gondola, monetizacion, fase1, pricing]
status: in-progress
derivado_de: "[[handoff-fase1]]"
---

# Gondola — Spec Fase 1 monetizable

> Contexto: ver [[handoff-fase1]] y [[v2-vision-arquitectura]]. App **viva y cobrando** — todo cambio pasa por `./run-tests.sh` → `./deploy.sh` (rollback automático). Nunca a mano.

## Objetivo

Subir el ARPU y la defensibilidad de Gondola **sin construir billing recurrente ni el riel de transacción** (eso es Fase 2). Tres frentes, todos cobrables/visibles esta semana:

1. **Pricing nuevo** (UI + links de pago) — re-precificar la escalera self-serve y el tier gestionado.
2. **Benchmarks de canal visibles** — exponer `segment_stats` (ya se computa, hoy oculto). Es el moat.
3. **Recordatorios de recompra** — la guita B2B está en el 2º/3er pedido; hoy no se trabaja.

El **success fee (% de GMV / fee por deal)** NO entra en Fase 1: requiere que la transacción pase por Gondola (Fase 2). Cobrarlo antes es a confianza y se filtra.

---

## Frente 1 — Pricing nuevo  *(implementar primero)*

### Decisión de modelo
Lo único cobrable hoy sin construir billing recurrente son los **packs de crédito one-shot** (checkout MercadoPago ya funciona) + el tier **gestionado (DFY)** que se cierra a mano. Por eso:

- Los **packs** son la compra self-serve (los "links de pago"). Se re-precifican.
- El **DFY** queda como tier high-touch (CTA a contacto, sin checkout self-serve), repreciado a $350k.
- Se **elimina el badge "mensual"** de la UI: implica débito recurrente que todavía no existe. El mecanismo de `plan='mensual'` (report_access) sigue intacto para cuentas otorgadas a mano por admin — solo se deja de publicitar un precio mensual.

### Tabla nueva (ARS)

| Pack (key interna) | Nombre visible | Leads | Precio | $/lead | Pitch |
|---|---|---|---|---|---|
| `probar` | **Buscador** | 60 | $49.000 | $817 | Validá el canal en tu zona. Una cuenta nueva ya paga el pack. |
| `vender` | **Pro** ⭐ | 200 | $119.000 | $595 | El más elegido: un mes de prospección activa con mensaje y seguimiento. |
| `expansion` | **Expansión** | 600 | $290.000 | $483 | Varias zonas, pipeline lleno, el mejor precio por lead. |

Gestionado: **`done_for_you` — "Gestionado (DFY)" — desde $350.000** (leads + un SDR que hace intro y seguimiento). Sin self-serve checkout.

> **Las keys internas NO cambian** (`probar/vender/expansion`). Solo cambian `nombre/leads/precio/pitch`. Razón: el `external_reference` de MercadoPago es `brand_id:pack_id` — cambiar la key rompería la acreditación de cualquier pago en vuelo.

### Riesgo crítico: pagos en vuelo durante el cambio de tarifa
El webhook valida `monto_pagado + 1 >= pack["precio"]` y acredita `pack["leads"]` (ambos **vigentes**). Si **subo** el precio, un `init_point` creado con la tarifa vieja y pagado **después** del deploy:
`monto_viejo ($25k) < precio_nuevo ($49k)` → `paid_ok=False` → **el cliente paga y no recibe leads.** Incidente real.

**Mitigación (incluida en este frente):** el webhook acredita según el **monto realmente pagado**, resuelto contra una escalera de tarifas (vigente + histórica) por pack:

```python
PACK_LEGACY_PRICES = {            # quitar tras ~7 días sin init_points viejos
    "probar":    [(25000, 30)],
    "vender":    [(70000, 100)],
    "expansion": [(150000, 250)],
}
def _grant_for_payment(pack_id, amount) -> int | None:
    pack = PACKS.get(pack_id)
    if not pack: return None
    ladder = [(pack["precio"], pack["leads"])] + PACK_LEGACY_PRICES.get(pack_id, [])
    for precio, leads in sorted(ladder, key=lambda x: -x[0]):  # tarifa más alta cubierta
        if float(amount) + 1 >= float(precio):
            return leads
    return None
```
El webhook usa `grant = _grant_for_payment(pack_id, amount)`; rechaza si `grant is None` o moneda ≠ ARS. Pago vigente → leads nuevos; pago viejo en vuelo → leads viejos; overpay → pack vigente. Idempotencia por `pay_id` intacta.

### Cambios de archivos
- `app.py`: `PACKS` + `PRICING` (sacar `mensual`, DFY→350k) + `PACK_LEGACY_PRICES` + `_grant_for_payment` + webhook (`pack["leads"]` → `grant`).
- `webapp/src/components/Paywall.tsx` *(polish, requiere rebuild)*: resaltar el pack `destacado` ("más elegido"); reemplazar la fila de badges mensual/DFY por una línea-CTA "¿Volumen o gestionado? Escribinos" → DFY. **Los precios/planes ya se actualizan solos vía `/api/pricing` sin rebuild**; el rebuild es solo cosmético.

### Criterios de aceptación
- `/api/pricing` devuelve los 3 packs nuevos + DFY 350k, sin `mensual`.
- Checkout de cada pack genera preferencia MP con el precio nuevo.
- Webhook: pago a precio nuevo acredita leads nuevos; pago a precio viejo (simulado) acredita leads viejos; subpago < toda tarifa → rechazado.
- `./run-tests.sh` en verde (45 checks).

---

## Frente 2 — Benchmarks de canal visibles  *(spec, no se implementa aún)*

`segment_stats` (rubro×zona: marcas, leads, positive, won, lost, conv_rate) ya se computa y se usa interno. Exponerlo:

- **Ficha del lead:** badge "comercios como este convierten al X% para marcas como la tuya" (solo si `n_marcas ≥ 5` — k-anonimato; respetar la pared global/privado que ya existe en el código).
- **Buscador:** rankear zonas/rubros por conversión histórica → "no quemes créditos en Palermo (12%), andá a Caballito (27%)". Convierte la herramienta de *lista* en *estrategia de canal*.
- **Dashboard "Inteligencia de canal"** (v2): dónde entran las marcas como vos, ticket promedio, ciclo.

Caveats: mostrar siempre el `n`; gate `n_marcas ≥ 5`; el `conv_rate` vale lo que valga la disciplina de marcar `ganado/perdido` (mejora con el riel de Fase 2).

Endpoint nuevo: `GET /api/segments?rubro=&zona=` → `{conv_rate, n, brands, ticket_prom}` con gate de anonimato. Es lo que defiende el precio ("no es una lista, es inteligencia de canal").

---

## Frente 3 — Recordatorios de recompra  *(spec, no se implementa aún)*

La recurrencia B2B es el 2º/3er pedido. Hoy la ficha tiene `last_contacted_at`, `outcome=ganado`, `deal_value` — falta cerrar el loop.

- Campo/derivado: para leads `ganado`, calcular "próxima recompra sugerida" (default editable, ej. +30 días del último pedido).
- En `/leads`: filtro/pill "A recomprar" (como "Vencidos" hoy) y KPI.
- Notificación al dueño de marca (WA template APPROVED) "estas 3 cuentas tocan reposición esta semana".
- Semilla del riel de Fase 2: cuando exista el pedido-en-Gondola, este recordatorio dispara un re-pedido en 1 tap (ahí nace el success fee honesto).

---

## Fuera de alcance (→ Fase 2)
- Billing recurrente real (MP suscripciones) para MRR con débito automático.
- Riel de pedido/recompra dentro de Gondola (sistema de registro de la relación B2B).
- **Success fee / % de GMV facilitado** — depende del riel.
- Lado del comercio (cuenta, badge de comprador verificado) = el "validador de confianza" real.

## Métrica que decide
Conversión **free→pago** (hoy 5 leads gratis). Target 8–15% con el onboarding arreglado (cold-start de los puntos 2/3 del feedback). Vale más que cualquier ajuste de precio.

## Plan de deploy
`./run-tests.sh` → revisar diff → `./deploy.sh` (tests→backup→snapshot→rsync DB-excluida→smoke→rollback auto). Idealmente en ventana de bajo tráfico. Tras ~7 días sin pagos viejos, quitar `PACK_LEGACY_PRICES`.
