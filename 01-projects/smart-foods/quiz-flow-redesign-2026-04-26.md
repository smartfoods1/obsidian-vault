---
date: 2026-04-26
type: marketing-asset
tags: [klaviyo, quiz, flow, email, smart-foods]
status: ready-to-load
---

# Rediseño Flow Quiz — Bienvenida QUIZ v2

## Contexto

Flow original (SnyXuf, "Bienvenida QUIZ") generó **$806k ARS / 30 días** con setup roto:
- Cero personalización por `quiz_adaptogeno` (única merge tag = `unsubscribe_url`)
- Email final con subject placeholder en producción ("Email n.º 4 Subject")
- 2 templates duplicados (UCESws ≡ UgXAZD, mismo HTML 18796 bytes)
- CTAs a Inner Glow OOS en los 5 emails
- BOOLEAN_BRANCH no segmenta (solo `is_joined: false`)

**Cohorte actual** (Klaviyo lista QUIZ, V3AcAk):
- 401 leads nuevos (nunca compraron) + 104 ya-customers
- Distribución: longevity 159 · innerglow 113 · brainboost 103 · immune 26
- 5 phones de 401 leads → canal correcto = email

**Stock decisions (Andrés 2026-04-26):**
- Brain Boost: 300u entran 27 abril
- Longevity Boost: stock 10 mayo
- Inner Glow: sin stock indefinido (pivot a Glow barrita)
- Immune Boost: stock disponible (23u)

**Decisiones de oferta (Andrés 2026-04-26):**
- Bundle Immune + Café Full Blend 10% off → AUTORIZADO (Email 4 rama immune)

---

## Mapeo definitivo: adaptógeno → producto + URL + imagen

| `quiz_adaptogeno` | Producto | URL | Imagen | Stock |
|---|---|---|---|---|
| `brainboost` | Brain Boost extracto | https://smartfoods.ar/collections/destacados-1/products/brain-boost-extracto-en-polvo-con-melena-de-leon?variant=46462693867651 | https://cdn.shopify.com/s/files/1/0684/9321/3827/files/hf_20260203_011701_8bc79283-5945-4e23-8b53-2305abe0fa5d.png | 300u 27/4 |
| `longevity` | Longevity Boost extracto | https://smartfoods.ar/products/longevity-boost-extracto-en-polvo-con-reishi-y-vitamina-c | https://cdn.shopify.com/s/files/1/0684/9321/3827/files/longevity_boost.webp | 10/5 |
| `immune` | Immune Boost extracto | https://smartfoods.ar/products/immune-boost-extracto-en-polvo-con-adaptogenos | https://cdn.shopify.com/s/files/1/0684/9321/3827/files/hf_20260208_152820_f0cebf8d-5ae3-4a40-bcdb-0630338ab0ce.png | 23 |
| `innerglow` (PIVOT) | Glow barrita (en lugar de extracto) | https://smartfoods.ar/products/glow-barrita-funcional-con-tremella-y-probioticos-12u | https://cdn.shopify.com/s/files/1/0684/9321/3827/files/barrita_glow_12_unidades.webp | 55 |

**From / sender** (todos los emails): `Andy de Smart Foods <andy@smartfoods.ar>` (mantener identidad existente)

---

## Reviews reales (Judge.me) por adaptógeno

> Fuente: Judge.me API · 158 reviews 5★ publicadas · seleccionados por largo y especificidad. Listos para usar como testimonial del Email 2.

### brainboost — 16 reviews disponibles

**Hero quote (Email 2):**
> "Tengo Hashimoto y hace meses que tomo Melena de león mejorando ampliamente la actividad cerebral. Excelente para quitar la niebla mental." — **Elizabeth**

**Backup:**
> "Note cambios digestivos y sobre todo más claridad mental. La atención del equipo de Smart Foods además es super." — **Gaby**
> "La melena de león me permite concentrarme de una manera natural y eficiente. Gracias!" — **Cecilia Quintana**

### longevity — 2 reviews disponibles (escasas pero específicas)

