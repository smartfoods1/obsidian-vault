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
(link al form Klaviyo con phone field)

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

Si preferís esperar al extracto (sin fecha confirmada todavía), dejame tu WhatsApp:
[link sutil: AVISAME CUANDO VUELVA → form WA]

Andy

---

## Email 2 (Día 2) — Testimonial específico

> Estructura común; bullets por rama.

**Subject genérico:** "Lo que me dijo {{ nombre cliente real }}"
**Preview:** Tarda dos semanas. Pero cuando arranca, no parás.

**Hero**: foto cliente real (no stock) + 2 líneas de quote
**Body**: 3-4 párrafos, primera persona del cliente
**CTA**: 1 link al producto match

| Rama | Quote sugerido (a llenar con review real Klaviyo o IG) | Foco |
|---|---|---|
| brainboost | "Antes leía un mail dos veces para entenderlo. Hoy le presto atención al primer renglón." | Foco/memoria laboral |
| longevity | "Dormía 8 horas y me levantaba molida. Ahora con 7 me siento descansada." | Sueño/cortisol |
| immune | "Cuatro inviernos sin gripe. Yo no lo creía hasta que mi hija sí se enfermó y yo no." | Defensas |
| innerglow → Glow barrita | "Me hice fan de la barrita. Es la merienda y un boost de colágeno al mismo tiempo." | Practicidad + skin |

**Acción Andy**: revisar reviews reales en Shopify/IG comments para extraer quotes textuales. Mejor que inventar.

---

## Email 3 (Día 5) — Cómo tomarlo / Ciencia

> Educacional. Refuerza la elección. Bajísimo CTR esperado pero alto impacto en conversión final.

**Estructura común:**
1. Hero text: "El error más común al empezar con {{ producto }}"
2. 3 puntos: cómo tomarlo, cuándo notarlo, qué evitar
3. CTA al producto

| Rama | Subject | Punto educacional clave |
|---|---|---|
| brainboost | El error más común al tomar Melena de León | Tomarlo solo a la mañana (no de noche, dispara cognición) |
| longevity | Por qué Reishi tarda más de lo que pensás | 21 días mínimo para cortisol; constancia > dosis alta |
| immune | Triple blend ≠ tres veces más | Sinergia entre Reishi-Shiitake-Maitake, no aditivo |
| innerglow → Glow barrita | Tremella + colágeno endógeno: cómo activarlo | Vitamina C (la barrita ya la trae) potencia absorción |

---

## Email 4 (Día 10) — Soft offer / Urgencia

> Cierre del flow. Por rama distinto. NO inventar descuentos sin autorización Andrés — usar urgencia/stock real o bundle natural.

| Rama | Mecánica | Subject |
|---|---|---|
| brainboost | "Quedan X unidades del lote del 27/4" (stock real, urgencia honesta) | El lote nuevo se va más rápido de lo que pensé |
| longevity | Countdown a 10 mayo + reminder waitlist | Faltan {{ días }} para que vuelva. Ya hay {{ X }} esperando. |
| immune | Bundle natural: Immune + Cafe Full Blend (10% off por bundle, requiere autorizar) | Lo que combina mejor con Immune Boost |
| innerglow | Glow barrita display 12u vs 6u (bundle). Reforzar capture WA waitlist | Tu cuerpo ya pide colágeno. Acá está. |

**Decisión pendiente Andrés**: ¿autorizar bundle 10% off Immune + Cafe? Si no, usar mismo modelo que brainboost (urgencia stock).

---

## Captura WhatsApp — Form Klaviyo (resuelve C)

**Objetivo**: capturar phone para futuros leads + backfill de los 401 actuales (especialmente innerglow + longevity OOS).

### Form nuevo Klaviyo

- **Nombre interno**: WaitList WA — Quiz
- **Tipo**: Embedded form / Pop-up trigger por click en CTA del email
- **Campos**:
  - email (prefilled / hidden)
  - phone (`+54 9 11 ...` formato)
  - quiz_adaptogeno_origen (hidden, prefilled desde profile property)
- **Confirmation**: "Listo. Te aviso por WhatsApp apenas entra stock."
- **Lista que sumar**: nueva lista "WaitList WA" + tag `waitlist:{{ quiz_adaptogeno }}`

### Modificación quiz form actual (TL7XrF)

Agregar campo phone OPCIONAL al final del quiz. No requerido para no bajar conversion.

Copy del campo:
> "¿Querés que te avise por WhatsApp cuando salga tu adaptógeno o tengamos novedades? (opcional)"

Esto resuelve los **futuros** leads que entren al flow. No los 401 actuales.

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

1. **Autorizar/rechazar bundle 10% off Immune + Cafe Full Blend** (Email 4 immune)
2. **Conseguir reviews/quotes reales** para Email 2 (Shopify reviews + IG comments)
3. **Cargar el flow en Klaviyo** siguiendo paso 1-5 arriba (estimado: 4-6h de trabajo)
4. **Decidir cuándo activar**: idealmente coordinar con entrada de stock Brain Boost (27/4)
5. **Decidir si modificar quiz form actual** para capturar phone (sesión aparte)

---

## Próximos pasos (sesión siguiente)

- Modificar form quiz Klaviyo TL7XrF para capturar phone (resuelve C para nuevos leads)
- Pausar UgXAZD (actual placeholder) usando revision API correcta — error 404 en revision 2024-10-15, probar revisions más recientes (2025-04-15+)
- Si Andrés activa flow v2: monitorear primeras 48h y ajustar
