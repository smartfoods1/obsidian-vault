---
date: 2026-07-04
type: backlog
tags: [lead-machine, gondola, enrichment, detective, import, b2b]
status: activo
derivado_de: "[[handoff-v2-completo]]"
---

# Góndola — Backlog: Detective de contacto + Import/Export

Backlog accionable para arrancar YA. Nace de dos pedidos del CEO (04-jul-2026):
1. Un "detective" que corra en el VPS con la key de Gemini y siga enriqueciendo leads (caso testigo: *Bio Solo Orgánico* — el WhatsApp está en su IG/Linktree pero la app no lo muestra).
2. Import + Export de cartera.

> **Hallazgo que da vuelta el diagnóstico:** el detective **ya existe y ya corre**. No hay que programarlo de cero — hay que **destaparlo** (está medio ciego por un problema de créditos) y **extenderlo** (no sigue la cadena social IG→Linktree→WhatsApp). Detalle abajo.

Código real en prod: `/opt/lead-machine/app.py` (VPS `root@76.13.228.77`). Local de dev: `~/lead-machine`. Deploy SOLO con `./deploy.sh`.

---

## Diagnóstico verificado (04-jul, contra prod)

| Componente | Estado real | Evidencia |
|---|---|---|
| Worker de enriquecimiento | **VIVO, 4 días up** | `lead-machine-worker.service` active; `LM_WORKER_BUDGET` seteado; 4.062 jobs `done`, 3.947 `failed`, 1.260 `queued`; 16.202 `lead_facts` |
| Búsqueda web (Serper) | **ROTA — sin créditos** | Test directo: `{"message":"Not enough credits","statusCode":400}`. El 100% de las búsquedas web fallan → el detective queda solo con el scrape del sitio |
| Validación WhatsApp (Baileys) | Chip vivo pero intermitente | `/status` = 200, pero `/validate` devolvió 503 en el log. `wa_registered` sigue NULL en la base |
| Cadena social IG→Linktree→WhatsApp | **No existe** | `_gather_enrich_signals` scrapea sitio + 3 Serper, pero no entra al perfil IG ni sigue el link-in-bio; `whatsapp` ni siquiera es un `_ENRICH_TARGET_FIELD` |
| Import de cartera | **No existe** | Cero endpoints de upload; FastAPI no importa `UploadFile` |
| Export | **Existe** | `GET /api/export` (csv/xlsx/json/pdf), `app.py:3250` |

**Traducción:** la tasa de `failed` (~49%) y el caso "Bio Solo Orgánico" tienen la misma causa raíz #1 — **Serper sin créditos**. El detective está pedaleando en el aire para todo comercio que no tenga sitio web propio (la mayoría del canal).

---

## P0 — Destapar lo que ya está construido (hoy, minutos)

### P0.1 — Recargar créditos de Serper ⚡ (el fix de mayor ROI de todo el backlog)
- **Qué:** la cuenta de serper.dev se quedó sin créditos → cada enrich pierde sus 3 búsquedas web. Recargar (o rotar a una key nueva) revive la mitad del pipeline sin tocar una línea de código.
- **Acción:** entrar a serper.dev, ver plan/créditos, recargar. Reemplazar `SERPER_API_KEY` en `/opt/lead-machine/.env` si se rota. `systemctl restart lead-machine-worker`.
- **Verificar:** `curl -s -X POST https://google.serper.dev/search -H "X-API-KEY: $K" -H "Content-Type: application/json" -d '{"q":"test","gl":"ar"}' -w "\n%{http_code}"` → debe dar 200.
- **Esfuerzo:** 10 min. **Impacto:** altísimo.

### P0.2 — Re-encolar los jobs que fallaron por Serper
- **Qué:** los 3.947 `failed` y buena parte de los `done` sin hallazgo se procesaron ciegos. Una vez con Serper vivo, re-encolarlos.
- **Acción:** `UPDATE enrich_jobs SET status='queued', attempts=0, next_attempt_at='', last_error='' WHERE status='failed';` (vía `sqlite3` con la app corriendo — es WAL, seguro). El worker los drena solo respetando `LM_WORKER_BUDGET`/día.
- **Ojo:** subir `LM_WORKER_BUDGET` unos días para drenar el backlog más rápido, después bajarlo.
- **Esfuerzo:** 5 min.

