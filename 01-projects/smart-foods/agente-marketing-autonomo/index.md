---
date: 2026-04-24
type: project
tags: [smart-foods, marketing, agente-autonomo, smartbrain]
status: in-progress
version: v2
supersedes: [01-attribution-engine, 02-shopify-discount-api, 03-trigger-engine, 04-decision-layer, 05-daily-briefing]
---

# Agente Marketing Autónomo — Smart Foods (v2)

> **v1 asumió greenfield. v2 reconoce el sistema existente (sesión 16-17 abril) y solo construye los gaps.** Los docs 01-05 de v1 quedan como draft histórico; este doc es la fuente de verdad.

## Filosofía del proyecto

**Andrés quiere un agente trabajando para él, no al revés.**

Eso significa:

- El agente **decide**, no pregunta.
- El agente **prueba** antes de escalar.
- El agente **valida calidad** de cada mensaje antes de enviar.
- El agente **mantiene integridad** (no dobles, exclusiones, budget caps).
- El agente **responde replies** vía SmartBot existente y **verifica éxito** de la conversación.
- El agente **informa**, no pide permiso.
- El agente **escala** solo lo mínimo indispensable.

**Producción directa** — sin shadow mode. Envelope full desde día 1. Kill switch por WA siempre activo.

## El envelope (qué puede hacer sin Andrés)

Este envelope vive en la tabla `agent_policy` (editable sin redeploy). Arranque: valores de la columna "default".

| Categoría | Autónomo | Push WA informa | Escalación (pide input) |
|---|---|---|---|
| **Lanzar campañas** | Segmentos existentes, descuento ≤15%, 1-3 campañas/día | Al lanzar cada una | Segmentos nuevos · descuento >15% · lanzamiento producto · palabras reguladas detectadas |
| **Responder replies** | Baja · precio · info producto · objeción estándar · pedido de envío · horarios · stock | Conversión >$100k · respuesta rechazada por cliente 2× | Queja regulatoria · amenaza legal · mención prensa · pedido explícito "hablar con Andrés" |
| **Pausar / reactivar** | Por umbral · por fatigue · por stockout · por ROAS <2× a 72h | Cada pausa con motivo | — |
| **Cupones Shopify** | Crear/desactivar ≤15% · scope producto/categoría | Crear cupón nuevo | Cupones >15% · scope "all" con >20% off |
| **Gasto** | Hasta $500k ARS/mes en descuentos · hasta 5000 WA sends/mes | Al cruzar 70% y 90% del cap | Pedir cap extra |
| **Técnico** | Retry 3× con exponential backoff · reintentar envíos fallidos · rotar template si uno falla | Error recuperado solo | Shopify/Klaviyo down >2h · WA template rechazado · DB corruption |
| **Crisis auto** | Detectar + pausar todo | — | Tasa baja >5% en 24h · ventas -30% vs baseline · review negativo viral |
| **Kill switch** | — | — | "STOP" desde WA de Andrés → pausa todo excepto contenido IG aprobado |

## Arquitectura — el agente sobre el sistema existente

```
                      [YA EXISTE]                     [GAP A CONSTRUIR]
                            │                                │
  ┌─────────────────────────┼─────────────┐          ┌──────┴──────────┐
  │                         │             │          │                 │
[Triggers]           [Generation]    [Execution]  [Policy Engine]  [Orchestrator]
lifecycle crons     email_strategy    coupon_guard   agent_policy   agent_runner
abandoned_cart       engine         wa_play_executor   table        (cron 1h)
anti_churn_b2c     personalization  cascade_executor
                                    marketing_metrics
                            │                                │
                            └────────────┬───────────────────┘
                                         │
                                    [Quality Gates]       ← construir
                                    pre-send validator
                                         │
                                    [Send / SmartBot]     ← existe
                                         │
                                    [Reply Verification] ← construir
                                    bot conversation audit
                                         │
                                    [Daily Briefing]     ← reformar
                                    cron_daily_summary.py
                                         │
                                  WhatsApp a Andrés (+5491165973204)
```

## Gap analysis — qué ya existe vs qué construir

### Ya existe (no tocar, solo integrar)

| Componente | Archivo | Qué hace |
|---|---|---|
| Attribution | `campaign_attributions` + `marketing_metrics.py` | Email+phone+discount matching, ROAS real. Cron 6h. |
| Cupón Shopify | `coupon_guard.py` (`ensure_campaign_coupon`, `ensure_all_plan_coupons`) | Auto-crea cupones pre-envío. Idempotente. |
| Planificación | `email_strategy_engine.py` (1030 líneas) | Plan semanal Claude + URL catalog + quiz + segmentos |
| Channel routing | `channel_router.py` | 14 reglas phase×objective, budget tracking |
| Cascadas WA | `cascade_executor.py` | Post-email cascadas hourly |
| WA plays | `wa_play_executor.py` | Templates Meta aprobados, idempotente, CEO exclusion |
| Personalización | `personalization_engine.py` | 3 niveles quiz (471 perfiles) |
| Daily briefing | `cron_daily_summary.py` | Existe pero con formato "resumen", no "agente informa" |
| SmartBot replies | `/packages/smartbot/backend/routers/chatbot.py` | Responde WA entrantes |
| Unsubscribe WA | Tabla `wa_unsubscribed` | Marca teléfonos opt-out |

