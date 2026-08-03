---
date: 2026-06-15
type: project
tags: [transicion, carrera, plan]
status: active
---

# Transición Andrés — Plan Carriles A+B (jun 2026)

Dos carriles en paralelo. **A = consultoría (caja en 30-60 días)**, **B = empleo remoto USD**. Runway 1-2 meses → ejecución.

- [[carril-a-consultoria|Carril A — Consultoría]] (oferta · prospectos · scripts)
- [[cartera-servicios-cpg-funcional|Cartera servicios CPG Funcional (jul 2026)]] (escalera · 4 prospectos · conflictos KR/PGN · síntesis panel)
- [[carril-b-empleo|Carril B — Empleo remoto USD]] (2 CVs · LinkedIn · mapa de roles)
- [[benchmarks-mercado|Benchmarks de mercado + posicionamiento]]

## Posicionamiento canónico

# POSICIONAMIENTO CANÓNICO — Andrés

> Documento maestro reutilizable. Toda pieza (CV, LinkedIn, outreach, propuesta, perfil de freelance) parte de acá. Números sin confirmar = `[A CONFIRMAR]`. No inventar.

---

## 1. STATEMENT DE POSICIONAMIENTO (el wedge en 1-2 frases)

**Versión corta (1 frase):**
> Operador de negocios reales que construye los sistemas de IA que los hacen funcionar — fundó y corrió una marca CPG multicanal y desarrolló solo, de punta a punta, la plataforma de IA que la operaba.

**Versión completa (2 frases):**
> La mayoría de los "expertos en IA" nunca operaron un negocio, y la mayoría de los operadores no saben construir software. Andrés hace las dos cosas: fundó y operó una marca CPG multicanal (D2C, marketplace, B2B, WhatsApp commerce) y construyó solo la plataforma de IA multi-tenant que la corría — y ya la vendió a un tercero en USD.

**Variante 1 línea para bio / headline:**
> Founder-operator que construye sistemas de IA para negocios reales. CPG + full-stack AI. Vendí mi plataforma a un cliente externo en USD.

---

## 2. INVENTARIO DE LOGROS / PRUEBAS (frasados con impacto)

### A. Operó un negocio CPG real, multicanal
- Fundó y operó **Smart Foods Argentina**, marca de alimentos funcionales con hongos adaptógenos, vendiendo en **5 canales simultáneos**: Shopify (D2C), MercadoLibre (marketplace), B2B mayorista, WhatsApp commerce e Instagram.
- Obtuvo **certificación regulatoria ANMAT/INAL** — barrera de entrada real en alimentos en Argentina, no trivial de conseguir.
- Escala / revenue / unidades vendidas: `[A CONFIRMAR con Andrés]`
- Tamaño de pipeline B2B: `[A CONFIRMAR — la DB menciona 665 prospectos; confirmar cuántos cerraron]`

### B. Construyó solo una plataforma de IA de nivel producción
- Diseñó y desarrolló **SmartBrain en solitario**: plataforma multi-tenant de automatización con IA, end-to-end (backend, frontend, infra, integraciones).
- Stack real: **FastAPI + uvicorn + aiosqlite (Python 3.12)** backend; **React 19 + Vite + Tailwind + TypeScript** frontend; **SQLite WAL, una DB por tenant**; auth **JWT + OTP por WhatsApp** con roles (ceo/ops/agency); **30+ routers modulares**.
- Capacidades en producción:
  - Bot de WhatsApp con **journeys conversacionales + respuestas LLM** (Gemini 2.5 Flash primario, OpenRouter fallback).
  - **Auto-publicación en Instagram** vía Graph API (imagen / carrusel / stories).
  - **Competitive intel**: scraping de Meta Ads + análisis con LLM.
  - **Prospección B2B**: Google Places API + scoring automático de leads.
  - Integraciones productivas: **Shopify, Klaviyo, Perfit, Tienda Nube, Meta Graph API**.
  - Pipeline de **generación de contenido con IA**, CRM B2B (pipeline kanban), analytics de revenue, reportes PDF.

### C. Validó el modelo en el mercado (la prueba más fuerte)
- Productizó SmartBrain como **SaaS multi-tenant** y firmó su **primer cliente externo: Korean Root, USD 1.000/mes**.
- Significado: **una empresa pagó en USD por el sistema de IA** que construyó — no por el producto físico. Validación de que su capacidad de building tiene valor de mercado independiente del CPG.

