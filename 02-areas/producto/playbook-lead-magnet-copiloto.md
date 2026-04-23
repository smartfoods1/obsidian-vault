---
date: 2026-04-22
type: playbook
tags: [playbook, lead-magnet, marketing, copiloto, reutilizable]
status: activo
derivado_de: "[[01-projects/copiloto-lead-magnet-segundo-cerebro/index|Lead Magnet Segundo Cerebro]]"
---

# Playbook · Lead Magnet para Programa Copiloto

Receta reutilizable para lanzar un lead magnet (guía PDF gratuita + landing) para el Programa Copiloto. Derivada de la implementación real de [[01-projects/copiloto-lead-magnet-segundo-cerebro/index|Segundo Cerebro]] (abril 2026).

## Cuándo aplica
- Querés un asset gratuito que capture emails y caliente leads para el Programa Copiloto.
- Tenés un tema específico que demuestra el tipo de trabajo que se hace en el programa (ej: productividad con IA, automatización de un flow concreto, sistema de CRM con Claude Code, etc.).
- El tema debe ser de interés para el público objetivo (founders/operadores argentinos que ya usan IA a nivel chat).

## Cuándo NO aplica
- Si el tema no demuestra indirectamente el valor del programa — mejor no crearlo que diluir.
- Si el tema ya está cubierto en la base gratis del programa (sería redundante).

## Los 8 pasos

### 1 · Definir el asset
- **Formato**: PDF 12-15 páginas (suficiente para tener sustancia, no tanto como para abrumar).
- **Estructura estándar**: portada · problema · concepto · herramienta · método · setup paso a paso · ejemplos · tips · diagrama del sistema · prompt para Claude Cowork · CTA programa · contraportada.
- **Tono**: argentino ("vos"), concreto, con historia personal del CEO.
- **Ángulo obligatorio**: el PDF DEBE incluir un prompt para Claude Cowork que muestra el tipo de trabajo del programa. Esto hace que el lead magnet funcione como *preview*.

### 2 · Draft de contenido primero
- Escribir TODO el contenido (landing + PDF) en un markdown de draft antes de tocar código.
- Pasárselo al usuario para aprobar tono / ángulo / estructura.
- Una vez aprobado, implementación en 1 sola pasada.

### 3 · Landing
- Ubicación: `copiloto.specialandres.ar/[slug-del-tema]/`
- Stack: HTML plano (sin build) con el design system del programa (`var(--bg-0)`, `var(--gradient)`, Space Grotesk + Geist + Geist Mono).
- Secciones estándar: nav (con link de vuelta al programa) · hero con gradient text · problema (3 cards) · solución (4 steps) · ejemplo real (before/after) · qué incluye (grid 8 checks) · formulario · sobre Andrés · FAQ · footer.
- SVG custom inline para ilustraciones — no screenshots reales, no fotos stock.
- Link prominente en la nav de la landing principal como "Guía gratis ↗" en verde.

### 4 · PDF
- Generar desde HTML custom con Chrome headless.
- Source: `/Users/specialandres/copiloto-landing/pdf-build/guia.html`
- Design system del programa mantenido en el PDF (mismo dark theme, misma paleta).
- Cada página es un `<section class="page">` con altura 297mm (A4) y padding 22mm top / 30mm bottom (el bottom mayor es clave: evita que texto largo choque con el footer de página).
- Footer con número de página y brand en cada hoja.
- Comando:
```bash
cd /Users/specialandres/copiloto-landing/pdf-build && \
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=guia-[slug].pdf --no-sandbox \
  --virtual-time-budget=10000 "file://$PWD/guia.html"
```

### 5 · Backend
- **NO crear una tabla nueva**. Extender `copiloto_leads` con la columna `source` (ya existe la migración en `_ensure_table`).
- **Endpoint**: `POST /api/copiloto/lead-magnet` ya implementado — **solo hay que agregar el slug nuevo** al dict `LEAD_MAGNETS` del archivo `copiloto_leads.py`:
```python
LEAD_MAGNETS = {
    "segundo-cerebro": {...},
    "NUEVO-SLUG": {
        "title": "Título completo de la guía",
        "pdf_url": "/guia-NUEVO-SLUG.pdf",
    },
}
```
- Reiniciar `smartbrain-api` después de editar.

