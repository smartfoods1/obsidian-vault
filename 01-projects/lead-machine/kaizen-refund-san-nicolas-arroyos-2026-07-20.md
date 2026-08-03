---
date: 2026-07-20
type: ops-log
tags: [gondola, lead-machine, kaizen, refund, soporte]
status: done
derivado_de: kaizen-cruce-clientes-refund-2026-07-18
---

# Kaizen — refund por leads de San Nicolás de los Arroyos (zona equivocada)

## Contexto
Kaizen (brand 152) rehízo la búsqueda seleccionando la localidad **San Nicolás** (barrio del
centro de CABA). La app le incluyó negocios de **San Nicolás de los Arroyos** (PBA, ~220 km,
cerca de Rosario). Pidió por WhatsApp eliminarlos y que le devolvieran los créditos. Se están
concentrando en CABA.

## Causa raíz (producto)
La búsqueda geográfica (`region='San Nicolás, Ciudad Autónoma de Buenos Aires'`) fue a Google
Places y éste devolvió comercios homónimos fuera del área: la ciudad **San Nicolás de los
Arroyos** matchea el texto "San Nicolás" y Places no acotó al radio de CABA. Mismo patrón de
ruido geográfico que ya se vio en otras zonas (homónimos lejanos). **El buscador no filtra por
distancia al centroide de la zona pedida.** → chip de mejora abierto.

## Diagnóstico (read-only)
- Total leads guardados Kaizen: **173**.
- Clasificación por distancia a CABA + localidad + CP:
  - Barrio **San Nicolás (CABA)**: 5 leads a 0–1 km del Obelisco → **correctos, NO se tocan**.
  - **San Nicolás de los Arroyos** (localidad literal, CP B2900, 214–221 km): **7 leads**, todos
    con WhatsApp (cobrados).

## Acción ejecutada (2026-07-20 ~11:47 ART)
Backup previo consistente: `/opt/lead-machine/backups/pre_snarroyos_refund_20260720_114721.db`.

Borrados los 7 `saved_leads` de San Nicolás de los Arroyos + refund idempotente (patrón
`lead_refunds` UNIQUE brand+global_place_id, igual que `refund_reconcile`):

| saved_id | gid | comercio | CP |
|---|---|---|---|
| 10305 | 2414 | Apidelta S.R.L. - Casa Central | B2900 |
| 10307 | 2416 | Dietetica 100 % Natural | B2900 |
| 10308 | 2417 | Oasis Almacen Natural | B2900 |
| 10309 | 2418 | La Comarca Almacén Saludable | B2900 |
| 10310 | 2419 | Tilo Tienda Natural Dietetica | B2900 |
| 10311 | 2420 | Pachamama natural market | B2900 |
| 10317 | 2426 | AL GRANO Almacen | B2900 |

**Resultado:**
- Leads borrados: **7**
- Créditos devueltos: **7** → `paid_credits` **48 → 55**
- saved_leads Kaizen: 173 → **166**
- Control post: barrio San Nicolás CABA = 5 (intactos), San Nicolás de los Arroyos = 0, refunds
  registrados = 7.

Nota: solo se borró de `saved_leads` (capa privada de la marca). NO se tocó `global_places`
(pool de red compartido) ni `cost_ledger` (el costo real ocurrió; el refund es de créditos al
cliente, no del gasto).

## Hallazgo lateral — leads-basura de OTRAS búsquedas (BORRADOS 2026-07-20 ~11:54)
El filtro por distancia destapó 3 leads lejanos que NO eran parte de la queja de Kaizen. Andrés
dio OK ("borralos también"). Backup: `pre_farleads_refund_20260720_115423.db`.
- **id 10313** "Olivares San Nicolás – Productos Or…" → **Cruz del Eje, Córdoba** (752 km),
  misma búsqueda "San Nicolás" (homónimo). Cobrado → +1 crédito.
- **id 2704** "Dietetica Belgrano" → **Rafaela, Santa Fe** (472 km), búsqueda "Belgrano".
  Cobrado → +1 crédito.
- **id 2710** "Almacén Orgánico Natural" → **General Pico, La Pampa** (502 km), búsqueda
  "Belgrano". NO cobrado (sin WhatsApp) → borrado sin refund.

