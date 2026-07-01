---
date: 2026-06-16
type: playbook
tags: [korean-root, b2b, campañas, outreach, whatsapp, smartbrain]
status: activo
---

# Korean Root — Cómo hace el equipo las campañas B2B (paso a paso)

> Para el equipo de Victoria (no técnico). Sección **B2B** del SmartBrain. Contacto SOLO por **API oficial de WhatsApp** (sin chip, sin wa.me manual — ya está configurado así).

## Estado verificado (jun 16 2026)
- WhatsApp oficial de KR (**+54 9 342 651-6417 "KR SRL"**): **CONNECTED, calidad GREEN, envío FUNCIONA** (probado con message_id real). El problema del 12/jun está resuelto.
- Pipeline con **637 leads** cargados.
- Hay una campaña de **EJEMPLO en borrador** ("EJEMPLO — Primer contacto mayoristas") en Campañas para que la vean.

## ⚠️ Prerrequisito para outreach EN FRÍO (importante)
WhatsApp (Meta) **no deja mandar un mensaje libre a alguien que nunca te escribió** — el primer contacto en frío **debe ser una plantilla aprobada por Meta**. KR hoy solo tiene aprobadas las plantillas de Salto Cuántico (`sc_*`); **faltan plantillas B2B** (primer contacto / recordatorio mayorista).
- **Para contactar leads en frío**: hay que crear esas plantillas B2B en Meta Business Manager → WhatsApp → Plantillas, y esperar aprobación (1-2 días). Una vez aprobadas, se usan en la secuencia.
- **Para responder a quien YA te escribió** (ventana de 24h abierta): se puede mandar texto libre sin plantilla.

## El flow, paso a paso

### 1. Conseguir leads (si hace falta)
- **B2B → Pipeline → "Scraper Google Maps"** (wizard de prospección): elegís zona y tipo (dietéticas, farmacias, cosmética, salud), ves vista previa + costo, e importás.
- O **Importar CSV** (botón Importar): nombre, contacto, teléfono, zona, tipo…
- O entran solos por la **landing mayorista** (`/mayoristas`).

### 2. Clasificar (si aparece el tab "Clasificar (N)")
- Cada lead nuevo: **Cliente** / **Lead** / **Eliminar**. Se puede en lote.

### 3. Ver y mover en el Pipeline
- **B2B → Pipeline**: leads por etapa (prospecto → primer contacto → interesado → …). Abrís una ficha para ver datos, notas e historial. Botones **Contactado / Follow-up / Cerrar** registran cada paso.

### 4. Armar la campaña (tab **Contactar**)
1. **B2B → Contactar** (ahora visible para el equipo, no solo CEO).
2. Elegís la **audiencia**: tipo de negocio + zona + score. Abajo ves la **vista previa**: cuántos leads y cuántos con teléfono.
3. Escribís/elegís los **mensajes**: 1er contacto + recordatorios (con su demora en horas). Hay plantillas KR pre-armadas por tipo de negocio.
4. **Crear secuencia** → queda en **BORRADOR**. No sale nada todavía.

### 5. Aprobar y enviar (sección **Campañas**)
- La secuencia creada aparece en **Campañas** en estado *borrador*.
- Ahí se **revisa y aprueba** → recién ahí empieza a salir por el WhatsApp oficial, espaciado.
- (Si es outreach en frío, los mensajes deben corresponder a plantillas aprobadas — ver prerrequisito arriba.)

### 6. Seguimiento
- En el **Pipeline / ficha del lead** ves quién respondió. A quien te escribió, le respondés desde la ficha (botón oficial, queda registrado).

## Reglas / notas
- **Solo API oficial**: no hay "chip propio" ni botones de WhatsApp manual (wa.me) — todo sale por el número oficial y queda trazado.
- Los mensajes salen **espaciados** (no todos de golpe) para cuidar la reputación del número.
- Si el banner/estado muestra algún error de envío, suele ser de Meta (plantilla no aprobada o número) — avisar al equipo técnico.
- Recomendación técnica pendiente: sacar la app de terceros "WPP API" suscripta a la WABA de KR (Business Manager), por higiene/seguridad.

Ver también: [[korean-root-conectar-instagram]] (conexión IG para Contenido).