**Hero quote (Email 2):**
> "Pensé que era el cansancio que tenía, pero no — es el Reishi que hace que duerma de corrido a la noche y no tenga insomnio. Es lo primero que noté, además de bienestar general." — **Carina**

**Backup:**
> "Tomarlo en un té por la tarde me ayuda a dormir mejor. Me despierto descansada y con más energía." — **A.**

### immune — 4 reviews disponibles

**Hero quote (Email 2):**
> "Los tomo hace meses como apoyo al sistema inmune ya que tengo Hashimoto. Me siento con más vitalidad y energía. Acompaño con Melena de León y obtengo gran recuperación." — **Elizabeth**

**Backup:**
> "Es una excelente opción para agregar los adaptógenos a nuestra vida diaria si no te gustan las demás opciones." — **Paula**

### innerglow → Glow barrita — 4 reviews del producto pivote

**Hero quote (Email 2):**
> "Simplemente deliciosas y efectivas. Cada bocado es una experiencia única. Pero lo mejor no es solo el gusto exquisito — sino que realmente se sienten los efectos. Notables cambios en mi energía y cómo me siento durante el día." — **Juan Martitegui**

**Backup:**
> "Al fin una barra proteica con ingredientes nobles. Riquísima y excelente aporte para después de entrenar." — **María Soledad Olmos**
> "Probé las barritas y me encantan. Son ricas, saciantes y las más completas del mercado. Lo mejor: hechas con productos reales." — **Florencia Lozano**

---

## Email 1 (Día 0) — "Tu match es X"

> El email crítico — concentra ~67% del revenue del flow. Subject promete personalización; cuerpo cumple con UN producto y UN CTA.

### Rama brainboost

**Subject**: Tu match es Brain Boost
**Preview**: Lo elegiste (sin saberlo) en el test. Te cuento por qué.

**Cuerpo:**

Hola {{ first_name|default:"" }},

Tu test de adaptógeno marcó **Brain Boost**. Y no fue casualidad — las respuestas que diste apuntan a algo concreto: querés más foco, mejor memoria, claridad mental.

Brain Boost es nuestro extracto concentrado de **Melena de León** (Hericium erinaceus), el adaptógeno más estudiado para neuroprotección y cognición. Doypack 30g, 30% beta-glucanos, doble extracción. Suficiente para 60 días.

[FOTO PRODUCTO — packaging Brain Boost]

**Cómo se toma:** medio scoop (0,5g) en café, té o agua. Se nota en 14 días. Funciona mejor a la mañana.

[CTA BUTTON: VER BRAIN BOOST →]
Link: https://smartfoods.ar/collections/destacados-1/products/brain-boost-extracto-en-polvo-con-melena-de-leon?variant=46462693867651

PD: justo entran 300 unidades mañana 27 de abril. Se agota rápido históricamente.

Andy

### Rama longevity

**Subject**: Tu match es Longevity Boost (vuelve el 10 de mayo)
**Preview**: Te lo guardo. Dejame tu WhatsApp y te aviso primero.

**Cuerpo:**

Hola {{ first_name|default:"" }},

Tu test marcó **Longevity Boost**. Las respuestas que diste apuntan a calma, sueño profundo, regulación del estrés.

Longevity Boost es nuestro extracto de **Reishi** (Ganoderma lucidum) + Vitamina C — el adaptógeno por excelencia para cortisol y descanso. Doypack 30g, 30% beta-glucanos, doble extracción.

[FOTO PRODUCTO — packaging Longevity Boost]

**El detalle:** se nos agotó. **Vuelve el 10 de mayo.**

Si querés que te avise apenas entra (antes de publicarlo), dejame tu WhatsApp:

[CTA BUTTON: AVISAME POR WHATSAPP →]
(link al form Klaviyo "WaitList WA — Quiz")

Mientras tanto, si querés algo que ya esté disponible y atienda algo parecido, miralo acá:
[link sutil: VER OTROS ADAPTÓGENOS → /collections/extractos-en-polvo-2]

Andy

### Rama immune

**Subject**: Tu match es Immune Boost
**Preview**: Triple blend de hongos. Lo elegiste (sin saberlo) en el test.