### Faltan (lo que hay que construir)

| # | Componente | Por qué | Esfuerzo |
|---|---|---|---|
| 1 | **`agent_policy` table + admin endpoint** | Envelope vive en código editable sin redeploy. El agente consulta antes de cualquier decisión. | 0.5 día |
| 2 | **`agent_orchestrator.py` cron** | El decisor. Cada 1h: lee triggers existentes, evalúa contra policy, ejecuta lo que puede, escala lo que no. | 2 días |
| 3 | **`quality_gates.py`** | Valida cada copy pre-envío: regulatorio · URLs vivas · producto correcto (polvo no cápsula) · cupón ↔ texto · tono de marca vs brand_context | 1.5 días |
| 4 | **`reply_verification.py` cron** | Audita conversaciones del SmartBot: clasifica resultado, detecta colgadas, auto-fix bajas no procesadas, flag "pide humano" | 2 días |
| 5 | **`cron_daily_summary.py` rewrite** | Reformato de "resumen CEO" a "agente informa". Incluye acciones ex-post, bloqueos, decisiones tomadas, pedidos de input al final. | 1 día |
| 6 | **Unsubscribe unificado** | Hoy solo `wa_unsubscribed`. Falta: handler que detecte "baja/stop/no quiero más" en replies, marque en Klaviyo + WA + DB. Y respete el opt-out en TODOS los envíos. | 1 día |
| 7 | **Circuit breaker + kill switch** | "STOP" por WA de Andrés → flag DB → orchestrator chequea antes de cada acción. Tasa baja >5%/24h → pausa todo automático. | 0.5 día |
| 8 | **Escalation WA channel** | Cuando el agente necesita escalar, formato estructurado + ID de escalation para que Andrés pueda responder. | 0.5 día |

**Total: ~9 días de desarrollo** (vs 10 días que había proyectado en v1 cuando asumía greenfield). La diferencia es que estos 9 días son **solo gap**, no reconstrucción.

## Reply verification — el algoritmo novedoso

Este es el pedazo que no existe y es clave para que el agente "verifique éxito de la conversación" como pediste.

**Cron `reply_verification.py` cada 2h:**

```python
# 1. Detectar conversaciones iniciadas por campaña
# Query: mensajes entrantes WA/email en las últimas 48h donde el contexto
# previo fue una campaña del agente
recent_replies = db.query("""
    SELECT conversation_id, campaign_id, customer_phone, thread_messages
    FROM conversations
    WHERE triggered_by_campaign_id IS NOT NULL
      AND last_message_at > datetime('now', '-48 hours')
      AND NOT verified
""")

# 2. Para cada thread, Gemini clasifica el resultado
for thread in recent_replies:
    classification = gemini.classify(
        prompt=f"""
        Conversación entre cliente de Smart Foods y nuestro bot. La campaña fue: {thread.campaign_subject}
        
        Transcript:
        {thread.messages}
        
        Clasificá el resultado en uno de:
        - RESOLVED_UNSUBSCRIBE (cliente pidió baja y fue procesada correctamente)
        - RESOLVED_INFO (cliente pidió info, bot respondió, cliente conforme o no responde)
        - RESOLVED_CONVERSION (cliente compró)
        - PENDING_OK (cliente aún está conversando, bot respondiendo bien)
        - BOT_FAILED (cliente frustrado, pide lo mismo 2+ veces, insulta, o bot respondió algo irrelevante)
        - HUMAN_REQUEST (cliente pide hablar con humano explícitamente)
        - REGULATORY_RISK (cliente menciona salud/enfermedad/legal/ANMAT/medio de prensa)
        - UNSUBSCRIBE_NOT_PROCESSED (cliente pidió baja pero bot no la procesó)
        
        También devolvé: satisfaction_score (0-10) y recommended_action (NONE / ESCALATE / RETRY_BOT / MANUAL_UNSUBSCRIBE)
        """,
        response_format="json"
    )
    
    # 3. Acción automática según clasificación
    if classification.result == "UNSUBSCRIBE_NOT_PROCESSED":
        process_unsubscribe(thread.customer_phone)
        alert_andres(f"Auto-fix: baja no procesada para {thread.customer_phone}")
    
    elif classification.result == "BOT_FAILED":
        if thread.retry_count < 2:
            retry_bot_response(thread, alternative_tone="more_empathetic")
        else:
            escalate_to_andres(thread, reason="bot_failed_2x")
    
    elif classification.result == "HUMAN_REQUEST":
        mark_inbox_priority(thread, tag="pedido_humano")
        notify_andres(thread, reason="cliente_pide_humano")
    
    elif classification.result == "REGULATORY_RISK":
        pause_related_campaigns()
        escalate_to_andres(thread, reason="riesgo_regulatorio", urgency="HIGH")
    
    # 4. Marcar como verificada
    mark_verified(thread.conversation_id, classification)
```

