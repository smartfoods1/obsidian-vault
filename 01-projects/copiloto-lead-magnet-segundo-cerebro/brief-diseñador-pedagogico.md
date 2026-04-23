---
date: 2026-04-22
type: brief
tags: [brief, pedagogia, curricula, copiloto, integracion]
status: pendiente-envio
para: "diseñador pedagógico Programa Copiloto"
---

# Brief para el diseñador pedagógico — Caso de estudio "Lead Magnet Segundo Cerebro"

Lo que sigue es contexto completo y autocontenido para integrar este proyecto real como **caso de estudio / ejercicio / demo** en la currícula del Programa Copiloto. El proyecto fue construido en una sesión de trabajo entre Andrés (fundador) y Claude Cowork el 22 de abril de 2026. Quedó shippeado a producción ese mismo día.

---

## 1 · Qué se construyó

Un **lead magnet completo** para el Programa Copiloto: una guía PDF gratuita sobre cómo armar un "segundo cerebro" con Obsidian + Telegram + IA, con landing page, captura de leads en el CRM existente del programa, entrega automática del PDF y notificación por WhatsApp al founder.

### URLs vivas
- **Landing**: https://copiloto.specialandres.ar/segundo-cerebro/
- **PDF (15 páginas, 2.3 MB)**: https://copiloto.specialandres.ar/guia-segundo-cerebro.pdf
- **Programa Copiloto (contexto)**: https://copiloto.specialandres.ar/

### Partes que se construyeron
1. **Landing HTML estática** con mismo design system del programa (dark theme, gradient violeta→rosa→naranja, Space Grotesk + Geist). Hero, problema, solución en 4 pasos, ejemplo real, comparativa Obsidian vs alternativas, formulario, bio, FAQ. SVG custom inline para ilustraciones (cero imágenes externas).
2. **PDF de 15 páginas** generado desde HTML con Chrome headless. Mismo design system. Contenido: problema → concepto del segundo cerebro → método PARA → setup de Obsidian → setup del bot de Telegram → clasificación con IA → sincronización → 10 tips → diagrama completo → **prompt para Claude Cowork** → CTA al programa.
3. **Backend nuevo endpoint** `POST /api/copiloto/lead-magnet` en FastAPI, agregado al mismo servicio que ya maneja los leads de pago del programa. Guarda en la misma tabla `copiloto_leads` con columna nueva `source`. WhatsApp opcional, idempotente por email, honeypot anti-bot, rate limit 5/h por IP.
4. **CRM reutilizado**: los leads del magnet aparecen en el admin CRM existente con `source='segundo-cerebro'`, filtrables del pipeline pago.
5. **Nginx** con rutas nuevas para la landing, el PDF y el endpoint.
6. **Link desde la landing principal** del programa hacia la guía ("Guía gratis ↗" en verde, en la nav).

---

## 2 · Por qué es un caso pedagógico potente

**Es lo que el programa enseña, hecho en 3 horas con Claude Cowork.** El alumno va a llegar a este punto y va a poder decir: "lo mismo que hizo Andrés, lo puedo hacer yo con mi negocio". Cubre:

- **Flujo end-to-end real**: no es un ejemplo de juguete. Está en producción, capturando leads reales.
- **Decisiones de arquitectura no triviales**: por qué extender vs crear nuevo, por qué una columna nueva y no tabla nueva, por qué reusar el CRM existente.
- **Múltiples artefactos coherentes**: landing + PDF + backend + CRM + nginx, todos alineados.
- **Marketing + técnico juntos**: no es solo código — es estrategia de lead magnet + diseño + copy + backend + deploy.
- **El prompt dentro del PDF es meta-demostrativo**: el PDF mismo contiene el prompt que armaría ese sistema. El estudiante ve la receta completa.

---

## 3 · Skills y conceptos demostrados