### P0.3 — Salud del chip Baileys (/validate) — ROBUSTEZ HECHA 04-jul, falta re-vincular
- **Diagnóstico:** el chip (`wa-baileys.service`, :8787) estaba **loggedOut (code 401)** — la sesión murió, no un 503 transitorio. Por eso `/validate` daba error y `wa_registered` sigue NULL. Un restart NO recupera un loggedOut: hay que limpiar `auth_info` + re-pairing con el teléfono físico (línea 5491165857832).
- **Hecho (04-jul):**
  1. **Health-check + auto-recover + alerta** (`wa_healthcheck.py` + `wa-healthcheck.timer`, cada 2 min). Vigila `/status`; si el chip cae, intenta `systemctl restart wa-baileys` (recupera caídas transitorias); si la sesión murió de verdad, **alerta a Andrés por Telegram** (canal robusto: entrega siempre, no depende del chip ni de ventanas de Meta) con los pasos de re-vinculación. Avisa también cuando se re-vincula.
  2. **Reconnect endurecido en `server.js`**: backoff exponencial (2s→cap 60s) en vez de retry fijo a 2s → sin loop rápido cuando WA rechaza seguido. Deploy con `node --check` + backup + restart verificado.
- **Falta (acción de Andrés, necesita el teléfono):** re-vincular ahora. `systemctl stop wa-baileys && mv auth_info auth_info.dead-$(date +%s) && systemctl start wa-baileys && curl -s -X POST http://127.0.0.1:8787/pair` → código de 8 díg → WhatsApp del chip > Dispositivos vinculados > Vincular con número.
- **Nota:** de acá en más el chip se auto-recupera de caídas transitorias y Andrés recibe alerta por Telegram si necesita intervenir. El "que nunca falle" está cubierto por detección+alerta, no por magia.

---

## P1 — Detective social: IG → Linktree → WhatsApp ✅ DEPLOYADO 04-jul

> **ACTUALIZACIÓN 04-jul (noche) — migrado a Gemini grounding (commit 9fe454e):** el detective ya NO usa Serper. `_gather_enrich_signals` hace **1 llamada a `gemini-2.5-flash` con tool `google_search`** (busca la web y extrae contacto en una pasada). Adiós dependencia de Serper y sus recargas. ~$0.002/lead (medir vs free tier de grounding de Google, ~1500/día gratis; ajustar `LM_COST_GEMINI_GROUNDED`). Calidad validada = comparable a Serper (Bio Solo Orgánico → mismo WhatsApp real). Las funciones Serper quedan solo para el ICP. El worker drena con el nuevo motor.

**Estado:** implementado y en prod (`./deploy.sh` OK, 45 tests + smoke). Validado contra datos reales antes de deployar: sobre leads con IG, cazó WhatsApps que el fijo no mostraba — ej. **SUPERSALUDABLE**: fijo derivado `+5491154110064` vs **celular de ventas real `+5491139235341`**; **Almacén Natural del Mercado**: WhatsApp `341` (Santa Fe) que el fijo porteño ocultaba. El worker drena ~600 leads/día con las 2.500 queries gratis (después, pack Starter $50).

**Qué se implementó (en `app.py`, sección enrich):**
- 4ta búsqueda Serper dirigida a `whatsapp OR wa.me OR linktr.ee`; se sigue el **link-in-bio** (Linktree/Beacons/… en `LINKTREE_HOSTS`) y se scrapea su HTML.
- Extracción DURA por regex de números detrás de `wa.me/` y `api.whatsapp.com` (`_extract_wa_numbers`), que se pasan como candidatos fuertes a Gemini.
- Nuevo `source='social'` (confianza 0.85 en `_FACT_CONFIDENCE`, arriba de `websearch`/`derived`) → el WhatsApp real **pisa** el fijo derivado, marca `wa_verificado`, y se propaga al snapshot privado.
- **Fix del gasto fantasma:** `_serper_call` devuelve `credited` y solo se cobra al presupuesto la búsqueda que dio HTTP 200 (antes se cobraba aunque el 400 "Not enough credits" no consumiera crédito → agotaba el budget diario sin trabajo).