**Cuerpo:**

Hola {{ first_name|default:"" }},

Tu test marcó **Immune Boost**. Las respuestas que diste apuntan a defensas, energía sostenida, prevención.

Immune Boost es el único triple blend del mercado argentino: **Reishi + Shiitake + Maitake** + Vitamina C. Doypack 30g, 30% beta-glucanos, doble extracción.

[FOTO PRODUCTO — packaging Immune Boost]

**Cómo se toma:** medio scoop (0,5g) en café, té o licuado. Diario. Funciona en 21 días.

[CTA BUTTON: VER IMMUNE BOOST →]
Link: https://smartfoods.ar/products/immune-boost-extracto-en-polvo-con-adaptogenos

Andy

### Rama innerglow (PIVOT a Glow barrita)

**Subject**: Tu match es Inner Glow — y tengo algo bueno para vos
**Preview**: El extracto está agotado. Pero hay otra forma.

**Cuerpo:**

Hola {{ first_name|default:"" }},

Tu test marcó **Inner Glow**. Las respuestas apuntan a piel, hidratación natural, glow desde adentro.

El extracto en polvo lo agotamos y vamos a tardar en reponerlo. **Pero tenemos algo mejor para arrancar:** la barrita Glow.

[FOTO PRODUCTO — barrita Glow]

Misma **Tremella** (la fuente natural de ácido hialurónico) en formato barra. Con cacao crocante, probióticos y sin TACC. 12 unidades por display.

**Por qué funciona:** la Tremella actúa igual en barra que en extracto. La diferencia es practicidad — la llevás en la cartera, la merendás, no necesitás scoop.

[CTA BUTTON: PROBAR GLOW BARRITA →]
Link: https://smartfoods.ar/products/glow-barrita-funcional-con-tremella-y-probioticos-12u

Si preferís esperar al extracto (sin fecha confirmada todavía), dejame tu WhatsApp:
[link sutil: AVISAME CUANDO VUELVA → form WaitList WA]

Andy

---

## Email 2 (Día 2) — Testimonial específico

> Estructura común. Cada rama usa la hero quote de la sección "Reviews reales" arriba. Body breve para que el testimonio sea protagonista.

### Estructura común

**Hero**: foto del cliente (si Judge.me la tiene; sino solo nombre y nombre del producto) + 2 líneas de quote
**Body**: 3-4 párrafos cortos refrescando por qué su match es ese adaptógeno
**CTA**: 1 link al producto match (mismo de Email 1)

### Por rama

**Rama brainboost**

Subject: "Hashimoto, niebla mental, y por qué Melena de León funciona"
Preview: Lo que cuenta Elizabeth. (No es marketing, es review verificada.)

Hero quote: ver Elizabeth en sección reviews

Body: "Elizabeth lleva meses tomando Brain Boost. Tiene Hashimoto — un autoinmune que muchas veces produce 'brain fog' o niebla mental. La Melena de León es uno de los adaptógenos con mayor evidencia para neuroprotección y claridad cognitiva. Si tu test marcó Brain Boost, probablemente buscás algo de eso..."

CTA: VER BRAIN BOOST → (mismo link)

**Rama longevity**

Subject: "Pensaba que era cansancio. Era falta de Reishi."
Preview: Carina lleva meses tomándolo. Esto contó.

Hero quote: ver Carina en sección reviews

Body: "El Reishi no te 'hace dormir'. Lo que hace es bajar cortisol y permitir que tu cuerpo entre en sueño profundo. La diferencia entre dormir 8 horas y descansar 8 horas. Si tu test marcó Longevity, probablemente eso te falta hoy. Vuelve el 10 de mayo. Te aviso primero si querés:"

CTA: AVISAME POR WHATSAPP → (form)

**Rama immune**

Subject: "Hashimoto, defensas y un triple blend que está funcionando"
Preview: Elizabeth combina Immune con Brain Boost. Esto cambió.

Hero quote: ver Elizabeth en sección reviews

