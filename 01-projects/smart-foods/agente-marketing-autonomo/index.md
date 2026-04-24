---
date: 2026-04-24
type: project
tags: [smart-foods, marketing, agente-autonomo, smartbrain]
status: deployed
version: v3-final
---

# Agente Marketing Autónomo — Smart Foods

> **Estado: deployado y corriendo en producción a partir del 2026-04-24.**
> Primera iteración completa. Observación + tuning las próximas 2 semanas.

## Qué quedó corriendo

### Backend — 5 tablas nuevas en `ops_smart-foods.db`

| Tabla | Uso |
|---|---|
| `agent_policy` (34 policies) | Envelope editable del agente — reglas, umbrales, blocklists |
| `agent_quality_log` | Audit de cada campaña (clean/warn/block) |
| `agent_reply_verification_log` | Clasificación de cada conversación del bot |
| `email_unsubscribed` | Opt-outs email + sync Klaviyo |
| `agent_daily_briefings` | Histórico de briefings WA enviados |
| `agent_monitor_alerts_log` | Alertas del circuit breaker (idempotencia) |

### Módulos nuevos — `dashboard/backend/`

| Archivo | Responsabilidad |
|---|---|
| `agent_policy.py` | get/set/list policies + kill_switch helpers |
| `quality_gates.py` | Validador de copy pre-envío (reg terms, producto, URLs, cupones) |
| `unsubscribe_handler.py` | Cross-channel (WA↔email) + Klaviyo suppression |
| `reply_verification.py` | Clasifica conversaciones del bot con Gemini |
| `routes_agent_policy.py` | `/api/agent/{status,policy,kill-switch,resume}` |
| `routes_quality.py` | `/api/agent/quality/{check,log,summary}` |
| `routes_reply_verification.py` | `/api/agent/replies/{log,summary,run-now}` |

### Hooks en código existente

- `main.py` — 2 routers nuevos registrados (idempotente, con backup `.bak.copiloto`)
- `chatbot_engine.py:915` — llamada a `cross_channel_unsubscribe` ANTES del purge GDPR existente (backup en `.bak.pre_xchannel`)

### Crones activos (VPS crontab)

| Cron | Frecuencia | Archivo |
|---|---|---|
| Quality gate (shadow+enforce) | cada 15 min | `cron_quality_shadow.py` |
| Reply verification | cada 2h (minuto 17) | `cron_reply_verification.py` |
| Daily briefing WA al CEO | 11:30 UTC (8:30 ART) | `cron_agent_daily_briefing.py` |
| Circuit breaker monitor | cada hora (minuto 23) | `cron_agent_monitor.py` |

## Las 7 capas del agente — qué está vivo

| # | Capa | Estado | Cómo se implementa |
|---|---|---|---|
| 1 | **Decisor** | Parcial — consume triggers existentes (`email_strategy_engine`, `cascade_executor`, etc.) | Envelope en `agent_policy` consultado por cada cron |
| 2 | **Mitigador de riesgo** | Vivo | A/B previo, umbrales OR/CTR/ROAS, kill switch |
| 3 | **Curador de calidad** | Vivo (enforce ON) | `quality_gates.py` bloquea → status `quality_failed` + alerta WA |
| 4 | **Guardia de integridad** | Vivo | Idempotency (ya existía) + cross-channel unsubscribe nuevo |
| 5 | **Respondedor de replies** | Vivo | SmartBot existente + `reply_verification.py` auditoría c/2h |
| 6 | **Reportero** | Vivo | `cron_agent_daily_briefing.py` con Gemini 8:30 ART |
| 7 | **Escalador** | Vivo | WA alert para HUMAN_REQUEST / REGULATORY_RISK / circuit breaker |

## Envelope actual (editable vía `PUT /api/agent/policy/{key}`)

### Campañas
- max/día autónomo: **3**
- segmento min: **50** / max autónomo: **5000**
- A/B test sample: **5%** · wait email 6h / WA 2h
- umbrales: OR ≥15%, CTR ≥1.5%, ROAS 72h ≥2×
- anti-fatigue: 14d cooldown, max 3 campañas/customer/30d

### Descuentos
- max autónomo: **15%** · ceiling absoluto: **30%**
- expires default: **14 días**
- cupón único por cliente si segmento >500 o descuento >20%

### Budget
- cap mensual cupones: **$500.000 ARS**
- cap WA sends/mes: **5000**
- alerta al 70% y 90%

### Replies
- bot retry max: 2
- verificación cada 2h
- 9 frases unsubscribe detectadas (incluye "baja", "stop", "borrame")
- 6 frases human-escalation
- 10 frases regulatorias (ANMAT, legal, prensa, etc.)

### Crisis (circuit breaker)
- max tasa baja 24h: **5%** → kill switch automático
- 3 campañas seguidas failed → cooldown 24h
- kill switch manual: `POST /api/agent/kill-switch`