**Pendiente de robustez (P2):** el worker debería **auto-pausar** (tocar el killfile + alertar) cuando Serper devuelva "not enough credits" repetido — hoy, sin créditos, sigue corriendo y marca leads como `no_source`. Mientras tanto: apagar el worker (`LM_WORKER_BUDGET=0`) cuando se agoten las gratis, hasta cargar el pack.

**Caso testigo original:** *Bio Solo Orgánico* — el WhatsApp/celular vive en su IG/Linktree; el detective social ahora lo sigue.

### Diseño (extender `_gather_enrich_signals`, `app.py:1458`)
Agregar un **paso de cadena social** cuando el enrich detecta (o ya tiene) un Instagram, o cuando el comercio no tiene sitio:

1. **Resolver el link-in-bio.** IG bloquea el scraping directo del perfil (login wall) — no pelear contra eso. En cambio:
   - Búsqueda dirigida Serper: `"{nombre} {localidad} linktree OR linktr.ee OR beacons OR wa.me"` + `"{nombre} instagram"`.
   - Seguir el primer link a un agregador **scrapeable en HTML plano**: `linktr.ee/*`, `beacons.ai/*`, `mtr.bio/*`, `koji`, `stan.store`, o el propio sitio.
   - Reusar `fetch_site_text_async` para bajar el HTML del agregador.
2. **Extraer contacto con regex sobre el HTML** (antes de Gemini, barato y preciso):
   - `wa\.me/(\d{10,15})`
   - `api\.whatsapp\.com/send\?phone=(\d{10,15})`
   - `href="tel:([^"]+)"`, `mailto:`
   - handle IG, links a menú/catálogo
3. **Gemini razona** cuál número es el **WhatsApp de ventas/dueño** vs genérico, y extrae `nombre_contacto` si aparece ("escribile a Marce", "consultas con...").
4. **Escribir el fact** con nuevo `source='social'` (confidence alta, arriba de `websearch`). Agregar `whatsapp` y `telefono_movil` a `_ENRICH_TARGET_FIELDS` (`app.py:934`) para que el detective pueda pisar el WhatsApp derivado-del-fijo con uno real.

### Detalles de implementación
- Nueva confianza en `_FACT_CONFIDENCE`: `social` > `websearch` (el link-in-bio es dato declarado por el propio comercio).
- El `whatsapp` hallado por el detective debe marcarse `wa_source='social'` para diferenciarlo del `derived` (fijo disfrazado). La UI ya tiene el badge — que muestre "Verificado (IG/Linktree)".
- Respetar el `LM_WORKER_BUDGET`: cada lead con cadena social suma ~2 Serper + 1 Gemini extra. Medir el costo incremental en `cost_ledger` (kind='enrich').
- No romper el cortocircuito `no_source`: si no hay sitio NI IG NI resultado social → sigue siendo terminal.

### Backlog de fuentes del detective (orden de valor)
1. Link-in-bio (Linktree/Beacons/etc.) — **el caso de Andrés, empezar acá**
2. Facebook page (suele tener teléfono/WhatsApp público y horarios)
3. Perfil IG público vía snippet de Serper (bio a veces trae el número)
4. Google Business "mensajes" / sitio del menú (PedidosYa, etc.)

**Esfuerzo:** 1-2 días (medio día el MVP de Linktree, el resto robustez + Gemini + tests).

---

## P1 — Import de cartera (nuevo `POST /api/import`)

**Por qué:** hoy el comercial vive en dos sistemas y —peor— la app le cobra créditos por clientes que ya son suyos y le sugiere un icebreaker de primer contacto a un cliente de años. Import lo arregla de raíz.

