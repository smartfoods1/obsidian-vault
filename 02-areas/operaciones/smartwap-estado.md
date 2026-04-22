---
date: '2026-04-22'
type: area
tags:
  - operaciones
  - smartwap
  - chatbot
  - multi-tenant
status: activo
---
# SmartWap — Estado del Producto

## Que es
Plataforma de chatbot multi-tenant con IA para WhatsApp Business. Producto SaaS independiente que reutiliza infra de SmartBrain.

## Sprints Completados

| Sprint | Estado | Construido |
|--------|--------|-----------|
| 1 | Completo | Auth multi-tenant, DB, webhook, frontend base |
| 2 | Completo | AI Engine (Gemini 2.5 Flash), Inbox, Contactos, KB |
| 3 | Completo | Campanas masivas, Admin Panel, Analytics |
| 4 | Completo | KB v2 (upload/URL/Brand Document), Flows, Admin AI control |
| 5 | Completo | WhatsApp Templates, Campaigns v2, UI Polish |

## Primer Cliente: Byba Yoga
- Hot yoga studio, @bybayogabuenosaires
- MVP: Cargar 26 posturas, horarios, testimonios, precios en KB
- Testear calidad de generaciones antes de automatizar

### 5 Pilares de Contenido (configurables por cliente)
- 40% Educativo (tips de posturas, beneficios del calor)
- 25% Motivacional/Inspiracional
- 20% Comunidad (behind-the-scenes, profesores)
- 10% Promocional (horarios, packs)
- 5% Estacional

### Automatizacion Target
- Cron semanal domingo 11am → genera semana completa → WhatsApp al owner
- Templates recurrentes (lunes horarios, miercoles testimonio, viernes motivacion)
- Hashtag bank por industria (rotatorio)

## Bloqueantes para Primer Cliente
- Configuracion Meta Business API
- KB inicial cargada con data real del cliente
- Bug resuelto: redirect post-login a /smartwap/ (no a SmartBrain)

## Importancia Estrategica
> Byba Yoga no es solo un cliente piloto. Es el laboratorio donde se valida si pilares + cron + templates funcionan en mundo real. Los datos de feedback alimentan V2.
