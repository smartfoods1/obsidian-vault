---
date: 2026-06-30
type: playbook
tags: [smartbrain, agentes, automatizacion, ia]
status: draft
---

# Agentes Autónomos para SmartBrain

## 1. Agente de Respuesta WhatsApp (ALTA PRIORIDAD)

- Recibe mensaje → clasifica intención (consulta, pedido, queja, spam)
- Busca en DB del tenant (productos, precios, stock)
- Genera respuesta con Gemini
- Si es pedido → crea orden en Shopify
- Si es queja → escala a humano con contexto
- **Impacto**: Reduce 80% del tiempo de atención al cliente

## 2. Agente de Contenido Autónomo (ALTA PRIORIDAD)

- Analiza qué funcionó mejor en los últimos 7 días
- Genera 3 variantes de post con Gemini
- Selecciona la mejor con scoring propio
- Publica automáticamente a Instagram
- **Impacto**: 15-20 posts/mes sin intervención

## 3. Agente de Pricing Intelligence (MEDIA PRIORIDAD)

- Scrapea MercadoLibre cada 6h
- Compara con precios propios en Shopify
- Alerta si competidor baja precio >10%
- Sugiere ajuste si hay oportunidad
- **Impacto**: Margen protegido

## 4. Agente de Lead Scoring B2B (MEDIA PRIORIDAD)

- Monitorea Google Places
- Scoring automático por ubicación, reviews, rubro
- Genera mensaje personalizado con Gemini
- Envía WhatsApp de primera prospección
- Follow-up automático si no responden
- **Impacto**: Pipeline B2B 24/7

## 5. Agente de Alertas Inteligentes (MEDIA PRIORIDAD)

- Monitorea ventas, stock, engagement, tráfico
- Detecta anomalías y actúa proactivamente
- Centraliza alertas de todos los módulos
- **Impacto**: Problemas detectados en minutos

## 6. Agente de Recovery Post-Venta (BAJA PRIORIDAD)

- Detecta carrito abandonado en Shopify
- Envía WhatsApp recordatorio (1h) + descuento (24h)
- Post-compra: día 3 experiencia, día 14 recompra
- **Impacto**: +15-20% recuperación de carritos

## Arquitectura

Cada agente como servicio independiente en el VPS:

```
/root/.openclaw/workspace/agents/
├── wa_responder/
├── content_autonomous/
├── pricing_intel/
├── lead_scorer/
├── smart_alerts/
└── recovery_agent/
```

- Corre como systemd service
- Loop propio (cada N minutos/horas)
- Accede a DB via `_resolve_db_path()`
- Usa Gemini para decisiones
- Kill switch manual

## Recomendación

Arrancar por el **Agente de Respuesta WhatsApp** — mayor impacto, menor riesgo.