### Diseño
- **Endpoint** `POST /api/import` (multipart CSV o texto pegado). Importar `UploadFile` de FastAPI (hoy ni se importa).
- **Parser tolerante:** aceptar columnas mínimas (nombre, dirección/localidad, teléfono, opcional: estado). Mapear encabezados en español con fuzzy (nombre/comercio/local; tel/teléfono/whatsapp).
- **Dedup + match:** por (nombre normalizado + localidad) o teléfono contra `global_places`. Si matchea, linkea al `global_place_id` existente; si no, crea uno nuevo.
- **Marcar como cliente:** cada fila importada crea un `saved_leads` con `origen='importado'` y permite setear `outcome='ganado'` (o estado `cliente`). Así entra a la cartera **sin cobrar créditos**.
- **Bonus elegante — dedup pre-búsqueda gratis:** como `/api/leads` ya filtra los `saved_leads` de la marca del resultado de Places, **con solo crear los importados como saved_leads, la búsqueda deja de devolver y cobrar clientes existentes.** No hay que tocar el dedup: cae solo.

### Detalles
- Tope de filas por import (ej. 5.000) + validación de tamaño de archivo.
- Preview antes de confirmar: "detecté 312 filas, 47 ya estaban en tu base, 265 nuevas → importar como cartera activa".
- No cobrar créditos por el import (es data del propio user).
- Registrar en `lead_events` para el timeline.

**Esfuerzo:** 1 día.

---

## P1 — Export (ya existe, cerrar gaps)

`GET /api/export` ya da csv/xlsx/json/pdf (`app.py:3250`). Falta menor:
- Confirmar que exporta los campos de contacto enriquecidos (whatsapp real, nombre_contacto, instagram) y el estado del pipeline.
- Botón claro en la UI de "Exportar mi base / esta vista" (respetando el filtro activo).
- **Round-trip:** que el CSV que exporta sea re-importable (mismos encabezados) → import/export cierran el círculo con el Excel del cliente.

**Esfuerzo:** 2-3 h.

---

## P2 — Quick wins que se acoplan

- **Filtro `min_fit` antes de cobrar** (`/api/leads`): parámetro de umbral para no cobrar leads fit<X. Hoy no existe (`app.py:2654`). Devuelve control de calidad al que paga.
- **`whatsapp` como target del detective:** (ver P1) que un WhatsApp real pise al derivado-del-fijo.
- **Marcar "ya es cliente" sin importar:** acción rápida en la ficha para excluir de futuras búsquedas aunque no haya importado CSV.

---

## Orden sugerido de ejecución

1. **P0.1 Serper** (10 min, revive el detective) → **P0.2 re-encolar** (5 min) → **P0.3 Baileys** (30 min). *Hoy.*
2. **P1 Import** (1 día — desbloquea la mitad retención del producto y mata la queja "pagué por mi cliente").
3. **P1 Detective social** (1-2 días — el caso Bio Solo Orgánico y la contactabilidad real).
4. **P1 Export round-trip** + **P2 filtros** (medio día).

> Regla de oro: nunca deployar a mano. `./run-tests.sh` → `./deploy.sh` (tests→backup→rsync→smoke→rollback).

---

## Proyecto: WhatsApp oficial de Góndola vía WABA (decidido 04-jul)

**Contexto:** Baileys (chip 5491165857832) se restringió al hacer outreach (error 463 + device_removed 2x en un día — ver memoria [[project_wa_baileys_outreach]]). Decisión: canal WA de Góndola pasa a **WABA oficial**, reciclando la de Smart Foods (que Andrés libera). WABA `1399636844706704`, número +54 9 11 2527-0390, **calidad GREEN**, 30 plantillas approved (todas de SF).

