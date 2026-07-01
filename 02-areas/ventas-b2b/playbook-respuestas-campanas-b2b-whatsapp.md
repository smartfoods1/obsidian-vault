---
date: 2026-06-22
type: playbook
tags: [b2b, whatsapp, korean-root, smartbrain, ventas, mayorista]
status: activo
---

# Playbook — Manejo de respuestas y proceso de venta B2B por WhatsApp

> Diseñado para el lanzamiento de campañas B2B de Korean Root (jun 2026), pero aplica a cualquier tenant del módulo B2B compartido (SF + KR). Modelo: **bot califica → humano cierra**.

## Decisiones tomadas (Andrés, 22/06/2026)

- **Dueño del inbound B2B de KR**: Victoria / su equipo.
- **Reparto bot vs humano**: bot califica + entrega colateral 24/7; el humano negocia y cierra.
- **Postura de lanzamiento**: fix-then-launch (cerrar los 5 puntos + canary antes de meter volumen).

## Proceso de venta (etapas, mapean a `crm_leads`)

`prospecto` → `primer_contacto` (template enviado) → `interesado` (contestó) → `negociacion` (pidió precio/muestra/condiciones) → `venta` (primer pedido) → `postventa` (recompra). Salida: `no_interesado`.

El sistema ya auto-promueve `primer_contacto → interesado` al recibir respuesta. El gap está de `interesado` en adelante.

### Reparto de tareas
- **Bot (instantáneo, 24/7)**: acusa recibo, clasifica intención, 1-2 preguntas de calificación (¿local físico? ¿qué vendés hoy?), manda one-pager + lista mayorista, captura datos (comercio, zona, dirección para muestra), marca caliente, hace handoff.
- **Humano (Victoria, horario comercial)**: negociación, condiciones a medida, cierre, logística del primer pedido. Relación y recompra = humano.

## Triage de respuestas entrantes

| Intención | Acción del bot | ¿Humano? |
|---|---|---|
| "Contame más" / interés genérico | One-pager + pregunta calificadora | Solo si califica caliente |
| Pide precio | Lista mayorista (volumen + margen) | Sí, para cerrar |
| Pide muestra | Captura comercio + dirección → marca pedido de muestra | Sí, despacho |
| "¿Quién sos?" | Intro de marca desde la KB | No |
| Negativo | Despedida amable, `no_interesado`, re-nurture | No |
| Confusión B2C | Rutea a flujo B2C | No |

Regla dura: bot instantáneo, **humano con SLA definido**. Sin dueño mirando el inbox, el triage no sirve.

## Estado real del sistema KR al 22/06/2026 (auditado)

- **WABA penalizada**: 352 fallos `131049` ("healthy ecosystem engagement") del 20/06 + errores hoy `Missing WA credentials for bot 'korean-root'`.
- **Sin B2B real corrido aún**: `wa_auto_sends_log` con `contact_type='b2b'` = 0. Las campañas 45/46 eran promos B2C (la 45 es la que reventó el 18/06 con el bug de saltos de línea, 1.564 fallidos).
- **Handler de respuestas gateado a SF**: `_B2B_REPLIES_ACTIVE = (BRAND_ID == "smart-foods")` en `webhook.py` → KR recibe genérico, sin colateral ni handoff. Templates `sf_b2b_*` son de hongos de SF.
- **Atribución rota**: campañas salen por `unified_campaign_contacts`; el handler busca el envío previo en `wa_auto_sends_log`. No coinciden → respuesta huérfana.
- **Sin dueño humano para KR**: handoffs notifican a Andrés vía `users.json` de SF.

## Checklist fix-then-launch (orden)