Resultado 2ª pasada: 3 borrados, 2 créditos devueltos.

## TOTAL operación 2026-07-20
- **10 leads borrados** (7 San Nicolás de los Arroyos + 3 lejanos).
- **9 créditos devueltos** (`lead_refunds`: 9 filas), todos los cobrados.
- **Kaizen usó la app EN VIVO durante la operación**: entre las dos pasadas (11:47→11:54) hizo
  búsquedas nuevas en CABA (+5 leads correctos, −5 créditos gastados), por eso el saldo se mueve.
  El refund es incremento relativo (`paid_credits = paid_credits + 1`), no pisa el saldo → seguro
  ante concurrencia. **No clavar un número de saldo fijo en el mensaje a Kaizen** (que lo vea en la app).
  Script 2ª pasada: `/tmp/exec_refund2.py` (VPS).

## Gerli (zona sur) — borrado 2026-07-20 ~12:42
Barrido completo de la cuenta (`/tmp/sweep_offzone.py`) encontró 6 leads de provincia guardados
en búsquedas de CABA. Decisión de Andrés: **borrar solo Gerli** (id 10128, zona SUR, fuera de
"Capital + Zona Norte" de Kaizen); **mantener** Martínez, Villa Adelina, Tigre, Ing. Maschwitz y
La Lonja/Pilar (Zona Norte = zona de operación de Kaizen). Backup `pre_gerli_20260720_124222.db`.
1 borrado, 1 crédito devuelto.

Caso **Claypole**: NO se cobró ni guardó (el comercio no tiene WhatsApp → Garantía Nivel 1). Solo
aparecía en la grilla de resultados en pantalla (`brands.last_results`), no en "Mis leads". Nada
que borrar ni devolver.

## FIX DE RAÍZ desplegado + ACTIVO en prod (2026-07-20 ~12:51)
Restricción geográfica por **viewport real de la zona** (autocomplete → placeId → Place
Details.viewport → `locationRestriction.rectangle` en el Places Text Search). Detrás de flag
`LM_ZONE_RESTRICT` (default 0 en código; **=1 en `/opt/lead-machine/.env`**, activo).
- Backend-only (no toca el frontend). Funciones nuevas en `app.py`: `_places_search_body` (pura),
  `_resolve_zone_viewport` (cacheada 24h por region), `_viewport_from_details`. Aplicado en los 2
  call-sites de `places_search_async` (`/api/leads` y `/api/leads/preview`).
- Fallback robusto: si el viewport no resuelve → búsqueda sin restricción (comportamiento previo).
- 6 tests nuevos (Z-1..Z-3c) verdes. Deploy vía `./deploy.sh` (smoke OK, flag OFF en el deploy →
  no-op; activado después con .env + restart). Canary Retiro: SIN restricción 20 leads dispersos
  por CABA → CON restricción 7 leads solo Retiro/Recoleta. Claypole (lat −34.80) y S.N. de los
  Arroyos (lat −33.33) quedan fuera del rectángulo de Retiro por construcción.
- **Off-switch instantáneo**: `LM_ZONE_RESTRICT=0` en `.env` + `systemctl restart lead-machine`
  (backups `.env.bak.zonerestrict.*`).
- **Tradeoff conocido** (aceptado por Andrés): buscar un barrio chico ahora trae solo de ese
  barrio (menos leads por búsqueda, pero sin ruido). Vigilar que no queden búsquedas "cortas".
- **Deuda**: los cambios están en prod (rsync) pero **sin commitear en git** (working tree). El
  próximo deploy los sube; conviene commitear en `main` para versionar.

## Scripts
- Diagnóstico read-only: `/tmp/diag_kaizen.py` · barrido off-zone `/tmp/sweep_offzone.py` (VPS)
- Ejecución (valida geografía por lead antes de borrar, aborta si no cuadra): `/tmp/exec_refund.py`,
  `/tmp/exec_refund2.py`, `/tmp/exec_gerli.py` (VPS)
- Canary del fix: `/tmp/canary_viewport.py` (VPS)

Ver [[kaizen-cruce-clientes-refund-2026-07-18]] · [[kaizen-primer-cliente-2026-07-16]]