| Skill / Concepto | Dónde aparece | Profundidad |
|---|---|---|
| Briefing efectivo a Claude Cowork | Fase de planning inicial: "mostrame el contenido antes para aprobarlo" | Alta |
| Matching de design system existente | Landing y PDF replican la paleta + tipografía de la landing madre | Media |
| Trade-offs de extensión vs creación | Decisión: nuevo endpoint + columna `source` en tabla existente | Alta |
| Idempotencia en endpoints públicos | Segundo submit del mismo email devuelve `{repeat: true}` en vez de duplicar | Alta |
| Hardening básico (honeypot, rate limit, validación) | Campo `website` oculto, 5 requests/h por IP, validación de email | Media |
| Generación de PDF desde HTML (Chrome headless) | Comando directo con Google Chrome, sin dependencias | Alta |
| Reutilización de infra del programa (CRM, nginx, servicio API) | Todo suma al mismo admin CRM ya usado para leads pagos | Alta |
| Deploy SSH + scp a VPS | Reglas de VPS cortas + reload nginx + restart systemd | Media |
| Estructura PARA para notas | Método Tiago Forte enseñado en la guía y usado en el vault | Baja |
| Funnel de lead magnet | Estrategia de marketing B2C/B2B demostrada en vivo | Media |
| Copy argentino y tono de programa | Todo el texto usa "vos" y el tono del Programa Copiloto | Baja |

---

## 4 · Propuestas de integración en la currícula

Opciones que se me ocurren. El diseñador pedagógico elige cuáles activar.

### A · Como caso de estudio único (semana temprana)
- **Momento**: semana 1 o 2 del programa.
- **Duración**: 1 clase de 60-90 min.
- **Formato**: Andrés muestra en vivo el proyecto ya terminado. Lee el PDF. Abre la landing. Muestra el lead capturado en el CRM. Abre el código del endpoint en el VPS y lo explica.
- **Objetivo pedagógico**: "esto es lo que vas a poder hacer al terminar el programa". Anclar expectativa y hambre.

### B · Como demo del prompt para Claude Cowork
- **Momento**: cuando se enseña briefing de tareas a Cowork.
- **Duración**: 30 min dentro de una clase de briefing.
- **Formato**: mostrar el prompt de la página 13 del PDF. Desarmarlo. Explicar por qué cada sección está donde está (stack, flujo, "dejá secrets en .env", "hacé incremental", etc.).
- **Objetivo pedagógico**: mostrar cómo escribir un prompt que le permita a Cowork shippear sin pedir 20 aclaraciones.

### C · Como ejercicio replicable por el alumno
- **Momento**: módulo de marketing / lead generation.
- **Duración**: proyecto de 1 semana.
- **Formato**: cada alumno arma SU propio lead magnet para SU negocio. Receta documentada en el [[playbook-lead-magnet-copiloto|Playbook: Lead Magnet para Programa Copiloto]].
- **Entregables del alumno**:
  - Una guía PDF gratuita (12-15 pág.) sobre un tema relevante a su público
  - Una landing con captura de email
  - Backend que guarde leads y entregue el PDF
  - Deploy en producción (VPS propio o compartido)
- **Rúbrica sugerida**: calidad del PDF · funcionamiento end-to-end · decisiones de arquitectura explicadas · 1 lead capturado de alguien real (familiar/colega) en la semana.

### D · Como ejercicio de lectura de código / troubleshooting
- **Momento**: módulo de backend con Cowork.
- **Formato**: abrir el archivo `copiloto_leads.py`. Entender qué hace cada endpoint. Modificar: agregar un segundo lead magnet nuevo al `LEAD_MAGNETS` dict. Desplegar. Verificar.
- **Objetivo**: que el alumno se sienta cómodo abriendo código que NO escribió, entendiéndolo y extendiéndolo.

### E · Como meta-reflexión sobre marketing
- **Momento**: módulo de marketing + AI para founders.
- **Formato**: discusión grupal. "¿Por qué el lead magnet de Andrés es sobre Obsidian si el programa enseña Claude Code? ¿Qué relación hay?" Exploración de cómo un asset gratis muestra el nivel de entrega y prepara al lead para comprar.
- **Objetivo**: pensar estratégicamente en el funnel, no solo tácticamente.

