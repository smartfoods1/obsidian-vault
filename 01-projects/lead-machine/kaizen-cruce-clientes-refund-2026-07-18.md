---
date: 2026-07-18
type: ops-log
tags: [gondola, kaizen, billing, refund, producto]
status: pendiente-decision
---

# Kaizen — Cruce lista de clientes vs leads servidos + devolución de créditos

## Contexto

Kaizen (brand 152, primer cliente pago, Pro 200) subió su lista de clientes el 18/7 20:37 UTC —
**después** de servidos sus 195 leads (último 17:21). La exclusión de "Cargar clientes" solo corre
en búsquedas futuras, así que hubo que cruzar retroactivamente el Excel (110 filas, 97 únicos,
carga completa en `brand_clients`) contra `saved_leads`.

## Hallazgo clave de producto

El matching del backend (`_is_own_client`: nombre igual/prefijo + zona) atrapó **0 de 7** casos
reales. Los 7 se encontraron por teléfono normalizado y dirección exacta (calle+número):
Google invierte el orden de las palabras del nombre y hay listings duplicados.
→ Task pendiente: agregar teléfono + dirección al matching (chip spawneado).

## Leads confirmados como clientes propios (7)

| Lead | Comercio | Cliente Kaizen | Señal | Cobrado |
|---|---|---|---|---|
| 2436 | Mercado Natural Lafinur (Palermo) | Mercado Natural Lafinur | dirección | sí |
| 2444 | Dietetica Natur Life (Palermo) | Natur Life Dietética | teléfono+dir | sí |
| 2691 | Plutarco Almacén (Coghlan) | Dietética Plutarco | dirección | no (sin WA) |
| 2707 | Almacén All Natural (Belgrano) | ALL Natural | dirección | sí |
| 2727 | "PRODUCTOS DIETETICOS Y NATURALES" | ALL Natural (listing duplicado, mismo WA que 2707) | dirección+tel | sí |
| 3029 | La Choza Caballito | Tienda La Choza Caballito | dirección | no (sin WA) |
| 3255 | Puna Dietetica (V. Urquiza) | Puna Almacén | teléfono+dir | sí |

Falsos positivos revisados y descartados: AlmaZen Palermo (cliente es el de Zabala 1693),
Coquito's Núñez y V. Crespo (cliente es la sucursal de Suipacha 635), Dietética All Natural
Caballito, Dietética Bellgrano Monserrat, Dietetica Belgrano de Rafaela.

## Acciones aplicadas (18/7, backup previo `leadmachine-2026-07-18_1910.db.gz`)

- Lead 2727 (único aún `nuevo`) → `descartado`. Los otros 6 ya los había descartado Kaizen a mano.
- Nota de traza en los 5 leads devueltos.
- **Devolución: +5 `paid_credits`** (los 5 cobrados con WhatsApp; los 2 sin WA nunca se cobraron
  por la garantía). Créditos Kaizen: 49 → **54**.

## Actualización 18/7 noche — matching v2 deployado + borrado definitivo (pedido de Andrés)

Backup previo: `leadmachine-2026-07-18_2120.db.gz`.

- **Matching v2 en prod**: `_is_own_client` ahora matchea por teléfono normalizado (columna nueva
  `brand_clients.telefono_norm` + backfill) y calle+altura, además del nombre+zona. Verificado
  contra los datos reales: 7/7 atrapados, 0 falsos positivos sobre los 195 servidos. Commit
  `7c6b03b` (checkpoint), tests de regresión con los 7 casos reales en la suite.
  → El cruce retroactivo a mano ya NO hace falta para clientes que suben la lista después de buscar.
- **Borrados los 7 leads clientes-propios** de `saved_leads` (brand 152) y del espejo (brand 7).
- **Borrados los 23 descartados sin información de contacto** (sin WhatsApp/tel/email/IG; nunca
  consumieron crédito por la garantía "sin WhatsApp no se cobra", vigente desde el 4/7) — también
  del espejo. Quedan 28 descartados legítimos (con contacto).
- **Acreditación +2** → los 7 leads propios quedan devueltos completos (5 el 18/7 tarde + 2 ahora).
  Créditos Kaizen: 54 → **56**. Estado final: 165 leads en cuenta, espejo consistente.

## Ronda 2 (18/7 noche) — descartados con WhatsApp validado MUERTO

Andrés vio en el espejo descartados "sin info de contacto" que la ronda 1 no tocó: no era data
vacía sino **WhatsApp validado como inexistente** (CheckNumber corrió hoy → `wa_registered=0`;
la grilla apaga el ícono). Esos leads SÍ se cobraron (tenían número al servirse).

- Borrados **15 por cuenta** (Kaizen + espejo, match 1:1): WA muerto y ningún otro canal
  (sin email/IG/web) — Matias, Tu Vida Sana, La Casita, La Buena Semilla, Buena Vida x2, etc.
- **Acreditación +15** (cobrados, sin devolución previa). Créditos Kaizen: 56 → **71**.
- Backup previo: `leadmachine-2026-07-18_2129.db.gz`.
- Quedan 13 descartados por cuenta, todos con algún canal real: 9 con WA muerto pero web/email
  activos y 4 con WA válido.

## Ronda 3 (18/7 noche) — criterio definitivo de Andrés: la web sola NO es contacto