1. **Sanar WABA**: quality GREEN + resolver `Missing WA credentials`. (Meta + verificación VPS)
2. **Templates KR APPROVED**, cuerpo `{{1}}` en un solo párrafo (anti-`#132018`), contenido desde la KB. Redacción = Claude; submit en Meta = equipo KR. Palo largo: arrancar por acá.
3. **Activar path de respuestas KR**: des-gatear `_B2B_REPLIES_ACTIVE` (data-driven desde `brand_context`, no hardcode) + reconciliar `_handle_b2b_campaign_reply()` para matchear contra `unified_campaign_contacts` por teléfono.
4. **Handoff a Victoria**: equipo KR trabaja el inbox del dashboard (Conversaciones, BOT→humano) + ping de aviso.
5. **Canary end-to-end** (1 número real: loguea + auto-responde + marca caliente + avisa) → rollout con `WA_SEND_FRACTION` + cap chico.

## Inputs pendientes de Andrés/Victoria

1. Lista mayorista KR (precios por volumen, MOQ, política de muestra).
2. Acceso/rol de Victoria al dashboard + ¿número para ping?
3. Confirmar audiencia: los 255 leads `dietética` ¿son los ~636 migrados de SF (28/05)? Riesgo de solapamiento de canal SF↔KR sobre la misma dietética.

## Definiciones finales (Andrés, 22/06)
- **Handoff**: inbox del dashboard (Conversaciones) + ping WA a **+54 9 342 444 6605** (línea oficial KR / Victoria, confirmada en `brand_context/identity/location`).
- **Audiencia**: 255 leads `dietética` (parte de los ~636 migrados de SF) → van OK, decidido.
- **Lista mayorista**: la arma el equipo de KR (precios/volumen/MOQ/muestra).

## Producto real de KR (grounding para todo el copy)
- **NO es** coreana/K-beauty, **NO** vende hongos ni cápsulas (eso es Smart Foods). Argentina, nutricosmética + bienestar funcional.
- **Estrella**: Limonada Cuántica (polvo efervescente; 9 aminoácidos esenciales + probióticos + vitaminas; inédita en Arg; RNPA 21-136658; sin TACC; $36.990).
- Formulación Cuántica Solar (60 comprimidos + biotina + betacaroteno; $36.990). Shakti Booster (creatina monohidrato ultramicronizada; $24.990). Aceites (orégano 70% carvacrol, cúrcuma+pimienta).
- **Audiencia**: mujeres 34-55 (persona "Carolina"), sub-línea Irradie.
- **Voz**: wellness cercano, educativo, oraciones cortas, sin sobreventa. SÍ: funcional, ingrediente, ritual, vitalidad, inteligente, longevidad. NO: milagroso, cura, 100% efectivo, comprobado, mágico, único.
- **Compliance**: ANMAT/INAL. Forbidden: cura enfermedades, reemplaza tratamiento, efecto inmediato garantizado.

## Templates B2B KR — SUBMITEADOS A META (PENDING, 22/06/2026)
Cargados en `wa_templates` (brand_id=korean-root) y enviados a aprobación vía la lógica canónica (`templates.py`/`_build_meta_payload`) a la WABA 459813607216452:
- `kr_b2b_dieteticas_intro` → wa_templates **id 11**, meta_id **28015376891393584**, status **PENDING**
- `kr_b2b_followup` → wa_templates **id 12**, meta_id **982095114636995**, status **PENDING**

Categoría MARKETING, es_AR. Diseño: cuerpo estático (admite saltos) + `{{1}}` = nombre del comercio (único param dinámico, de una línea → evita `#132018`). Botones QUICK_REPLY fijos ("Quiero la lista", "No, gracias") → compatible con dispatcher actual. Para chequear estado: endpoint `POST /api/templates/{tid}/sync` o `GET /api/templates/sync-all`.