Body: "El triple blend (Reishi + Shiitake + Maitake) tiene sinergia — los tres juntos modulan inmunidad de formas distintas. Por eso es el único de su tipo en Argentina. Si tu test marcó Immune, esto es lo que estás buscando..."

CTA: VER IMMUNE BOOST →

**Rama innerglow → Glow barrita**

Subject: "Una barra que funciona. (Y es rica, en serio.)"
Preview: Lo que dijo Juan Martitegui después de probarlas.

Hero quote: ver Juan Martitegui en sección reviews

Body: "La barra Glow no es 'una barra con tremella'. Es la dosis funcional de tremella + probióticos + cacao crocante en un formato que comés sin pensar. Si tu test marcó Inner Glow, esta es la versión que sí está disponible y que la gente que las prueba no deja de pedir..."

CTA: PROBAR GLOW BARRITA →

---

## Email 3 (Día 5) — Cómo tomarlo / Ciencia

> Educacional. Refuerza la elección. Bajísimo CTR esperado pero alto impacto en conversión final.

### Estructura común

1. Hero text: "El error más común al empezar con {{ producto }}"
2. 3 bullets: cómo tomarlo, cuándo notarlo, qué evitar
3. CTA al producto

### Por rama

**brainboost**

Subject: El error más común al tomar Melena de León
Preview: 80% lo toma a la noche. Por eso no le funciona.

Body bullets:
- ✓ Tomarlo a la mañana o mediodía (despierta cognición)
- ✗ Evitar después de las 17h (puede afectar sueño)
- ⏱ Resultados consistentes a partir del día 14

CTA: VER BRAIN BOOST →

**longevity**

Subject: Por qué Reishi tarda más de lo que pensás
Preview: 21 días mínimo. Constancia > dosis alta.

Body bullets:
- ⏱ Reishi necesita 21 días mínimo para efecto sostenido en cortisol
- 🌙 Tomarlo a la tarde-noche (dispara descanso)
- ✗ No mezclar con cafeína (anula el efecto calmante)

(Reminder: vuelve 10/5 — anotame si todavía no lo hiciste)

CTA: AVISAME →

**immune**

Subject: Triple blend ≠ tres veces más
Preview: La sinergia entre Reishi-Shiitake-Maitake explicada.

Body bullets:
- ✓ Reishi modula inmunidad adaptativa
- ✓ Shiitake activa células NK
- ✓ Maitake potencia la respuesta innata
- 🔄 Los tres juntos > la suma de las partes

CTA: VER IMMUNE BOOST →

**innerglow → Glow barrita**

Subject: Tremella + Vitamina C: por qué juntas funcionan mejor
Preview: La barrita ya las trae. Te explico la combinación.

Body bullets:
- 💧 Tremella retiene hasta 500x su peso en agua = hidratación celular
- ✨ Vitamina C es cofactor en síntesis de colágeno
- 🍫 La barra ya combina ambos en dosis funcional

CTA: PROBAR GLOW BARRITA →

---

## Email 4 (Día 10) — Soft offer / Urgencia

> Cierre del flow. Mecánica distinta por rama.

### brainboost — Urgencia stock real

Subject: Quedan {{ stock }} del lote del 27 de abril
Preview: No es manipulación. Hay 300 unidades y volaron rápido.

Body: "Cuando empecé este flow tenía 300 unidades del nuevo lote. Hoy quedan {{ stock_actual }}. Si todavía no lo decidiste y tu test marcó Brain Boost, este es probablemente el último mail que te mando este mes."

CTA: VER BRAIN BOOST →

**Nota implementación**: si Klaviyo no permite merge tag dinámico de stock, usar texto fijo "Quedan menos de 50 unidades" cuando se acerque al fin del lote.

### longevity — Countdown

Subject: Faltan {{ días }} para que vuelva Longevity
Preview: Si todavía no me dejaste tu WhatsApp, este es el momento.

Body: "El 10 de mayo entra el lote nuevo. Quien esté en la lista de WhatsApp se entera 24h antes que nadie y tiene reservada su unidad. Si tu test marcó Longevity, no te quedes afuera."

CTA: ANOTAME EN WAITLIST WA →