### D. Velocidad de construcción con IA (prueba de throughput)
- Construyó **múltiples juegos y simuladores de browser** con IA en días, incluyendo simuladores de negocio complejos: un **tycoon de suplementos en LATAM** (modela regulatorio, retail, working capital, influencers en 5 países) y un **sim de kiosco con economía argentina** (inflación, dólar blue, licuación de capital).
- Significado: traduce dominios complejos del mundo real a software funcional, rápido. No es teoría — es velocidad de ejecución demostrada.

---

## 3. MATRIZ DE SKILLS (priorizada por valor en el target USD)

### Técnicas — orden de mayor a menor diferenciación

| Prioridad | Skill | Por qué importa para el target |
|---|---|---|
| 1 | **Diseño de agentes de IA / integración de LLMs** (Gemini, OpenRouter, prompt engineering, fallback chains) | Es el skill más demandado y mejor pago hoy; lo demostró en producción, no en un demo |
| 2 | **Automatización end-to-end de negocio con IA** | El wedge tangible: conectar IA a operaciones reales (ventas, contenido, soporte) |
| 3 | **Full-stack asistido por IA** (Python/FastAPI + React/TypeScript) | Puede entregar features completas solo, sin equipo |
| 4 | **Integraciones de API REST** (Shopify, Meta, Klaviyo, Perfit, Google, WhatsApp Cloud) | Plomería que la mayoría evita; clave en automatización |
| 5 | **Arquitectura de backend** (FastAPI, multi-tenancy, SQLite/WAL, auth JWT+OTP) | Diseñó un sistema multi-tenant real, no un CRUD |
| 6 | **Data / SQLite + analytics** | Soporta decisiones, no solo features |

### De negocio — orden de mayor a menor diferenciación

| Prioridad | Skill | Por qué importa para el target |
|---|---|---|
| 1 | **Growth / marketing automation** (email, WhatsApp commerce, contenido con IA) | Donde IA + negocio se cruzan — su zona única |
| 2 | **E-commerce ops multicanal** (Shopify, MercadoLibre, Tienda Nube) | Experiencia operativa real, no consultiva |
| 3 | **Ventas B2B + brand building** | Cerró un cliente SaaS en USD; sabe vender |
| 4 | **Meta Ads / performance** | Construyó tooling de ads intel; entiende la plataforma |
| 5 | **Certificación regulatoria (ANMAT/INAL)** | Prueba de rigor y capacidad de navegar complejidad |

**Idiomas:** Español nativo (voseo argentino). Inglés: `[A CONFIRMAR — asumir profesional/working para roles remotos]`.

---

## 4. PROOF POINTS (cortos, memorables, para abrir o cerrar)

1. **"Construí solo la plataforma de IA que corría mi propia marca — y se la vendí a otra empresa por USD 1.000/mes."**
   → El wedge entero en una frase. Demuestra building + validación de mercado.

2. **"Operé una marca CPG en 5 canales a la vez: D2C, marketplace, mayorista, WhatsApp e Instagram."**
   → Operador real, no teórico.

3. **"Mi bot de WhatsApp con IA vende, publica en Instagram solo y prospecta clientes B2B — todo en producción."**
   → IA aplicada a resultados de negocio concretos, no demos.

4. **"Modelé la economía argentina —inflación, dólar blue, working capital— en un simulador funcional en días."**
   → Velocidad + capacidad de traducir dominios complejos a software.

---

## 5. NARRATIVA DEL CIERRE DE SMART FOODS (honesta, reutilizable)

**Versión 2-3 frases (default):**
> Construí y operé una marca CPG multicanal y desarrollé la plataforma de IA que la operaba. Estoy cerrando ordenadamente una estructura societaria que no prosperó, para enfocarme en mi activo más valioso: construir sistemas de IA que operan negocios reales. Soy un fundador que ejecutó, aprendió y se reorienta — con una validación concreta de que lo que construyo tiene mercado.

**Versión 1 frase (para LinkedIn / contextos cortos):**
> Tras fundar y operar una marca CPG y construir la plataforma de IA que la corría, estoy reorientándome a tiempo completo a construir sistemas de IA para negocios reales.

**Reglas de framing:**
- Nunca "fracaso", "quiebra" ni súplica. Es **reorientación estratégica**.
- El foco va siempre hacia adelante (qué construye ahora), no hacia atrás.
- El cierre societario se menciona una sola vez, sin dramatismo, e inmediatamente se pivotea al activo.

---

## 6. WATCH-OUTS (qué NO hacer al posicionarlo)

