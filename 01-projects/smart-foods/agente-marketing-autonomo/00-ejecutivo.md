---
date: 2026-04-24
type: executive-summary
tags: [smart-foods, agente, marketing, ejecutivo]
status: v1
---

# Agente Marketing Autónomo — Documento Ejecutivo

## TL;DR en 4 líneas

Construimos un agente autónomo que **trabaja para Smart Foods 24/7** ejecutando marketing (email + WhatsApp), auditando cada mensaje antes de enviar, respondiendo replies, dándote reporte diario y escalando solo cuando es estrictamente necesario. **Objetivo único: maximizar rentabilidad sin que Meta nos considere spam.**

---

## 1. Qué hace el agente

### En 1 frase
**Toma decisiones de marketing dentro de un envelope que vos definís, ejecuta, mide, reporta y aprende.**

### Las 7 capas vivas

| Capa | Qué hace | Cuándo se dispara |
|---|---|---|
| **1. Decisor** | Elige qué campaña lanzar, a quién, cuándo | Consume los triggers existentes (lifecycle crons, plan semanal) + policies |
| **2. Mitigador de riesgo** | A/B test del 5% antes de escalar, umbrales OR/CTR/ROAS, anti-fatigue | Antes de cada envío masivo |
| **3. Curador de calidad** | Bloquea copy con términos regulados (ANMAT), menciones de "cápsula", URLs rotas, cupones falsos | Cada 15 min sobre campañas pendientes |
| **4. Guardia de integridad** | No-dobles, exclusiones automáticas, respect kill switch, budget caps | En cada envío |
| **5. Respondedor de replies** | SmartBot existente responde; si falla → auto-fix via el agente | En tiempo real + verificación cada 2h |
| **6. Reportero** | WhatsApp diario 8:30 ART con todo lo hecho + pedidos de input | 1×día |
| **7. Escalador** | Te avisa por WA en HUMAN_REQUEST, REGULATORY_RISK, circuit breaker | En tiempo real cuando hace falta |

---

## 2. Qué decide solo vs qué te pide

### Decide SOLO (sin pedirte nada)

- Lanzar campañas a segmentos existentes con descuento ≤15%
- Hasta 3 campañas/día
- Responder replies: baja, consulta precio, info producto, objeciones estándar
- Pausar campañas con performance bajo umbral
- Crear/desactivar cupones Shopify ≤15%
- Retry de errores técnicos transitorios
- Detectar y procesar opt-outs cross-channel (WA + email + Klaviyo)

### Te informa (push WA, no necesita tu OK)

- Cada campaña lanzada
- Pausas automáticas con motivo
- Al cruzar 70% y 90% del budget mensual
- Errores recuperados solos
- Auto-fix de bajas no procesadas por el bot

### Te pide input (y espera)

- Descuentos >15%
- Segmentos nuevos primera vez
- Lanzamientos de producto
- Cliente pide hablar con humano explícito
- Detección de riesgo regulatorio (ANMAT, prensa, legal)
- Budget extraordinario
- Shopify/Klaviyo caído >2h

### KILL SWITCH

El agente pausa TODO automáticamente si:
- Tasa de bajas 24h >5%
- Detecta REGULATORY_RISK en una conversación
- 3 campañas consecutivas falladas

Vos también podés activarlo manualmente: `POST /api/agent/kill-switch` o respondiendo "STOP" al bot por WA.

---

## 3. Cómo verlo en acción

### 3.1 WhatsApp — tu canal principal

**Todos los días 8:30 ART** te llega un único mensaje con:
- Qué campañas ejecutó ayer
- Replies del bot (total + % resueltas + escalaciones)
- Revenue atribuido + mes a la fecha
- Pedidos de tu input (con número para responder SÍ/NO)
- Bloqueos técnicos si hay

**En tiempo real** te llega WA solo cuando:
- Hay una escalation (HUMAN_REQUEST / REGULATORY_RISK)
- El circuit breaker se activó
- El quality gate bloqueó una campaña que estabas por enviar
- Cruzaste 70%/90% del budget

### 3.2 Dashboard — endpoints para consultar

Accesibles desde el dashboard con tu JWT (o via `curl` si preferís):

| Endpoint | Qué muestra |
|---|---|
| `GET /api/agent/status` | Estado actual + kill switch on/off |
| `GET /api/agent/policy` | Las 34 policies que definen el envelope, agrupadas por categoría |
| `GET /api/agent/quality/summary?days=7` | Cuántas campañas auditadas, cuántas bloqueadas, top violations |
| `GET /api/agent/quality/log?only_blocked=true` | Log de cada bloqueo con motivo |
| `GET /api/agent/replies/summary?days=7` | Conversaciones verificadas por clasificación |
| `GET /api/agent/replies/log?only_escalated=true` | Las escalaciones con su contexto |

### 3.3 Inbox (SmartBot) — conversaciones flaggeadas

Las conversaciones que el agente marca como `starred` con `priority=high` aparecen arriba en el Inbox. Son las que piden tu atención directa (cliente pidió hablar con humano, riesgo regulatorio, etc.).

### 3.4 Chat con el agente

**NUEVO**: podés conversar con el agente en modo chat para:
- Preguntar qué hizo y por qué
- Ajustar policies sobre la marcha ("subí el descuento max a 18%")
- Pedir análisis de performance ("qué campañas funcionaron mejor esta semana")
- Definir estrategia conjunta