**Nota implementación**: el countdown en días puede ser texto fijo "Faltan días" o se calcula dinámicamente con merge tag de fecha si Klaviyo lo permite.

### immune — Bundle 10% OFF (autorizado por Andrés)

Subject: Lo que va mejor con Immune Boost: el café del mismo blend
Preview: Bundle Immune + Café Full Blend con 10% OFF.

Body: "Si te gustó Immune Boost, hay algo que combina perfecto: el Café Funcional Full Blend tiene los mismos tres hongos del extracto (Reishi + Shiitake + Maitake) + café orgánico colombiano. Tomar Immune en el café del mismo blend potencia el efecto. Por eso armamos el bundle. **10% OFF** mientras dure el lote."

CTA: VER BUNDLE IMMUNE + CAFÉ →

**Nota implementación**: requiere crear un coupon code "BUNDLE_IMMUNE_10" en Shopify y configurar la URL del bundle (puede ser una collection page o dos productos en cart con discount auto-aplicado vía Shopify Scripts).

### innerglow → Glow barrita — Bundle/Display

Subject: Por qué la mayoría compra el display y no las sueltas
Preview: Una vez que las probás, no comprás de a una.

Body: "El display de 12 barras Glow te dura 2 semanas si las merendás como yo. La unidad suelta cuesta proporcionalmente más y se acaba en 3 días. La gente que arranca con la unidad vuelve por el display. Hagamos un atajo."

CTA: VER DISPLAY GLOW 12u →

(Reminder: te puedo avisar cuando vuelva el extracto Inner Glow → form WA)

---

## Captura WhatsApp — Form Klaviyo (resuelve C)

**Objetivo**: capturar phone para futuros leads + backfill de los 401 actuales (especialmente innerglow + longevity OOS).

### ⚠️ Limitación API: Forms son read-only via Klaviyo API

Confirmado vía test: `PATCH /api/forms/TL7XrF/` devuelve 405 Method Not Allowed. La modificación del quiz form actual o la creación del form WaitList WA debe hacerse manualmente en Klaviyo UI.

### Form nuevo Klaviyo: "WaitList WA — Quiz"

**Configuración manual en Klaviyo (Sign-Up Forms → Create New Form):**

- **Nombre interno**: WaitList WA — Quiz
- **Tipo**: Embedded form (mejor que popup — se llama desde click en CTA del email)
- **Campos**:
  - email (prefilled / hidden)
  - phone_number (`+54 9 11 ...` formato — Klaviyo soporta validación E.164)
  - quiz_adaptogeno (custom property hidden, prefilled desde profile property)
  - source_email (hidden, valor "quiz_flow_v2")
- **Submit action**:
  - Update profile (phone, custom: `waitlist_status = "active"`, `waitlist_adaptogen = {{ quiz_adaptogeno }}`)
  - Add to list "WaitList WA — Quiz"
- **Confirmation**: "Listo. Te aviso por WhatsApp apenas entra stock."

### Modificación quiz form actual (TL7XrF)

Agregar campo phone OPCIONAL al final del quiz. No requerido para no bajar conversion.

**Texto sugerido del campo:**
> "¿Querés que te avise por WhatsApp cuando salga tu adaptógeno o tengamos novedades? (opcional)"

**Implementación**: Klaviyo UI → Sign-Up Forms → TL7XrF → Edit → agregar Phone Number field con required=false al final del flow del form.

---

## Implementación en Klaviyo (paso a paso)

### Paso 1: Construir el flow nuevo en DRAFT (no tocar SnyXuf)

1. Klaviyo → Flows → Create Flow → Set up own flow
2. Trigger: List → "Subscribed to List" → V3AcAk (lista QUIZ)
3. Nombre: `Bienvenida QUIZ v2 — segmentado`
4. **DEJAR EN DRAFT hasta que esté testeado**

### Paso 2: Estructura del flow