- **No inventar métricas.** Revenue, unidades, MRR, % de crecimiento, número de clientes B2B cerrados → todo `[A CONFIRMAR]` hasta que Andrés los dé. Un placeholder honesto > un dato falso.
- **No venderlo como "gurú de IA" ni con humo.** Cada claim anclado en algo que construyó u operó. Nada de "transformación digital", "sinergias", "thought leader".
- **No esconder ni dramatizar el cierre de Smart Foods.** Mencionar una vez, framear como reorientación, pivotear al activo. Ni ocultarlo (se nota) ni regodearse en el problema.
- **No diluir el wedge.** El diferencial es *operador + builder en una sola persona*. No posicionarlo como "otro dev full-stack" ni como "otro consultor de IA" — eso lo mete en océanos rojos donde compite por precio.
- **No sobre-tecnificar para audiencias de negocio ni sub-tecnificar para audiencias técnicas.** Ajustar densidad: a un CTO dale el stack; a un founder dale el resultado de negocio.
- **No presentar los juegos como hobby.** Son **prueba de throughput y de traducción de dominios complejos a software** — ese es el framing, no "hace jueguitos".
- **No asumir inglés fluido en piezas en inglés** hasta confirmar nivel. Si se confirma working/profesional, los CVs y LinkedIn van en inglés profesional.
- **No tratar a Korean Root como "un cliente más".** Es *la prueba de validación de mercado*. Siempre que aparezca, enmarcarlo como evidencia de que su building tiene valor independiente.

---

**Placeholders globales a completar por Andrés antes de publicar:** nombre completo, email, teléfono, LinkedIn, GitHub, web/portfolio, nivel de inglés, y todas las métricas marcadas `[A CONFIRMAR]`.

---

# PLAN DE ACCIÓN 7 DÍAS — Andrés

> Dos carriles en paralelo. **A = Consultoría (caja en 30-60 días).** **B = Empleo remoto USD.** Runway 1-2 meses → ejecución, no perfeccionismo. Esta semana es 80% setup de munición + primeros tiros, no esperás cerrar nada todavía (salvo suerte).

---

## ANTES DE EMPEZAR: regla de oro de la semana

No te dispersás. La trampa con runway corto es saltar entre las dos pistas todo el día y no avanzar ninguna. Solución: **bloques fijos por horario, no por impulso.**

- **Mañana (3-4 hs): Carril B (empleo).** Tu cerebro está fresco → CV, aplicaciones, perfiles, prep de pitch. Trabajo que requiere foco y calidad.
- **Tarde (3-4 hs): Carril A (consultoría).** Outreach, conversaciones, propuestas. Es trabajo más social/comercial, tolera energía media.
- **Por qué B a la mañana:** el empleo es tu piso de seguridad (ingreso estable y mayor), y las aplicaciones mal hechas se descartan en 6 segundos. La consultoría tolera más iteración sucia.

**Regla anti-dispersión:** una sola herramienta de tracking (un Google Sheet o Notion con 2 tabs: "Aplicaciones B" y "Pipeline A"). Todo contacto entra ahí el mismo día. Si no está en el sheet, no pasó.

---

## DÍA 1 (Lunes) — Munición base

**Mañana — Carril B**
- Decidí el título principal: **Forward-Deployed Engineer / AI Solutions Engineer** como header (es el rol con +800% de demanda y mejor fit con tu wedge). CV en inglés profesional.
- Escribí el CV base (1 página) usando el posicionamiento canónico. Header reconocible por ATS: *"Founder & Principal Engineer — SmartBrain (multi-tenant AI SaaS)"*, no "fundador integral".
- El hook arriba de todo: *"Built a multi-tenant AI platform solo, ran a multichannel CPG brand on it, and sold it to an external client for USD 1,000/mo."*

**Tarde — Carril A**
- Armá la **lista de 30 prospectos** de consultoría: fundadores DTC/ecommerce LATAM y US que conozcas o sigas (tu red de Smart Foods, competidores no-competidores, gente de comunidades). El que ya pagó —Korean Root— es tu caso, no tu prospecto.
- Escribí el **one-pager de oferta**: retainer productizado USD 2.000-3.500/mes, paquete cerrado (bot WA + automatización contenido/IG + competitive intel), anclado en "el operador que construye los sistemas de IA que corren tu marca DTC". Cero hourly.

---

## DÍA 2 (Martes) — Perfiles públicos + primer outreach