**3 frentes (la ruta crítica es Meta):**
1. **Re-branding del número** ✅ ENVIADO 04-jul (Claude, vía Chrome en el WhatsApp Manager). `verified_name` "Smart Foods" → "Góndola": `new_name_status=PENDING_REVIEW`, quality GREEN intacta. Meta aprueba el nombre en 2-5 días. **Foto de perfil ✅ cambiada al logo de Góndola** (04-jul, vía Cloud API: resumable upload → handle → whatsapp_business_profile; se aplicó al instante, sin revisión). Avatar PNG generado en `~/lead-machine/brand/gondola-avatar.png` (qlmanage del app-icon SVG, 640×640 fondo verde sólido). **Andrés desvincula el smartbot mientras Meta revisa el nombre** (el nombre no cambia hasta la aprobación, hay tiempo).
2. **Plantilla de Góndola** ✅ CREADA 04-jul (Claude, vía API). `gondola_reactivacion_v1` (id 1565387291852615, MARKETING, es_AR), body {{1}}=marca {{2}}=créditos, botón URL estático a gondola.ar → estado **PENDING** (Meta revisa). Cumple `~/.claude/rules/wa-template-rules.md`.
3. **Integración Cloud API en lead-machine** ✅ HECHO 04-jul (`2da127c`, deployado). `send_whatsapp_template(phone, template, params)` a la Graph API + `/api/admin/wa-blast` (dry-run probado = 7 destinatarios). Config `WA_ACCESS_TOKEN`/`WA_PHONE_NUMBER_ID`/`WA_TEMPLATE_LANG=es_AR` copiada de smartbrain al .env de lead-machine. Cadena técnica **validada** (test dio `#132001 template not found` = auth+envío OK, solo falta crear la plantilla). Falta solo: Frentes 1 (re-branding) y 2 (plantilla `gondola_reactivacion_v1`), ambos de Andrés en Meta.

**Regla de oro (de la sesión):** WABA es para usuarios PROPIOS con opt-in (se registraron), NO para leads fríos scrapeados (eso quema la WABA — ver decisión de validación abajo). El `/send` de Baileys queda solo para validación onWhatsApp del detective y responder 1:1.

**Mientras tanto (esta semana):** reactivación por EMAIL (Resend, 23 usuarios) es el camino rápido; la WABA es el canal permanente que se construye en paralelo.

### Pipeline B2B de intermediación (SmartBrain tenant gondola) — construido 04-jul noche
Decisión: se usa **SmartBrain tenant gondola** (no un frontend nuevo en la app). Flujo: mover lead a "Primer Contacto" en el CRM → secuencia activa → dispatcher manda 1er msg por WABA → respuesta → SmartBot gondola.
- ✅ **CRM poblado**: 2.090 leads del detective (leadmachine.db/global_places) → `crm_leads` de ops_gondola.db (`origen=gondola_detective`, `brand_id=gondola`, `optin_whatsapp=0` = FRÍOS). Dedup por teléfono.
- ✅ **Plantilla** `gondola_b2b_primer_contacto` (id 1023748130638938) creada en Meta → PENDING. Body con {{1}}=nombre dietética.
- ✅ **Secuencia** "Primer contacto Góndola" en `crm_sequences` (etapa_trigger=primer_contacto, brand_id=gondola). `_activate_sequence` la engancha al mover a la columna.
- ✅ **Ruteo inbound** (webhook.py de SmartBrain): `PHONE_TENANT_MAP` mapea `phone_number_id 1057793384074433 → gondola`; early-return quirúrgico + `_save_inbound_to_tenant` (aislado, no toca lógica de SF). Testeado con payload simulado: cae en gondola, NO en smart-foods. Número es 100% de Góndola (SF lo libera). Backup del webhook en `/tmp/webhook.py.bak.*`.
- 🔲 **Falta**: sumar gondola al cron del dispatcher (con flag de activación) + aprobación de Meta (nombre + plantilla) → activar. Los leads son FRÍOS: outreach con canary/cuidado, no blast.

---

## Email lifecycle (Resend) — ✅ EN PROD, blast 23/23 enviado 04-jul

**ACTUALIZACIÓN 04-jul (tarde):** dominio `gondola.ar` VERIFICADO en Resend (envía desde `hola@gondola.ar`). Campaña de reactivación **enviada a los 23 usuarios (23/23)** con la garantía Nivel 1 incluida, +10 búsquedas cargadas a cada uno. Contraste del día: email 23/23 vs WhatsApp Baileys 1/4 (chip restringido, error 463). **Email = canal de reactivación.**