Ver sección 6.

---

## 4. La regla rectora: maximizar rentabilidad sin SPAM

### Filosofía

**Mejor no mandar que mandar mal.** Cada guardrail existe para proteger una de dos cosas:

1. **Tu reputación en Meta** (calidad de WA number, no ser flaggeado como spam)
2. **Tu margen de contribución** (no gastar en descuentos o en adquirir clientes de bajo LTV)

### Cómo el agente protege Meta

- **Templates Meta aprobados siempre** — nunca free-text masivo
- **Anti-fatigue**: cliente no recibe >3 mensajes en 30d, ni 2 en <14d
- **Exclusión automática** de unsubscribed en WA + Klaviyo
- **Rate limiting** con dedupe 24h (evita doble envío)
- **Kill switch automático** si la tasa de bajas 24h sube del 5%

### Cómo el agente protege el margen

- **Budget cap mensual** de $500k ARS en descuentos — no se puede exceder sin tu OK
- **Umbrales de performance**: campañas con ROAS <2× a 72h se pausan solas
- **A/B test con 5% previo** antes de escalar a toda la audiencia
- **Descuento max autónomo 15%** — ceiling absoluto 30% (necesita tu OK)
- **Atribución por cupón único**: cada campaña con su cupón trackeable a Shopify

### Cómo se equilibra

Si el agente detecta que una campaña tiene alta tasa de conversión pero alta tasa de baja, **prioriza la baja** (riesgo Meta > oportunidad revenue).

Si detecta que una campaña tiene baja tasa de baja pero ROAS <2×, la pausa (ineficiencia de capital).

**Si los dos pasan al mismo tiempo — escala y pide tu criterio.**

---

## 5. Los hallazgos reales del primer día

En las primeras 24h de operación el agente detectó:

1. **1 consulta médica grave** en el WhatsApp: "quisiera usar adaptógenos para mi hija de 12 años con epilepsia, indicación del pediatra". Kill switch automático + escalación a Flor. Caso cerrado. También dejó un KB nuevo para que el bot responda estas consultas con referral a `smartfoods.ar/pages/red-de-profesionales`.

2. **1 URL fantasma** en emails: `/pages/historia` está linkeada en 4 campañas pero no figura en el url_catalog. Decisión pendiente tuya: agregarla o quitar los emails.

3. **3 BOT_FAILED** — cosas como que el cliente dijo "Hola" y el bot respondió con alerts de stock bajo. Mejora concreta para el KB del bot.

4. **4 falsos positivos tuneados en vivo**:
   - "trata" sacado del blocklist regulatorio (matcheaba "se trata de")
   - "UTF-8" agregado al ignore list de cupones
   - URLs `.jpg`, `.png`, `w3.org` filtradas (assets/infra)
   - Doble chequeo de evidencia textual antes de auto-desuscribir

---

## 6. Próximo: chat con el agente

Estamos agregando **chat bidireccional** en la UI para que puedas:

- Conversar con el agente sobre estrategia
- Ajustar policies conversacionalmente ("subí el cap de descuento a 20% este mes por liquidación de stock")
- Pedir análisis ("mostrame el funnel de la campaña VIP de marzo")
- Definir experimentos ("probemos un segment de compradores 60d con un cupón del 18%")
- Debatir decisiones ("¿qué pensás de pausar las campañas los domingos?")

**Filosofía**: el agente tiene el poder de actuar solo dentro del envelope, pero vos podés expandir/contraer ese envelope en conversación. Cada cambio queda registrado con tu nombre + motivo en `agent_policy`.

---

## 7. Checklist para vos

### Esta semana
- [ ] Chequeá los briefings diarios WA a las 8:30. Si el formato te gusta, seguimos. Si no, me decís qué cambiar.
- [ ] Respondé las escalaciones cuando lleguen (el agente te pasa la cita literal del cliente).
- [ ] Probá el chat con el agente (sección 6, cuando esté live).

### Si algo se desmadra
- Kill switch: `curl -X POST -H "Authorization: Bearer <jwt>" -H "Content-Type: application/json" -d '{}' http://76.13.228.77:8080/api/agent/kill-switch`
- O decís "STOP" por WhatsApp al bot (ya existe ese detector)
- O ajustás una policy específica sin parar todo

### Cuando veas que algo falta
- Agregar trigger nuevo → me pedís y lo hago
- Expandir envelope → `PUT /api/agent/policy/{key}` o vía chat
- Cambiar frecuencia de cron → editamos el crontab

---

## 8. El único objetivo

**Que vos trabajes MENOS y Smart Foods venda MÁS, sin riesgo de quedar flaggeados en Meta como spam.**

Si el agente está fallando en uno de esos tres frentes (tu tiempo, revenue, reputación), me decís y lo arreglamos.

---

## 9. Enlaces rápidos

- [[index|Estado técnico completo del proyecto]]
- [Dashboard](http://76.13.228.77:8080/) — UI principal
- Crons activos: `ssh root@76.13.228.77 "crontab -l | grep agent"`
- Logs del agente: `/var/log/agent_daily_briefing.log`, `/var/log/agent_monitor.log`, `/var/log/quality_shadow.log`, `/var/log/reply_verification.log`