### 6 · Nginx
- Agregar en `/etc/nginx/sites-enabled/copiloto.specialandres.ar`:
  - Una regla `location = /guia-NUEVO-SLUG.pdf` con `root /var/www/copiloto`
  - Una regla `location /NUEVO-SLUG` para la landing (si no está cubierta por el `try_files` existente)
- `nginx -t && systemctl reload nginx`

### 7 · Deploy
Flow estándar:
```bash
# Backend (si cambió)
scp copiloto_leads.py root@76.13.228.77:/root/.openclaw/workspace/dashboard/backend/routers/
ssh root@76.13.228.77 "systemctl restart smartbrain-api"

# Landing
scp -r NUEVO-SLUG/ root@76.13.228.77:/var/www/copiloto/

# PDF
scp guia-NUEVO-SLUG.pdf root@76.13.228.77:/var/www/copiloto/

# Nginx (si cambió)
scp nginx.conf root@76.13.228.77:/etc/nginx/sites-enabled/copiloto.specialandres.ar
ssh root@76.13.228.77 "nginx -t && systemctl reload nginx"
```

### 8 · QA + Link
Test end-to-end:
```bash
curl -sI https://copiloto.specialandres.ar/NUEVO-SLUG/
curl -sI https://copiloto.specialandres.ar/guia-NUEVO-SLUG.pdf
curl -s -X POST https://copiloto.specialandres.ar/api/copiloto/lead-magnet \
  -H "Content-Type: application/json" \
  -d '{"nombre":"QA","email":"qa@test.com","source":"NUEVO-SLUG","website":""}'
```

Verificar:
- Form submit devuelve `{ok:true, pdf_url:"..."}`
- Llega WA a Andrés con el mensaje "📚 NUEVO LEAD — GUÍA"
- Lead aparece en el admin CRM con el source correcto
- Segundo submit del mismo email devuelve `{repeat: true}` (idempotencia)
- Honeypot acepta silente sin notificar (request con `website:"x"`)

Luego:
- Borrar el lead de QA: `DELETE FROM copiloto_leads WHERE email='qa@test.com' AND source='NUEVO-SLUG'`
- Linkear la nueva guía desde la nav de la landing principal.

## Checklist reducida

```
[ ] 1. Draft de contenido en markdown, aprobado por Andrés
[ ] 2. Landing HTML + SVG custom
[ ] 3. PDF HTML generado con Chrome headless (≤15 páginas)
[ ] 4. Slug agregado a LEAD_MAGNETS en copiloto_leads.py
[ ] 5. Nginx rules para landing + PDF
[ ] 6. Deploy (scp + restart api + reload nginx)
[ ] 7. QA: curl tests + WA ping + lead en CRM
[ ] 8. Borrar lead QA + linkear desde nav de copiloto.specialandres.ar
[ ] 9. Empujar tráfico: IG, email, WhatsApp
```

## Lecciones aprendidas (Segundo Cerebro)
- **Padding inferior del PDF = 30mm mínimo**. Menos que eso y contenido largo choca con el footer de página.
- **Los tips largos no caben**. Si una sección tiene lista de 10 items, cada uno debe ser **una línea**, no dos.
- **SVG inline > imágenes externas**. Cero dependencias, renderizado perfecto en PDF, cualquier color se adapta al design system.
- **Idempotencia por email+source es crítica**. Un usuario que refresca o clickea dos veces no debe generar 2 pings de WA.
- **El prompt de Claude Cowork es la conversión real**. Mostrar concretamente qué podrías hacer con el programa es más fuerte que cualquier copy de ventas.

## Métricas estándar a trackear
- Leads capturados / semana por source
- Conversión landing → submit (instrumentar con `/api/copiloto/track` si se quiere granular)
- Conversión lead magnet → lead pago del programa (join por email)
- Descargas del PDF en access log de nginx

## Proyectos aplicando este playbook
- [[01-projects/copiloto-lead-magnet-segundo-cerebro/index|Segundo Cerebro]] (abril 2026) — primer lead magnet, baseline.