**`kr_b2b_dieteticas_intro`** (primer contacto): Hola {{1}}, te escribo de Korean Root, marca argentina de bienestar funcional. Estamos sumando puntos de venta como el tuyo con una línea distinta a lo que ya tenés en góndola: nuestro producto estrella es la Limonada Cuántica, bebida funcional efervescente con 9 aminoácidos esenciales, probióticos y vitaminas — inédita en Argentina, con registro ANMAT y libre de gluten. Apunta a un público de alto valor y recurrente (mujeres de 35 a 55 que buscan vitalidad, piel y energía) y se complementa con la Formulación Cuántica Solar y la creatina ultramicronizada Shakti Booster. Trabajamos con margen para el comercio, material de exhibición y muestras sin cargo. ¿Te paso la lista mayorista y las condiciones?

**`kr_b2b_followup`** (seguimiento 5-7 días): Hola {{1}}, te había escrito desde Korean Root por la línea de bienestar funcional para tu comercio. Resumen: Limonada Cuántica (efervescente con aminoácidos, probióticos y vitaminas, registro ANMAT, sin TACC), Formulación Cuántica Solar y creatina Shakti Booster — con margen para el punto de venta y muestras sin cargo. Si te interesa, hoy te paso la lista mayorista. ¿Avanzamos?

## Estado de implementación (22/06/2026 — DESPLEGADO)
- [x] **Colateral de respuesta KR** — cargado en `brand_context` section `b2b`, keys: `reply_intro` (one-pager + opciones 1/2/3), `reply_precio`, `reply_muestra`, `reply_hablar`, `reply_negativo`, `handoff_phone` (5493424446605), `price_list_url` (vacío hasta que el equipo arme la lista). Aterrizado en producto real (Limonada Cuántica/Solar/Shakti), sin claims prohibidos. Ojo: ya existía `min_order=$360.000` → el `reply_precio` NO promete "sin mínimo".
- [x] **Código** — `webhook.py` parcheado (backup `.bak-20260622-*`). Nuevas funcs `_b2b_ctx` + `_b2b_reply_datadriven`, data-driven, activadas SOLO si el tenant tiene `reply_intro` en brand_context → **SF queda 100% intacto**. Clasifica intención (interés/precio/muestra/hablar/negativo), entrega colateral, marca caliente (`etapa→negociacion`/`interesado`/`no_interesado`), reconcilia atribución en `wa_auto_sends_log` + `unified_campaign_contacts` (marca `wa_replied=1`), y hace handoff (ping a 5493424446605 + queda en CRM/inbox). Validado con test offline (5 intenciones OK, 3 pings, cleanup). smartbrain-api reiniciado sano.
  - **GOTCHA documentado**: `crm_interactions.tipo` en KR tiene CHECK estricto (solo `whatsapp_enviado/recibido, llamada, visita, email, nota, cambio_etapa`). El handler SF original inserta `campaign_reply_*`/`b2b_sample_request` → latent bug que explotaría en KR. Mi path usa solo tipos permitidos (info de atribución va en `contenido`).
- [ ] **Canary end-to-end** (post-aprobación de templates) → mandar a 1 número real, contestar, confirmar reply+handoff+CRM → rollout con `WA_SEND_FRACTION` + cap.

### Pendientes menores (cuando el equipo entregue)
- `price_list_url` / media del catálogo → cargar en brand_context para que el bot lo adjunte.
- Opcional: el notify global de leads (`_get_phone_for("andres")`, webhook.py ~973) sigue yendo a "andres"; si Andrés no quiere recibir pings de leads KR, routearlo a `handoff_phone` (cambio chico, fuera de alcance hoy).
- Handoff "dashboard": hoy el lead queda en CRM (etapa negociacion) + conversación en inbox. Si se quiere un estado explícito "necesita humano" en el inbox, es un follow-up chico.

## Referencias
- `webhook.py` (`_handle_b2b_campaign_reply`, `_handle_b2b_flow_choice`) — VPS KR 103.199.187.246
- Reglas WA templates: `~/.claude/rules/wa-template-rules.md`
- Protocolo campañas masivas: memoria `feedback_wa_campaign_protocol`
- Solapamiento de canal: memoria `project_kr_smartfoods_channel_overlap`