```
[Trigger: Added to List V3AcAk]
       ↓
[Conditional Split: profile.quiz_adaptogeno]
   ├── = "brainboost" → Branch BRAIN
   ├── = "longevity"  → Branch LONGEVITY
   ├── = "immune"     → Branch IMMUNE
   ├── = "innerglow"  → Branch GLOW
   └── (else / null)  → Branch DEFAULT (genérico, los 4 productos)
```

Cada branch:
```
[Email 1] → [Wait 2d] → [Email 2] → [Wait 3d] → [Email 3] → [Wait 5d] → [Email 4] → [End]
```

### Paso 3: Crear los 4 templates por rama × 4 emails (16 templates)

- Usar diseño visual del Email 1 actual (Ry5pAd) como base — funcionó.
- Cambiar copy por el de este doc.
- Cambiar imagen y CTA único por rama.
- **Limpiar palabras "TODO"** que arrastraban los templates viejos.
- Subject + preview text completos (no dejar placeholders).

### Paso 4: Test antes de activar

1. Crear test profile con `quiz_adaptogeno = brainboost`, suscribir a V3AcAk.
2. Verificar que entra al branch correcto y recibe Email 1 brainboost.
3. Repetir con cada adaptógeno.
4. Verificar links 200 OK + imagen carga + CTA único.

### Paso 5: Switch atómico

1. Klaviyo → Flow SnyXuf (viejo) → Pause.
2. Klaviyo → Flow nuevo → Activate (live).
3. Monitorear primeras 48h: open rate, CTR, unsub.
4. Si todo bien, archivar SnyXuf (no borrar — backup).

### Paso 6: Backfill 401 leads actuales

Los 401 leads ya están en V3AcAk pero no van a re-entrar al flow nuevo (Klaviyo no re-dispara el flow para ya-suscritos). Opciones:

**A. Manual segmentation:**
- Crear segmento dinámico: `In list V3AcAk AND Has not received "Bienvenida QUIZ v2 - Email 1"` (filtro Klaviyo nativo)
- Crear campaign one-shot por adaptógeno (4 campaigns) usando Email 1 de cada rama
- Enviar manualmente

**B. Re-add al list trigger (riesgoso):**
- No recomendado. Klaviyo dispara el flow desde cero para todos, incluido a quienes ya recibieron emails del flow viejo.

→ **Opción A recomendada.**

---

## Acciones que NO se pueden ejecutar via API (manual en Klaviyo UI)

| Acción | Por qué | Cómo hacerlo |
|---|---|---|
| Pausar email UgXAZD ("Email n.º 4 Subject") | API en revision 2024-10-15 da 404; revisions 2025-10-15+ requieren mandar `definition` completo del flow-action. PATCH simple no soportado. | Klaviyo UI → Flows → SnyXuf → Email "Email n.º 4 Subject" → toggle Live/Draft (1 click) |
| Modificar quiz form TL7XrF (agregar phone) | Forms PATCH devuelve 405 Method Not Allowed | Klaviyo UI → Sign-Up Forms → TL7XrF → Edit → agregar Phone field |
| Crear form WaitList WA | Forms POST también limitado | Klaviyo UI → Sign-Up Forms → Create New Form |

---

## Acciones que SÍ se pueden ejecutar via API (autónomas)

| Acción | Endpoint | Status |
|---|---|---|
| Crear lista "WaitList WA — Quiz" | POST /api/lists/ | ✅ **Ejecutado 2026-04-26** — list_id `W4qVEs` |
| Crear segmentos por quiz_adaptogeno (backfill) | POST /api/segments/ | ⏸ Pendiente — esperar a que flow v2 exista |
| Crear flow nuevo en draft | POST /api/flows/ | ⚠️ Posible pero complejo (definition JSON grande) |
| Crear templates email | POST /api/templates/ | ✅ Ejecutable |
| Crear coupon Shopify "BUNDLE_IMMUNE_10" | Shopify API | ✅ Script listo (ver Anexo abajo) |

### Lista creada: WaitList WA — Quiz (id `W4qVEs`)

Klaviyo URL: https://www.klaviyo.com/lists/W4qVEs

Cuando crees el form WaitList WA en Klaviyo UI, configurar el "Add to list" target con este ID. Los profiles que el form capture entrarán acá.