**Garantía de cobro Nivel 1 — ✅ DEPLOYADA (commit b210fe3):** `/api/leads` cobra SOLO leads con WhatsApp de contacto (`_save_leads` devuelve nuevos + nuevos_con_wa; billable = 2º). "Si no tiene WhatsApp, no te lo cobramos." Nivel 2 (WhatsApp verificado) pendiente = requiere validación confiable (onWhatsApp robusto / servicio; NO validar-por-envío que quema la WABA). El "bot que registra entrega/respuesta" va para el CRM de outreach del usuario (no validación masiva).

---

## Email lifecycle (Resend) — infra (CÓDIGO HECHO 04-jul)

Canal de email a los usuarios registrados (23 al 04-jul; la app antes solo notificaba por WA/Telegram). Servicio elegido: **Resend** (free 3.000/mes; dominio raíz `gondola.ar`; remitente `hola@gondola.ar`).

**Implementado y deployado (`b16d822`), no-op hasta setear la key:**
- `send_email(to, subject, html, unsubscribe_bid)` → POST a Resend; `EMAIL_FROM` configurable.
- Columna `brands.unsubscribed` + endpoint público `GET /api/unsubscribe?u=<token HMAC>`.
- **Welcome** automático al registrarse.
- `POST /api/admin/email-blast` (dry_run por defecto) para campañas: respeta `unsubscribed`, excluye test/internal, pie de baja obligatorio. Dry-run verificado = 23 destinatarios.

**Falta (pasos de Andrés, ~20 min):**
1. resend.com → Add Domain `gondola.ar` → copiar los registros DNS (SPF TXT, DKIM `resend._domainkey`, DMARC) a **Cloudflare** (DNS only, nube gris).
2. Verify en Resend → generar API key.
3. Poner en `/opt/lead-machine/.env`: `RESEND_API_KEY=...` (y opcional `EMAIL_FROM=Góndola <hola@gondola.ar>`) → `systemctl restart lead-machine`.

**Cuando esté la key:** test de welcome + campaña de reactivación a los 23 (dry-run → real). DNS gestionado en Cloudflare (NS penny/kenneth). Sin MX/SPF/DMARC previos (limpio).

---

## Decisión: cómo se valida el WhatsApp (y por qué NO con la WABA) — 04-jul

Surgió la idea de usar la WABA (Cloud API oficial de Meta) con una plantilla para validar los números. **Descartado.** Razones, para que no vuelva a proponerse:

1. **La Cloud API no valida sin enviar.** Meta removió el endpoint de contacts/validación silenciosa; hoy *"there is no longer a way to explicitly check if a phone number has a WhatsApp ID... send it directly after they have opted-in"* ([Meta docs](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/phone-numbers)). Con la WABA, **validar = enviar**. Una "plantilla para validar" es un envío disfrazado.
2. **Enviar plantillas a leads fríos scrapeados = quema de la WABA.** Números sin opt-in → bloqueos/reports → cae la calidad → restricción/baneo. Viola el opt-in de business-initiated y las reglas de `~/.claude/rules/wa-template-rules.md`.
3. **Arriesga el número de la propia marca** (el "chip WABA que no uso" es el comercial de Smart Foods) por una validación que ni siquiera es silenciosa.
4. **No resuelve "que no falle el envío":** el vendedor escribe desde SU WhatsApp (`wa.me`), no desde la WABA de Góndola. Son canales distintos.

**Lo que sí se hace:**
- **Validación silenciosa** vía Baileys `onWhatsApp` (no-send, gratis) — ya existe; robustecida el 04-jul (ver P0.3).
- **Dato declarado** vía detective social (Linktree/IG): el WhatsApp que el comercio publica ya tiene WhatsApp y es el de ventas — mejor que validar (ver P1 Detective social).
- **La WABA sí sirve, pero para OUTREACH con opt-in** (nutrir tibios/clientes), con la WABA de cada marca cliente — nunca para tocar fríos ni para validar.

---

Relacionado: [[handoff-v2-completo]] · [[roadmap-contactar-vender]] · [[project_lead_machine]] · [[project_wa_baileys_outreach]]
