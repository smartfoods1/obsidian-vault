---
date: '2026-04-22'
type: area
tags:
  - operaciones
  - smartbrain
  - arquitectura
  - vps
status: activo
---
# SmartBrain — Arquitectura y Estado Actual

## Metricas del Sistema
- **9 servicios** corriendo
- **566 endpoints**
- **130 tablas** en SQLite
- **75 componentes React**
- **30+ automatizaciones**
- **19 integraciones**

## Valoracion
- **Equivalente SaaS:** USD $2,119/mes
- **Costo de replicacion:** USD $150K-$250K
- **Multi-tenant:** Ya funcional con 3 marcas en UN VPS

## Modelo Comercial Definido
- **Setup fee:** USD $4,500
- **Sesion soporte on-demand:** USD $300/sesion
- **Modelo:** Multi-tenant en nuestra infraestructura (no instalar en VPS del cliente — ineficiente)

## Arquitectura Base
```
Internet → nginx (443/SSL) → journey_proxy (Flask :18791)
                            → smartbrain-api (FastAPI :8080)
```

## Productos Derivados

### SmartWap (Chatbot Multi-tenant)
- 5 sprints completados (auth, AI engine, campanas, KB v2, templates WA)
- Producto listo para onboardear clientes
- Primer cliente potencial: Byba Yoga

### SmartCopilot (Contenido + WhatsApp)
- Unifica SmartWap + generacion de contenido
- Stack: FastAPI + React + Gemini 2.5 Flash
- 5 pilares de contenido configurables por cliente

## Fragilidades Conocidas (Sprint Robustez pendiente)
- Single process bloqueante
- SQLite bajo concurrencia (WAL mitiga pero no resuelve escala)
- asyncio sin error handling robusto
- BackgroundTasks fragil
- Sin monitoreo
- Gemini sin retry logic

## Decision Clave
> Sprint de Robustez (monitoring + retry + error handling + logs estructurados) ANTES de escalar clientes. Un cliente en produccion con crash = perdida de credibilidad irreparable.