**Resultado**: cada conversación que el bot tuvo es auditada. Las que fallaron se arreglan solas (baja auto-procesada, retry con otro tono) o escalan. Al día siguiente, el briefing incluye: "Bot tuvo 34 conversaciones. 31 resueltas (10 bajas · 18 info · 3 conversiones). 2 escaladas a inbox (pedidos humano). 1 auto-fix de baja no procesada."

## Daily briefing — formato "agente informa"

Cambia tono y estructura. Cron 8:30 ART a `+5491165973204`.

```
Agente Marketing — 24 abr

Ayer ejecuté:
• Lancé 2 campañas email (REACT45-Brain, STOCK-Immune)
• Lancé 1 campaña WA B2B (reorden mayo, 42 leads)
• Pausé STOCK-Immune a las 17h por CTR 1.2% < umbral
• Maneja 34 replies: 10 bajas procesadas, 18 consultas respondidas, 3 conversiones, 2 escaladas a inbox
• Auto-fix: 1 baja no procesada por bot, corregida

Resultados ayer:
Revenue atribuido: $1.64M · Cupones: $38k · Margen neto: $720k
Conversaciones exitosas del bot: 31/34 (91%)

Mes a la fecha:
Rev: $18.4M · ROAS email 6.1× · WA 11.4× · Descuentos: $380k/$500k cap (76%)

Pedidos de input (respondé SI/NO con el número):
1. REACT90-GLOW20 a 845 personas (descuento 20% excede envelope).
   Rev esperado $380k. ¿Autorizo?
2. Reply de @cliente_X pide hablar con vos (thread en Inbox).
   ¿Respondo yo o te lo dejo?

Bloqueos:
• Ninguno.

Próximas 24h:
Sigo con plan semanal. Próximo trigger importante: reactivación 60d
(1.120 personas) el sábado.
```

## Roadmap de implementación — 9 días

Producción incremental. Cada día deja algo utilizable; no hay "big bang".

| Día | Milestone | Deploy a prod? |
|---|---|---|
| 1 | Tabla `agent_policy` + endpoint admin + kill switch flag | Sí (solo lee, no afecta nada aún) |
| 2-3 | `quality_gates.py` integrado en `email_strategy_engine` + `wa_play_executor` | Sí, valida pero no bloquea aún (shadow log) |
| 3 | Quality gates pasan a bloqueantes. Unsubscribe unificado. | Sí |
| 4-5 | `agent_orchestrator.py` — corre cada 1h leyendo triggers existentes | Sí, modo autónomo real |
| 6-7 | `reply_verification.py` — audita conversaciones SmartBot | Sí |
| 8 | `cron_daily_summary.py` rewrite + formato WA nuevo | Sí — primer briefing tuyo nuevo llega día 9 |
| 9 | Circuit breaker + escalation paths formalizados | Sí, sistema completo |
| 10+ | Ajuste de envelope según decisiones tomadas | Iteración semanal |

## Métricas de éxito

Día 30 post-lanzamiento:

- **Tu tiempo en marketing cae de ~3h/semana a <30min/semana** (principal KPI)
- 0 campañas enviadas con copy regulatoriamente riesgoso
- 0 dobles envíos
- >90% de replies resueltas por bot sin tu intervención
- ROAS blended mantiene o supera 5× (baseline actual 7.4×)
- <5 escalaciones/semana en el WA de briefing
- 100% de bajas procesadas correctamente (auto-verificado)

## Links

- [[01-attribution-engine|v1 legacy — attribution (ya existe en el sistema)]]
- [[02-shopify-discount-api|v1 legacy — shopify discount (ya existe: coupon_guard)]]
- [[03-trigger-engine|v1 legacy — triggers (ya existen: lifecycle crons)]]
- [[04-decision-layer|v1 legacy — decision (reemplazado por envelope + orchestrator)]]
- [[05-daily-briefing|v1 legacy — briefing (reemplazado por formato nuevo arriba)]]
- Sistema existente: [[../../../.claude/projects/-Users-specialandres/memory/project_marketing_system|Memory: Marketing System abril 17]]
