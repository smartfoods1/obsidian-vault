---
date: '2026-04-22'
type: area
tags:
  - b2b
  - cliente
  - byba-yoga
  - smartcopilot
  - piloto
status: prospecto
---
# Cliente B2B: Byba Yoga (Piloto SmartCopilot)

## Datos
- **Negocio:** Hot yoga studio
- **Instagram:** @bybayogabuenosaires
- **Rol:** Primer case study para SmartCopilot

## Por que importa
No es solo un cliente piloto. Es el laboratorio donde se valida si pilares de contenido + cron automatico + templates funcionan en mundo real.

## MVP Requerido
- [ ] Cargar 26 posturas en KB
- [ ] Cargar 5+ testimonios reales
- [ ] Cargar precios actualizados
- [ ] Cargar bios de profesores
- [ ] Cargar horarios

## Pilares de Contenido (configurados)
- 40% Educativo (tips de posturas, beneficios del calor)
- 25% Motivacional/Inspiracional (frases, transformaciones)
- 20% Comunidad (behind-the-scenes, profesores)
- 10% Promocional (horarios, packs)
- 5% Estacional

## Automatizacion Target
- Cron semanal domingo 11am → genera semana completa
- Notificacion WhatsApp al owner con contenido para revisar
- Templates recurrentes: lunes horarios, miercoles testimonio, viernes motivacion
- Hashtag bank rotatorio (global + local + nicho)

## Arquitectura Tecnica SmartCopilot Tier 1
Prompt completo generado para implementar 5 prioridades en VPS. Incluye:

### Schema (5 tablas nuevas)
- `content_pillars`: pilares con porcentaje asignado por cliente
- `testimonials`: banco de testimonios reales con tracking de uso (para rotar)
- `reference_photos`: fotos del estudio como referencia visual para Gemini
- `content_templates`: templates recurrentes (lunes horarios, miercoles testimonio, etc.)
- `hashtag_bank`: hashtags segmentados global/local/nicho con rotacion automatica

### Funcion Clave
`get_enriched_context()` — enriquece cada generacion con el testimonio menos usado, fotos de referencia y hashtags rotatorios.

### Datos Iniciales Cargados
- 21 hashtags segmentados (globales: #bikramyoga #hotyoga, locales: #yogabuenosaires, nicho: #26posturas)
- 3 templates recurrentes pre-configurados
- Pilares ya calibrados al mix correcto para hot yoga

### Bug Conocido
Generacion semanal inteligente genera copy pero NO imagenes. Causa probable: funcion de imagen no se llama en el cron, error silencioso (try/except sin log), o funcion async sin await. Prompt de diagnostico generado.

## Decision Estrategica
> No buildear FAQ/soporte in-app todavia. Usar el bot de WhatsApp de SmartCopilot como canal de soporte (el cliente aprende como funciona el bot usandolo). Buildear en su lugar un onboarding de 3 pasos para primer login.

## Metricas de Exito
- [ ] Duenio revisa/aprueba contenido en menos de 5 min
- [ ] Engagement rate vs contenido manual anterior
- [ ] Tasa de publicacion semanal (target: 5 posts/semana)