### Mi recomendación (sin que me lo pidas)
Combinar **A** (semana 1 como promesa) + **C** (ejercicio propio del alumno en módulo de marketing) + **B** (cuando se enseña briefing a Cowork). D y E son opcionales si sobra tiempo.

---

## 5 · Archivos y recursos para la clase

Todos disponibles si el diseñador los necesita:

### Código fuente local
- Landing HTML: `/Users/specialandres/copiloto-landing/segundo-cerebro/index.html` (~900 líneas con CSS + HTML + SVG inline + JS del form)
- PDF HTML origen: `/Users/specialandres/copiloto-landing/pdf-build/guia.html`
- Backend: `/tmp/copiloto-deploy/copiloto_leads.py` (local) / `/root/.openclaw/workspace/dashboard/backend/routers/copiloto_leads.py` (VPS)
- Nginx: `/tmp/copiloto-deploy/nginx.conf`

### Artefactos en Obsidian vault (privado — para uso interno del programa)
- Project note completo: [[01-projects/copiloto-lead-magnet-segundo-cerebro/index|index]]
- Playbook reutilizable: [[02-areas/producto/playbook-lead-magnet-copiloto|Playbook: Lead Magnet para Programa Copiloto]]

### El prompt para Claude Cowork (extracto de página 13 del PDF)
Reutilizable para enseñar briefing. Ver el PDF directamente en la URL pública.

### Infraestructura disponible para alumnos
- VPS compartido (o cada alumno el propio — Hostinger KVM 1 a USD 5/mes)
- Dominio `copiloto.specialandres.ar` (el principal) o subdominios propios de alumnos
- Estructura reutilizable: `LEAD_MAGNETS` dict es extensible a N guías distintas sin cambiar código

---

## 6 · Datos operativos del proyecto

Para contexto del diseñador:

- **Tiempo real de ejecución**: ~3 horas una sola sesión, incluye draft de contenido + landing + PDF + backend + deploy + iteración sobre maquetación del PDF.
- **Costo de infra incremental**: USD 0. Reusa VPS, servicio FastAPI, nginx, CRM, dominio y cert SSL ya existentes del programa.
- **Tecnologías**: HTML plano + CSS vanilla + FastAPI + SQLite + nginx + Chrome headless para PDF. Nada exótico.
- **Decisión clave que importa enseñar**: NO crear una tabla nueva de "lead_magnet_leads". Extender la existente con `source`. Esto es una decisión de seniority — la respuesta incorrecta (crear tabla nueva) te lleva a 2 sistemas separados que nunca se reconcilian.

---

## 7 · Preguntas para el diseñador

Cosas que decidir del lado pedagógico (Andrés no opinó, lo dejamos en tus manos):

- [ ] ¿Qué módulos actuales tenés donde esto encaja?
- [ ] ¿Preferís mostrarlo como demo en vivo o como replay grabado?
- [ ] ¿Querés que armemos los materiales de clase (slides, transcript, homework spec)?
- [ ] Si activamos el ejercicio C (replicable por alumno), ¿qué pasa con los alumnos sin negocio propio? ¿Armamos casos ficticios de base?
- [ ] ¿El prompt para Claude Cowork de la página 13 se enseña como está o lo adaptamos al tema del alumno?

---

## 8 · Siguiente paso sugerido

1. Leer este brief.
2. Abrir la landing y descargar el PDF (lleva 5 min).
3. Volver con:
   - Qué opción (A/B/C/D/E o combinación) vas a activar.
   - Cronograma tentativo de integración a la currícula.
   - Lista de materiales adicionales que necesitás que preparemos.

Cualquier duda → preguntale a Andrés directamente o pedí acceso al proyecto en el vault de Obsidian.
