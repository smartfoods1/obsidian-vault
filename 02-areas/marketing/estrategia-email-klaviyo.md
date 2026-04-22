---
date: '2026-04-22'
type: area
tags:
  - marketing
  - email
  - klaviyo
  - automatizacion
status: activo
---
# Estrategia Email Marketing — Klaviyo

## Objetivo
Motor de email inteligente integrado con SmartBrain. No solo campanas genericas — Claude lee segmentos de Klaviyo + ecommerce, comprende patrones y genera estrategias coherentes con WhatsApp (sin colisiones).

## Arquitectura Tier 1

### Base de Datos (4 tablas nuevas)
- `klaviyo_segment_mapping`
- `email_weekly_plan`
- `email_campaign`
- `email_campaign_metrics`

### Motor Semanal
- Claude cruza: segmentos ecommerce + journeys WA activos + stock + objetivos + performance historica
- Genera plan semanal con recomendaciones
- CEO aprueba antes de ejecucion

### Cron de Ejecucion
- Lunes 6:00 → genera plan
- Lunes 7:45 → notifica por WhatsApp
- Lunes 18:05 → ejecuta si fue aprobado

### UI de Aprobacion
- Cada CEO aprueba semanalmente antes de ejecucion
- Mockup ASCII diseñado

## Decision Pendiente
> Si no apruebs a tiempo, el Cerebro ejecuta por default (aprobacion implicita) o queda bloqueado?
> - Opcion A: Aprobacion implicita = 10x velocidad pero pierde control
> - Opcion B: Control manual = frena si viajas

## Copy Brain Boost (email flagship)
- **Angulo:** NGF (Nobel Rita Levi-Montalcini), estudio japones 2009 sobre hericenonas/erinacinas
- **Titulo:** "La molecula que tu cerebro deja de producir despues de los 30"
- **Estrategia:** Venta indirecta pura — educacion del problema → producto como conclusion obvia
- **Sin descuento en email 1.** Seguimiento 5-7 dias con email tactico + bundle 90 dias si convierte
- **Template:** HTML responsive, table-based, Klaviyo-compatible, colores Smart Foods (#282823, #E0E938, #4B6834)
