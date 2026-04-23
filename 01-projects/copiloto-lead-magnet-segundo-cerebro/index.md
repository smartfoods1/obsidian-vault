---
date: 2026-04-22
type: project
tags: [project, copiloto, lead-magnet, marketing, lanzado]
status: lanzado
deployed_at: 2026-04-22
---

# Copiloto · Lead Magnet "Tu Segundo Cerebro"

Lead magnet gratuito para el Programa Copiloto: landing + guía PDF de 15 páginas sobre cómo capturar ideas con Obsidian + Telegram + IA. Captura leads en el mismo CRM que el programa pago, con `source='segundo-cerebro'`.

## Objetivo
Generar leads del funnel superior para el Programa Copiloto sin fricción (gratis, sin pago). El contenido también vende indirectamente el programa — la guía termina con un CTA y el prompt para Claude Cowork muestra el tipo de trabajo que se hace en el programa.

## Estado
Lanzado en producción el 2026-04-22. Pendiente: empujar tráfico (orgánico IG, email a base existente, crosspost Programa Copiloto).

## Entregables shippeados

### Landing
- **URL pública**: https://copiloto.specialandres.ar/segundo-cerebro/
- **Archivo local**: `/Users/specialandres/copiloto-landing/segundo-cerebro/index.html`
- **Archivo en VPS**: `/var/www/copiloto/segundo-cerebro/index.html`
- HTML plano (sin build), mismo design system que la landing principal (dark theme, Space Grotesk/Geist, gradient violeta→rosa→naranja)
- Secciones: hero · problema · solución (4 pasos) · ejemplo real · Obsidian vs alternativas · qué incluye · formulario · sobre Andrés · FAQ
- SVG custom inline para ilustraciones (no screenshots)

### PDF
- **URL pública**: https://copiloto.specialandres.ar/guia-segundo-cerebro.pdf
- **Archivo local**: `/Users/specialandres/copiloto-landing/pdf-build/guia-segundo-cerebro.pdf`
- **Archivo en VPS**: `/var/www/copiloto/guia-segundo-cerebro.pdf`
- 15 páginas, 2.3 MB, A4
- Generado con Chrome headless desde `pdf-build/guia.html`
- Comando regenerar:
```bash
cd /Users/specialandres/copiloto-landing/pdf-build && \
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=guia-segundo-cerebro.pdf --no-sandbox \
  --virtual-time-budget=10000 "file://$PWD/guia.html"
```

### Backend
- **Endpoint nuevo**: `POST /api/copiloto/lead-magnet`
  - Acepta `{nombre, email, whatsapp?, source, website}` (website = honeypot)
  - WhatsApp opcional (a diferencia del endpoint paid `/lead`)
  - Idempotente por email+source (devuelve `{repeat: true}` en el 2º submit)
  - Rate limit 5/hora por IP
  - Notifica a Andrés por WhatsApp con mensaje "📚 NUEVO LEAD — GUÍA"
  - Responde `{ok, id, pdf_url}` en vez de redirigir a Mercado Pago
- **Archivo**: `/root/.openclaw/workspace/dashboard/backend/routers/copiloto_leads.py`
- **Migración DB**: columna `source TEXT DEFAULT 'landing'` agregada a `copiloto_leads` (auto en `_ensure_table`). Index `idx_copiloto_source`.
- **Status nuevo**: `lead_magnet` agregado a `LEAD_STAGES`
- **Registry**: `LEAD_MAGNETS = {"segundo-cerebro": {title, pdf_url}}` — agregar entry acá para cada nueva guía futura

### CRM (admin existente)
- Accesible en `http://76.13.228.77/copiloto/` con X-Admin-Token
- Los leads del magnet aparecen con `source='segundo-cerebro'` y `status='lead_magnet'` — filtrables del resto del pipeline pago

### Nginx
- `/etc/nginx/sites-enabled/copiloto.specialandres.ar`
- 3 rutas nuevas: `POST /api/copiloto/lead-magnet` (proxy), `GET /guia-segundo-cerebro.pdf` (static), `GET /segundo-cerebro/` (static HTML)

### Link desde landing principal
- Agregado en nav de `copiloto.specialandres.ar/` como "Guía gratis ↗" en color verde

## Playbook reutilizable
Para armar el próximo lead magnet (cualquier tema, mismo funnel): ver [[Playbook - Lead Magnet Programa Copiloto]].

## Métricas a trackear
- [ ] Leads capturados / semana (query: `SELECT COUNT(*) FROM copiloto_leads WHERE source='segundo-cerebro'`)
- [ ] Conversión landing → submit
- [ ] Conversión lead magnet → lead pago del programa (join por email)
- [ ] Descargas del PDF (access log de nginx)

## Próximos pasos
- [ ] Empujar tráfico: post en IG @specialandres anunciando la guía
- [ ] Email a lista del Programa Copiloto con el link
- [ ] Segmento "downloaded segundo-cerebro" en Klaviyo para nurture de 7 días
- [ ] A/B test: cambiar headline del hero (tu cerebro olvida vs otro ángulo)
- [ ] Próximo lead magnet: aplicar el [[Playbook - Lead Magnet Programa Copiloto]]

## Decisiones de diseño tomadas
- **Endpoint nuevo en vez de extender `/lead`**: el endpoint paid forza redirect a Mercado Pago y exige WhatsApp. Dos flows distintos merecen dos endpoints.
- **Misma tabla `copiloto_leads` con columna `source`**: evita duplicar schema y hace que el admin CRM ya existente muestre todo junto. Filtro por source separa embudos.
- **WhatsApp opcional**: fricción mata conversión. Solo email es suficiente para entregar la guía.
- **SVG custom, no screenshots reales**: control total del estilo, cero dependencia externa, se renderiza perfecto en PDF.
- **PDF estático en nginx**: el link es público pero el botón solo aparece post-submit. Bueno enough para lead magnet gratis — no necesita firma/gate server-side.