Andrés vio los web-only en el espejo y fijó el criterio: **sin contacto accionable = WA inválido
y sin email y sin Instagram** (una página web sola no cuenta; operación WhatsApp-first). Además:
"ni siquiera deberían aparecer en descartados si no se pueden enriquecer" → task chip actualizado
(filtrar en pool-serve + vista/export + auto-refund al validar muerto un número cobrado).

- Borrados **7 por cuenta** (Kaizen + espejo, match 1:1): Vida Country, El Lunes Empiezo, Li-Món,
  La Moderna de Núñez, Casa Polti, El Banquito, Vitalcer corrientes — WA muerto, solo web.
- **Acreditación +7** (cobrados, sin devolución previa). Créditos Kaizen: 71 → **78**.
- Backup previo: `leadmachine-2026-07-18_2137.db.gz` (tercero del día).
- Estado final ambas cuentas: **143 leads, 6 descartados** — Tienda Nova x3 y ENELDO con WA
  validado OK, Tienda Nova Núñez/Urquiza con WA muerto pero email (+IG Núñez).

## Total devuelto a Kaizen hoy: 49 + 5 + 2 + 15 + 7 = 78 créditos (sobre 200 pagados)

## Fix sistémico (19/7) — deployado, con el auto-refund APAGADO

Las 3 rondas anteriores fueron a mano. El 19/7 se deployó el fix de producto para que no vuelva a
pasar. Commit `99bb98a` en la rama `claude/dazzling-varahamihira-aac798`, deploy con `./deploy.sh`
(smoke OK). El criterio de Andrés quedó en una sola función, `_sin_contacto_accionable()`:
**WhatsApp inválido (`wa_registered=0`, reportado muerto, o sin número) Y sin email Y sin Instagram**;
la web sola no cuenta.

**1. Serve-time** — `_pool_serve()` ahora lee `wa_registered` (está en la misma tabla que ya
consultaba) y no sirve esos comercios del pool cacheado. No se ofrecen y no se cobran. El camino de
Places (leads frescos) no tiene señal previa, así que no aplica.

**2. Vista y export** — `/api/my-leads` y `/api/export` los ocultan, pero **solo si el crédito ya se
devolvió** (hay fila en `lead_refunds`) o la marca es `unlimited` (no consume créditos). Ocultar un
lead cobrado sin devolver la plata sería cobrar por nada en silencio, así que la parte 2 depende de
la 3. Un lead cobrado y sin refund sigue visible.

**3. Auto-refund — NACE APAGADO (`LM_AUTO_REFUND=0`), falta tu OK**
- `refund_reconcile()` en `app.py` + endpoint admin `POST /api/admin/refunds/reconcile`
  (dry-run por default; `?apply=true` no hace nada mientras el flag esté en 0).
- Devuelve **+1 `paid_credits`** por lead cobrado después del 4/7 (`LM_REFUND_MIN_CREATED`, muerte
  del chip Baileys) que quedó `wa_registered=0` sin email ni IG. Marcas `unlimited` quedan fuera.
- Idempotencia real: tabla `lead_refunds` con `UNIQUE(brand_id, global_place_id)`. Un número puede
  re-chequearse y volver a dar 0 — el crédito se devuelve una sola vez. Cada refund deja traza.
- `ops/checknumber_verify.py` lo dispara al final de cada corrida, pero solo si el flag está en 1.
- Detalle a tener en cuenta: siempre acredita `paid_credits`, incluso si el lead se había consumido
  del cupo gratis. Es una devolución levemente a favor del cliente; se eligió eso antes que la
  contabilidad exacta.

**Dry-run contra prod (19/7): 2 candidatos, ambos de Kaizen** — BIOPEÑA (`+5491148062765`, lead 2968)
y Tienda Saludable (`+5491145454776`, lead 3045), los dos servidos el 18/7 a la tarde. Son nuevos: no
estaban en las 3 rondas manuales. Hoy Kaizen los sigue viendo y ya se los cobramos.

**Decisión pendiente**: prender `LM_AUTO_REFUND=1` en el `.env` del VPS y reiniciar el service. Son
2 créditos ahora y después queda automático.

Foto del pool en prod al 19/7: 1615 números validados OK, 383 sin chequear, 322 con WA muerto pero
con email o IG (se siguen sirviendo, son contactables) y **79 sin ningún canal** — esos 79 son los
que el filtro nuevo saca de circulación.

### El fix se perdió una vez y se recuperó (mismo día)

Pasó exactamente lo que se había advertido. Entre el primer deploy y el segundo, la rama del CRM se
mergeó a `main` y se deployó desde ahí: como `main` no tenía este commit, el rsync **borró el fix de
prod**. Durante esa ventana Góndola volvió a servir y cobrar leads sin canal accionable.

Recuperado con un merge de `main` (CRM hasta `e4e623b`) dentro de la rama del fix → commit `47501f3`,
suite completa en verde (26 checks Kaizen + los del CRM, 0 fallos) y redeploy. Verificado en prod: las
tres piezas del fix y el CRM conviviendo, y `main == worktree == prod` en `47501f3`. El `app.py`
mergeó solo; el único conflicto fue el bloque final de `tests/test_app.py`, donde las dos ramas
habían agregado checks antes del print — se quedaron los dos.

**Lección**: prod es un rsync del working dir, así que cualquier rama que se deploye sin tener el
commit de la otra la revierte en silencio. Antes de `./deploy.sh` desde cualquier rama, verificar que
tenga mergeado lo que ya está vivo en prod. El smoke no lo detecta: un revert deploya perfecto.
