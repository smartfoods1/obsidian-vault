---
date: '2026-04-22'
type: project
tags:
  - project
  - healthos
  - plataforma
  - bienestar
  - ia
status: activo
---
# HealthOS — Plataforma de Bienestar Integral

## Objetivo
Plataforma de bienestar integrada con SmartBrain, con IA generativa como core. Puerta de entrada a adaptogenos Smart Foods.

URL: salud.smartfoods.ar (DNS pendiente de configurar)

## Arquitectura

### Stack
- Frontend: React 19 + Vite + Tailwind + Chart.js
- Backend: FastAPI + SQLite WAL
- IA: Claude Anthropic (genera planes personalizados)
- Auth: Magic link (sin contrasenia)
- VPS: srv1319033.hstgr.cloud

### 6 Dimensiones de Salud
1. Suenio
2. Movimiento
3. Nutricion
4. Estres
5. Digestion
6. Sexualidad

## Secciones Completadas

| Seccion | Status | Funcionalidad |
|---------|--------|---------------|
| Home | Completa | Protocolo integral, 6 dimensiones |
| Mis Retos | Completa | Conversacion guiada (4 preguntas/dimension) → plan 30 dias con 4 habitos |
| Mi Progreso | Completa | Wellness Score, adherencia, racha diaria, historial |
| Mis Adaptogenos | Completa | Protocolo + adaptogenos de retos, dosis personalizada, link Shopify |
| Mi Perfil | Completa | Edicion datos, toggle recordatorio diario WA con selector hora |
| Profesionales | Completa | Directorio con filtros, reservas, notificacion WA |
| Contenido | Completa | Biblioteca por dimension, badges pendientes |

## Motor de IA
- Claude genera planes de 30 dias personalizados basados en conversacion guiada
- 4 preguntas contextuales por dimension
- Adaptogeno incluido SOLO si aplica genuinamente (no marketing forzado)
- Mensaje motivacional personalizado

## Sprints Completados
5A (auth + home), 5B (motor IA + mis retos), 5C (progreso + graficos), 5D/E (perfil + adaptogenos), 5F (profesionales + contenido)

## Canal de Revenue Directo
"Mis Adaptogenos" muestra el protocolo del onboarding con prioridad 1/2/3 y los adaptogenos de retos activos. Cada card tiene boton "Comprar en Smart Foods" con link directo a Shopify (PRODUCTS_CATALOG). Si no hay URL, no muestra boton. Deduplicacion automatica si el mismo producto aparece en protocolo y reto.

## Bloqueantes Actuales
1. **DNS:** Falta record A en Hostinger: Tipo A, Nombre: salud, Valor: 76.13.228.77, TTL: 3600. Luego: `certbot --nginx -d salud.smartfoods.ar`
2. **Sprint 6A pendiente:** Cron de recordatorio diario por WhatsApp (el toggle en Mi Perfil existe pero el ejecutor que realmente envia los mensajes NO existe todavia — critico para retencion)
3. **DB pendiente Sprint 6A:** 3 columnas nuevas ya en `health_users`: whatsapp_daily_reminder, reminder_time, updated_at

## Decision Pendiente
> Antes de seguir construyendo features, activar DNS y llevar 10 beta users reales. Cada sprint sin usuarios reales = features en el vacio. Esto se marco 5 veces en sesiones. El cuello de botella no es tecnico — son 3 pasos en Hostinger.