**Mañana — Carril B**
- Reescribí **LinkedIn** completo: headline = variante de bio del canónico, About con el wedge, experiencia SmartBrain con bullets numéricos (los que tengas confirmados).
- Limpiá/ordená **GitHub**: README decente en SmartBrain (aunque sea privado, andá pensando qué mostrás) y deja los juegos/sims públicos como prueba de throughput. Linkealos arriba en LinkedIn.

**Tarde — Carril A**
- Mandá los **primeros 10 mensajes de outreach** de consultoría (warm primero: gente que ya te conoce). Tono Andrés: directo, sin humo, voseo si es LATAM / inglés profesional si es US. No vendés "IA", ofrecés resolver SU problema concreto.
- Registrá los 10 en el sheet.

---

## DÍA 3 (Miércoles) — Aplicaciones en serio + case study

**Mañana — Carril B**
- Creá perfiles en **YC Work at a Startup** (canal #1 para founding eng / FDE) y **Wellfound** (filtro Remote + min USD 100K). Perfil único, hablás directo con founders.
- Aplicá a las **primeras 5 vacantes**, cada una con UNA línea específica de por qué ESA empresa (mata la alarma de "ex-founder matando tiempo"). Tailoring real, no copy-paste.

**Tarde — Carril A**
- Escribí el **case study de Korean Root** (1 página): problema → qué construiste → resultado (paga USD 1.000/mes por el sistema). Es tu prueba de venta más fuerte para los dos carriles.
- Mandá **5 outreach más** (ahora podés meter cold, con el case study adjunto/linkeado).

---

## DÍA 4 (Jueves) — Volumen + comunidades

**Mañana — Carril B**
- Revisá **HN "Who is hiring?"** (hnhiring.com/locations/remote, filtro remote) y aplicá a **5 más**. Acá postean antes que en los boards grandes.
- Grabá un **Loom de 60 seg** mostrando SmartBrain en vivo (el bot, el dashboard, un router). Muchos FDE/founding-eng screens piden esto async; tenerlo listo te diferencia y acelera.

**Tarde — Carril A**
- Entrá a **2-3 comunidades de founders DTC** (Slacks/Geneva/grupos). No spamees: presentate, aportá algo útil, dejá que tu wedge se vea. El canal #1 de compra es recomendación de pares.
- Seguimiento de los outreach del Día 2 que no respondieron (bump corto).

---

## DÍA 5 (Viernes) — Conversaciones + red de seguridad

**Mañana — Carril B**
- Registrate en **plataformas LATAM-US** (Arc.dev, Trio, Revelo) como red de seguridad — pagan en USD, techan más bajo, pero dan velocidad. No es tu canal principal, pero es piso.
- Practicá el **pitch verbal de 60 seg** sobre SmartBrain en inglés (grabate, escuchate). Si te trabás, esto es lo que arreglás este fin de semana.

**Tarde — Carril A**
- Apuntá a tener **3-5 conversaciones agendadas** para la semana que viene (calls de descubrimiento, no pitch). Confirmá las que salieron del outreach de Días 2-3.
- Para cada call agendada: prepará 3 preguntas sobre SU operación (no monólogo tuyo).

---

## DÍA 6 (Sábado) — Cierre de gaps (medio día)

- **Cerrá lo que quedó flojo:** el Loom si no salió, el inglés del pitch, completar placeholders del CV con números reales.
- **Calibrá pricing del retainer** según las primeras señales: si nadie pestañea con USD 2.000, subí; si todos frenan, revisá el empaquetado (no bajes precio de entrada, mejorá la oferta).
- Descanso real la otra mitad. Runway corto quema; el burnout te cuesta más caro que un día.

---

## DÍA 7 (Domingo) — Review semanal + plan Semana 2

- Llená el **scoreboard** (abajo) con los números reales.
- Decidí los ajustes de Semana 2 (sección "qué decidís").
- Preparás los próximos 30 prospectos / 15 vacantes para no arrancar el lunes en frío.

---

## MÉTRICAS DE LA SEMANA (scoreboard mínimo)

| Métrica | Target Semana 1 | Por qué |
|---|---|---|
| **Outreach consultoría enviados (A)** | 25-30 | Volumen para que el embudo arroje 3-5 conversaciones |
| **Conversaciones/calls agendadas (A)** | 3-5 | Señal real de interés, no vanity |
| **Propuestas enviadas (A)** | 0-2 | Si sale 1, es upside; no es el objetivo de la semana 1 |
| **Aplicaciones empleo (B)** | 15-20 | Con tailoring real, no spray; calidad sobre cantidad bruta |
| **Respuestas/screens (B)** | 2-4 | Tasa normal es baja; no te asustes |
| **Activos creados** | CV, LinkedIn, GitHub, one-pager, case study KR, Loom | Munición que se reusa toda la búsqueda |

> Regla: el número que más importa esta semana son **conversaciones** (A) y **respuestas** (B), no envíos. Los envíos son input; las respuestas te dicen si el mensaje pega.

---

## QUÉ DECIDÍS — fin de Semana 1

1. **¿El mensaje pega?** Si <10% de respuesta en outreach A → el problema es el mensaje o la lista, no el volumen. Reescribí el hook antes de mandar más.
2. **¿Dónde hay más tracción, A o B?** Mirá honestamente de qué lado llegaron más respuestas. La Semana 2 inclina recursos —no abandona— hacia donde haya señal.
3. **¿El pricing del retainer resiste?** Calibralo con las reacciones reales.
4. **¿El inglés es un cuello de botella?** Si en los primeros screens B te frenó, esa es la prioridad #1 de mejora.

## QUÉ DECIDÍS — fin de Semana 2

1. **Carril dominante:** con 2 semanas de data, definís si vas all-in a un carril o sostenés ambos. Criterio: ¿alguna propuesta A está por cerrar? ¿algún proceso B llegó a 2da vuelta?
2. **Caja inmediata:** si A no dio señales de cierre y el runway aprieta, activás la red de seguridad (Arc/Trio/Revelo + un proyecto chico USD 3-5K aunque sea por debajo de tu techo, para comprar tiempo).
3. **Foco de pipeline:** elegís el nicho/título que más respondió y duplicás esa apuesta. Dejás de regar parejo.
4. **Pricing v2:** ajuste fino de retainer y/o estructura (base + performance) según lo aprendido.

---

## PREGUNTAS DE CALIBRACIÓN — respondé esto y afino todo el plan

Sin estas respuestas, varias decisiones de arriba son a ciegas. Son cinco, directas:

1. **Inglés — nivel real, sin maquillar.** ¿Podés sostener un call de 30 min con un founder técnico americano hoy, sin fricción? ¿Escribir un mail profesional sin ayuda? Escala 1-5 hablado / 1-5 escrito. Esto define si B arranca ya o si hay 1-2 semanas de prep, y si los targets son US directo o vía plataformas LATAM-US.

2. **Breakeven personal en USD/mes.** ¿Cuánto necesitás para cubrir tu vida mensual mínima? El número exacto. Define si un proyecto puente de USD 3K alcanza, cuántos clientes A necesitás, y cuál es el piso salarial innegociable en B.

3. **AI-lead vs growth-lead — ¿dónde te ves y dónde disfrutás?** El mercado dice liderá con AI/builder (más demanda, mejor pago, más líquido remoto). Pero si donde brillás y la pasás bien es growth, lo balanceamos. ¿Querés meter las manos en código/agentes, o preferís estrategia/growth con la técnica como diferencial?

4. **¿Ya tenés LinkedIn / GitHub / portfolio?** ¿En qué estado? ¿LinkedIn actualizado o abandonado? ¿GitHub con repos públicos o todo privado? ¿Algún portfolio/web? Define cuánto del Día 1-2 es crear de cero vs pulir.

5. **Full-time vs contractor — ¿qué buscás realmente?** ¿Un empleo full-time estable (un solo empleador, relación de dependencia / EOR) o preferís ser contractor (varios clientes, más libertad, menos seguridad)? ¿O sos abierto a ambos y decide la mejor oferta? Esto define si los carriles A y B compiten o se complementan, y cómo estructurás el cobro (Deel, etc.).

**Bonus que ayudaría:** los números `[A CONFIRMAR]` del posicionamiento — revenue/escala de Smart Foods, cuántos de los 665 prospectos B2B cerraron. Cualquier métrica real que tengas hace tu CV y tu pitch mucho más fuertes. Si no los tenés a mano, los dejamos como están; mejor placeholder honesto que número inventado.

---

Andrés, una marca antes de soltar esto: la semana es deliberadamente de **construir munición + primeros tiros**, no de cerrar. Con runway de 1-2 meses la tentación es exigirte un cierre en 7 días y frustrarte. El cierre real llega semana 3-5. Lo que esta semana tiene que dejarte es: arsenal completo (CV/perfiles/case study/oferta) + embudo cargado + las 5 respuestas de calibración que afinan todo lo demás. Eso es ganar la semana 1.