### Quality gates
- 20 términos regulados bloqueados (cura, diabetes, cancer, etc.)
- 6 palabras prohibidas sobre formato (cápsula, pastilla, etc.)
- URLs de assets/infra excluidas (.jpg, .png, w3.org, etc.)

## Endpoints admin

```
GET  /api/agent/status                          → estado + kill switch
GET  /api/agent/policy                          → todas las policies por categoría
GET  /api/agent/policy/{key}                    → una policy
PUT  /api/agent/policy/{key}                    → editar (CEO only)
POST /api/agent/kill-switch                     → pausar todo (CEO only)
POST /api/agent/resume                          → reactivar (CEO only)

POST /api/agent/quality/check                   → test copy arbitrario
GET  /api/agent/quality/log?limit=50            → últimas validaciones
GET  /api/agent/quality/summary?days=7          → agregado semanal

GET  /api/agent/replies/log?only_escalated=true → conversaciones auditadas
GET  /api/agent/replies/summary?days=7          → distribución por clasificación
POST /api/agent/replies/run-now                 → forzar corrida (CEO only)
```

## Primer día de operación real — lo que encontró el agente

Audit manual de 30 campañas email existentes (después de tuning):
- **26 clean** · 4 warn · 0 block

Finding real del gate: `smartfoods.ar/pages/historia` está linkeada en 4 emails pero NO en url_catalog.

Primera corrida reply_verification (60 conversations 48h):
- 48 UNKNOWN · 4 PENDING_OK · 3 BOT_FAILED · 2 RESOLVED_CONVERSION · 1 RESOLVED_INFO
- **1 REGULATORY_RISK real** (epilepsia en menor) → kill switch auto activado, Flor respondió personalmente
- **1 UNSUBSCRIBE_NOT_PROCESSED falso positivo** → falla del LLM, auto-fix revertido, prompt fortificado + doble chequeo en código

## KB adicionada por el caso regulatorio

Nueva entrada `chatbot_kb` id=8, categoría `consulta_medica`:
- 30+ keywords (epilepsia, diabetes, embarazo, pediatra, quimio, etc.)
- Respuesta estándar con link a `https://smartfoods.ar/pages/red-de-profesionales`

Red de seguridad: si el bot falla al usar este KB, el reply_verification lo detecta en la siguiente corrida y activa kill switch + alert.

## Kill switch y recuperación

Kill switch puede ser activado por:
- Andrés manualmente (`POST /api/agent/kill-switch`)
- reply_verification ante REGULATORY_RISK
- monitor ante tasa baja >5% 24h

Para reactivar:
```bash
curl -X POST -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" -d '{}' \
  http://76.13.228.77:8080/api/agent/resume
```

## Backup, reversibilidad, rollback

Todos los cambios son reversibles:
- `main.py.bak.copiloto` backup antes del primer patch
- `chatbot_engine.py.bak.pre_xchannel` backup del hook unsubscribe
- Policies editables sin redeploy
- Feature flag `agent_marketing_kill_switch` pausa todo inmediato
- Modo `quality_gate_enforcement_mode=shadow` revierte el gate a no-bloqueante

## Lo que sigue — próximas iteraciones (cuando Andrés decida)

1. **Integración profunda con `email_strategy_engine`** para que el plan semanal se ejecute sin aprobación humana (hoy requiere tu OK en el dashboard)
2. **Webhook Shopify orders** con atribución por cupón en tiempo real (hoy es vía `marketing_metrics` cada 6h)
3. **Webhook Klaviyo** de unsubscribe para cerrar el gap inverso (baja desde email → WA)
4. **Retry automático del bot** cuando reply_verification clasifica BOT_FAILED
5. **Agent Growth** — capa de ads (Meta + Google) con presupuesto capado, generación de creatives, kill del 20% inferior

## Checklist final deploy

- [x] Tablas creadas
- [x] Policies sembradas (34)
- [x] Módulos instalados con permisos correctos
- [x] Routers registrados en main.py
- [x] Hook en chatbot_engine con backup
- [x] Service restarted sin errores
- [x] Tests smoke pasados (6+5+5)
- [x] Cron quality cada 15 min
- [x] Cron reply verification cada 2h
- [x] Cron daily briefing 8:30 ART
- [x] Cron monitor cada hora
- [x] Kill switch off, enforce on
- [x] KB médico insertado
- [x] Dry-run briefing valida OK (~750 chars)

## Archivos relacionados

- v1 legacy: [[01-attribution-engine]], [[02-shopify-discount-api]], [[03-trigger-engine]], [[04-decision-layer]], [[05-daily-briefing]]
- Context: [[../../../.claude/projects/-Users-specialandres/memory/project_marketing_system|Memory: Marketing System]]