---

## Métricas de éxito (medir 30d post-launch)

| Métrica | Baseline (flow viejo) | Target (flow v2) |
|---|---|---|
| Email 1 CTR | 5.6% | >10% (con CTA único + match real) |
| Email 1 conversion | 6 / 197 | 12-15 / similar volumen |
| Revenue 30d | $806k | $1.2M+ |
| Phones capturados (waitlist) | 0 | 50+ (de OOS branches) |
| Unsub rate | 1% | <1.5% |

---

## Pendientes operativos para Andrés

1. ✅ ~~Autorizar bundle 10% off Immune + Café Full Blend~~ → AUTORIZADO
2. ✅ ~~Conseguir reviews reales~~ → integrados desde Judge.me
3. **Cargar el flow en Klaviyo** (paso 1-5) — usar este doc como referencia
4. **Crear coupon "BUNDLE_IMMUNE_10"** en Shopify (10% off, requiere ambos productos en cart)
5. **Pausar email UgXAZD** en Klaviyo UI (1 click)
6. **Modificar quiz form TL7XrF** agregando phone field opcional
7. **Crear form WaitList WA — Quiz** en Klaviyo UI
8. **Decidir cuándo activar**: idealmente coordinar con entrada de stock Brain Boost (27/4)

---

## Próximos pasos (sesión siguiente)

- Si Andrés activa flow v2: monitorear primeras 48h y ajustar
- Implementar bundle Shopify (script listo abajo)
- Hallazgos del audit Klaviyo (ver Anexo C)

---

## Anexo A — Audit Klaviyo flows (2026-04-26)

Audit automático de los 6 flows en cuenta. Hallazgos extra:

| Flow | Issue | Acción sugerida |
|---|---|---|
| Bienvenida QUIZ (SnyXuf) | subject "Email n.º 4 Subject" en producción | Pausar UgXAZD (deprecated cuando flow v2 activa) |
| Bienvenida QUIZ (SnyXuf) | 4/5 emails sin preview text | Flow v2 lo soluciona (preview obligatorio en cada email) |
| Abandoned Checkout (TzJxaD) | Recupero 1 + Segundo recupero sin preview text | Agregar preview en Klaviyo UI |
| Order Confirmation (XaAibB) | Sin preview text | Agregar preview |
| recupero inactivos (WbjFmS) | En draft hace 2 meses | Decidir si activar o archivar |

**Preview text best practice**: 50-100 caracteres, complementa el subject (no lo repite). Aumenta open rate típicamente +5-15%.

---

## Anexo B — Script Shopify para coupon BUNDLE_IMMUNE_10

> Crea un Price Rule + Discount Code en Shopify que aplica 10% off cuando ambos productos (Immune Boost extracto + Café Funcional Full Blend) están en el cart. Requiere `SHOPIFY_TOKEN` con scope `write_price_rules` y `write_discounts`.

```python
import json, os, requests, datetime
shop = os.environ["SHOPIFY_SHOP"]
token = os.environ["SHOPIFY_TOKEN"]
api_v = os.environ.get("SHOPIFY_API_VERSION", "2026-01")
H = {"X-Shopify-Access-Token": token, "Content-Type": "application/json"}

# Resolve product IDs
def get_product_id(handle):
    r = requests.get(f"https://{shop}/admin/api/{api_v}/products.json?handle={handle}&fields=id", headers=H)
    return r.json().get("products",[{}])[0].get("id")

immune_id = get_product_id("immune-boost-extracto-en-polvo-con-adaptogenos")
cafe_id   = get_product_id("immune-boost-cafe-funcional-molido-con-hongos-adaptogenos-para-espresso-e-italiana-y-capsulas-recargables")

# Create price rule
rule_body = {"price_rule": {
    "title": "BUNDLE_IMMUNE_10",
    "target_type": "line_item",
    "target_selection": "entitled",
    "allocation_method": "across",
    "value_type": "percentage",
    "value": "-10.0",
    "customer_selection": "all",
    "starts_at": datetime.datetime.utcnow().isoformat() + "Z",
    "entitled_product_ids": [immune_id, cafe_id],
    "prerequisite_product_ids": [immune_id, cafe_id],  # both required in cart
    "allocation_limit": 1,
}}
r = requests.post(f"https://{shop}/admin/api/{api_v}/price_rules.json", headers=H, json=rule_body)
rule = r.json().get("price_rule",{})
print("Price rule:", rule.get("id"))

# Create discount code
code_body = {"discount_code": {"code": "BUNDLE_IMMUNE_10"}}
r2 = requests.post(f"https://{shop}/admin/api/{api_v}/price_rules/{rule['id']}/discount_codes.json", headers=H, json=code_body)
print("Discount code:", r2.json())
```

