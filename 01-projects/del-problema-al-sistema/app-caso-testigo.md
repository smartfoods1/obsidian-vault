---
date: 2026-06-21
type: project
tags: [del-problema-al-sistema, app, caso-testigo, whatsapp, agente]
status: en-progreso
---

# App del caso testigo — Empleado de ventas en WhatsApp

La app de referencia que Andrés construye en vivo, etapa por etapa, y que cada alumno replica en su negocio (sobre canal de baja fricción). Es la columna vertebral de la demo. Volver al [[index|índice]] · ver [[curriculum-y-guiones|guiones]].

## Qué es

Un agente de IA que atiende la **primera línea de consultas de venta en WhatsApp**: responde sobre productos, califica al interesado y deriva/agenda los leads calientes a un humano. No reemplaza al vendedor: le saca de encima el 80% repetitivo y le pasa lo que vale la pena.

## Alcance (claro, para no excederse)

**Hace (v1):** responde consultas de producto/precio/envío/pago, recomienda, califica (¿comprador real?, ¿qué busca?, ¿urgencia?), propone siguiente paso, deriva el caliente a un humano.
**No hace (v1):** cobrar pagos, gestionar stock en tiempo real, post-venta/logística, dar descuentos no autorizados. Definir esto explícito evita que el alumno se exceda de alcance y no termine nunca.

## Arquitectura mínima

```
mensaje entrante (canal) → webhook → arma contexto
   (system prompt + KB + historial del contacto)
   → LLM (vía el harness) → respuesta → envía por el canal
```
- **Estado:** historial por contacto (memoria de conversación).
- **Handoff:** si dispara una regla → notifica al dueño + marca la conversación.
- **Stack:** Python (el harness lo arma con Claude Code) · SQLite (historial + leads) · canal vía Baileys/WhatsApp Web (demo de Andrés) o Telegram/widget web (alumnos) · corriendo en el VPS con systemd.

## Desglose etapa por etapa (qué se construye cada semana)

**S1 · Detectar** — Definir el trabajo: "atender la primera línea de consultas de venta y calificar". Frase + alcance in/out. Todavía no se escribe código; se define el problema.

**S2 · Traducir** — La ficha del empleado:
- *Qué sabe:* catálogo, precios, envíos, formas de pago, FAQ, horarios.
- *Qué decide:* entender la necesidad, recomendar, calificar, proponer siguiente paso.
- *Qué NO toca:* no inventa precios/stock, no promete descuentos, no cobra; ante duda o lead caliente → humano.
- *Entregable:* system prompt + KB estructurada.

**S3 · Conectar** — Las piezas:
- Webhook del canal recibe el mensaje.
- Se inyecta la KB + el historial al prompt.
- El LLM responde y se envía por el canal.
- (Opcional) Google Sheet para precios/stock o para loguear leads.
- *Entregable:* contesta un mensaje real punta a punta.

**S4 · Construir** — Comportamiento:
- Flujo: saludo → entender → recomendar → calificar → CTA (agendar/derivar/link).
- Memoria por contacto (recuerda el hilo).
- Guardrails: qué nunca dice; tono de marca.
- Handoff: disparadores (pide humano, lead caliente, queja, fuera de alcance) → notifica al dueño.
- *Entregable:* diálogo completo que avanza a venta o derivación.

**S5 · Lanzar** — Producción:
- Deploy en el VPS (systemd), 24/7, con restart automático.
- Logging de conversaciones + métricas (atendidos, derivados, calientes).
- Monitoreo básico / alertas.
- Paso a WhatsApp oficial (WABA) — upsell de setup.
- *Entregable:* sistema en producción atendiendo de verdad.

## Notas pedagógicas

- Andrés construye sobre WhatsApp (Baileys) como demo; el alumno replica en Telegram/web (cero fricción). El concepto se transfiere, el canal es intercambiable.
- **Dónde se traba el alumno (blindar):** credenciales del canal (S3), deploy al server (S5), debugging de un error (transversal). Tener plantillas + entorno preconfigurado + plan B en la nube.
- Capturar el "antes/después" del caso de cada alumno para prueba social.