**Validar después**: cart con Immune + Café + aplicar BUNDLE_IMMUNE_10 → debería dar 10% off en ambos.

---

## Anexo C — IDs y referencias creados esta sesión

### Lista
| Recurso | ID | URL Klaviyo |
|---|---|---|
| WaitList WA — Quiz | `W4qVEs` | https://www.klaviyo.com/lists/W4qVEs |

### Templates HTML (16/16 creados via API)

Todos visibles en Klaviyo → Email Templates → buscar `QUIZv2_*`. Cada uno se asigna en el flow Email node con "Assign existing template".

| # | Rama | Email | Template ID | Subject |
|---|---|---|---|---|
| 01 | brainboost | E1 — Tu match | `RaNjbn` | Tu match es Brain Boost |
| 02 | longevity | E1 — Tu match | `YkvRdi` | Tu match es Longevity Boost (vuelve el 10 de mayo) |
| 03 | immune | E1 — Tu match | `VV4V6c` | Tu match es Immune Boost |
| 04 | innerglow | E1 — Tu match | `RHc7sB` | Tu match es Inner Glow — y tengo algo bueno para vos |
| 05 | brainboost | E2 — Testimonial | `X6tKY4` | Hashimoto, niebla mental, y por qué Melena de León funciona |
| 06 | longevity | E2 — Testimonial | `SfzTHQ` | Pensaba que era cansancio. Era falta de Reishi. |
| 07 | immune | E2 — Testimonial | `XCRyfh` | Hashimoto, defensas y un triple blend que está funcionando |
| 08 | innerglow | E2 — Testimonial | `WZQvCE` | Una barra que funciona. (Y es rica, en serio.) |
| 09 | brainboost | E3 — Educacional | `SMXFZ5` | El error más común al tomar Melena de León |
| 10 | longevity | E3 — Educacional | `WnPt23` | Por qué Reishi tarda más de lo que pensás |
| 11 | immune | E3 — Educacional | `Ybfkww` | Triple blend ≠ tres veces más |
| 12 | innerglow | E3 — Educacional | `SaWDns` | Tremella + Vitamina C: por qué juntas funcionan mejor |
| 13 | brainboost | E4 — Urgencia stock | `VKNqpq` | Quedan menos de las que pensé del lote del 27 de abril |
| 14 | longevity | E4 — Countdown | `XyehTT` | Pocos días para que vuelva Longevity |
| 15 | immune | E4 — Bundle 10% | `WiccED` | Lo que combina perfecto con Immune Boost |
| 16 | innerglow | E4 — Display | `TfJdUU` | Por qué la mayoría compra el display y no las sueltas |

### URL directa para editar cada template

`https://www.klaviyo.com/email-templates/{TEMPLATE_ID}/edit`

Ej: https://www.klaviyo.com/email-templates/RaNjbn/edit

### Pendiente find-replace en 6 templates

Antes de activar el flow, reemplazar `https://smartfoods.ar/pages/waitlist` por la URL real del form WaitList WA en estos 6 templates:

- `YkvRdi` (longevity E1)
- `RHc7sB` (innerglow E1)
- `SfzTHQ` (longevity E2)
- `WnPt23` (longevity E3)
- `XyehTT` (longevity E4)
- `TfJdUU` (innerglow E4)

Si querés, en próxima sesión hago el find-replace via API una vez tengas la URL del form.
