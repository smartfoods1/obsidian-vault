---
date: 2026-06-22
type: brand-manual
tags: [gondola, lead-machine, marca, identidad, b2b]
status: activo
derivado_de: workflow multi-agente (5 direcciones → jurado 3 lentes → síntesis → QA)
---

# Góndola — Manual de Marca

> Identidad de la app de prospección B2B, antes "Lead Machine". Generada por panel de
> direcciones + jurado (estrategia / craft UI-UX / ingeniería de diseño) + síntesis + QA.
> **Assets SVG** en el repo: `~/lead-machine/brand/` (mark, mark-white, app-icon, lockup).
> **Tokens ya aplicados** en `webapp/src/index.css`. Implementado local el 2026-06-22 (deploy aparte).

---

## 1. Esencia y posicionamiento

**Esencia:** ganar góndola, sin fricción.

**Qué es Góndola:** app SaaS freemium de prospección B2B que encuentra y **califica** clientes mayoristas (dietéticas, almacenes naturales, naturistas) para marcas de alimentos funcionales y suplementos en Argentina. Scrapea Google Maps, enriquece con IA, arma la ruta de venta y un CRM de seguimiento (contactar → vender).

**Posicionamiento:** Góndola NO te da una lista cruda. Te dice **qué comercio merece tu producto** y te arma la ruta para entrar al canal. El valor es **calificar** (señal, no volumen) y **matar la fricción comercial** del contactar al vender. Premium/Tier-1 pero de calle: herramienta de laburo que te hace ganar plata.

**A quién le habla:** dueños de marcas de alimentos/suplementos, comerciales de calle, sales managers. Gente práctica que vende en territorio y vive en WhatsApp.

---

## 2. Historia del nombre

**Góndola** = el estante/exhibidor del supermercado donde las marcas pelean el espacio. Doble sentido propietario: la góndola es el **estante físico** *y* el **canal retail**. El producto ayuda a las marcas a **ganar góndola** (entrar al canal mayorista y quedarse con el lugar que convierte).

El acento ortográfico — **Góndola**, sentence-case con tilde — es identidad: reivindica el español argentino frente al logotipo anglo en mayúsculas. Ningún SaaS de stock tiene tilde en el wordmark.

---

## 3. Paleta

Reemplaza el índigo SmartBrain de stock por un **verde-almacén profundo** + **ámbar de tienda**: aterriza la marca en el mundo retail saludable que el usuario respeta, lejos del SaaS-by-default.

| Token | Hex | Uso |
|---|---|---|
| `--color-brand` | `#1F6B45` | Primario. CTAs, estados activos, la estructura del mark. White encima = 6.47:1 (AA). |
| `--color-brand-strong` | `#124A33` | Hover/variante oscura **y texto sobre brand-tint**. Sobre blanco = 10.23:1 (AAA); sobre tint = 9.09:1 (AAA). |
| `--color-brand-tint` | `#EAF4ED` | Fondo MUY claro (L=0.883) de chips/tabs activos. Encima va brand-strong. |
| `--color-accent` | `#E0A52E` | Ámbar. **Solo no-textual**: la tapa del producto destacado, badges, puntos. 2.19:1 → NUNCA texto. |
| `--color-ink` | `#15231C` | Texto principal. Sobre blanco = 16.29:1. |

**Superficies (se mantienen):** `--color-page #f8fafc`, `--color-surface #ffffff`, `--color-subtle #f1f5f9`, líneas `#e2e8f0`/`#cbd5e1`, texto soft `#475569` / faint `#94a3b8`.

**Regla dura:** el ámbar es un acento de *significado* (el lugar ganado), no decoración, y jamás texto.

---

## 4. Tipografía

Split intencional, las dos familias self-hosted vía `@fontsource-variable` (sin CDN):

- **Wordmark + headings → Space Grotesk** (`@fontsource-variable/space-grotesk`, weight 600, tracking -0.02em). Carácter geométrico, 'g' de doble panza; le da firma técnica al nombre.
- **UI densa → Manrope** (`@fontsource-variable/manrope`, 400/500/600/700). Humanista-geométrica, más nítida que Inter en tablas/KPIs/chips a 13-14px. Números tabulares (`.nums`) para grillas de score/reseñas/precios.

El theme expone `--font-sans` (Manrope) y `--font-display` (Space Grotesk).

---

## 5. Logo

**Concepto:** el mark abstrae una **góndola vista de frente**: dos rieles horizontales (base + techo) que cierran el mueble, con una fila de productos parados encima. Un producto **rompe la fila** — es más alto y lleva una **tapa en ámbar**: es el destacado, la marca que **ganó el espacio premium**. Los rieles son lo que separa este mark de un bar-chart de growth: la silueta es inconfundiblemente un exhibidor.

**Construcción:** geometría 100% pura (rects redondeados snapeados a grilla), sin `<text>`. Estructura en `currentColor` / `var(--color-brand)`; la tapa del destacado en `var(--color-accent)`. Themeable y nítido a 16px. (QA corrigió la geometría: el producto alto frena 0.5px bajo el riel superior para no empastar a tamaño chico.)

**Reglas:**
- **Mark solo** → favicon, app icon, avatar, badges, espacios cuadrados/reducidos (≥16px).
- **Lockup** (mark + 'Góndola') → header, login, landing, propuestas, firmas, decks (≥120px de ancho).
- **Clearspace** → ≥ la altura riel-a-riel del mark alrededor del lockup; ≥25% del lado en el mark solo.
- **Wordmark** → siempre Space Grotesk 600, sentence-case con tilde, color ink.

---

## 6. Voz y tono

Español argentino, **voseo**. Directo, claro, estratégico — sin rodeos. Premium pero cercano: "herramienta de trabajo que te hace ganar plata". Hablás de **resultados** (ganar góndola, entrar al canal, el comercio que encaja), no de features ("leads", "datos crudos"). Confrontás el cliché del competidor mental ("base de datos / lista de dietéticas") con criterio: calificás, no listás.

**Tagline:** *Ganá la góndola: el comercio justo, en tu zona, listo para vender.*

---

## 7. Do / Don't

**Hacé**
- Mark en currentColor + tapa en `--color-accent` (themeable, light/dark).
- Wordmark sentence-case con tilde: **Góndola**.
- Ámbar solo para el destacado, badges y puntos.
- brand-strong para texto sobre tint; ink para texto principal.
- Variante favicon de 3 productos + 2 rieles (robusta a 16px).

**No hagas**
- Índigo de stock, gradientes, blobs, flechita de growth, check genérico.
- Pintar todo el producto de ámbar o usar ámbar en texto (falla WCAG 2.19:1).
- Wordmark en MAYÚSCULAS ni sin tilde ('GONDOLA' / 'Gondola').
- Quitar los rieles (sin ellos se lee como bar-chart — el cliché a evitar).
- Sustituir Space Grotesk por Inter en el wordmark.
- Rotar, inclinar, estirar o sombrear el mark.

---

## 8. Contraste (WCAG, verificado)

| Par | Ratio | Nivel |
|---|---|---|
| white sobre `--color-brand` | 6.47:1 | AA (botones/CTAs) |
| `--color-brand-strong` sobre white | 10.23:1 | AAA (texto/links/headings) |
| `--color-brand-strong` sobre tint | 9.09:1 | AAA (chips/tabs activos) |
| `--color-ink` sobre white | 16.29:1 | AAA |
| `--color-accent` sobre white | 2.19:1 | ✗ → uso exclusivo no-textual |

---

## Por qué esta dirección (consenso del jurado)

Ganó entre 5 direcciones: 2 de 3 jueces la coronaron (el juez técnico le dio 45/45, el más alto del set). Es la única donde nombre + mark + tagline + color cuentan **una sola historia propietaria** ("ganar góndola") sin pie de foto. Injertos aplicados: chasis de producción robusto (favicon a 16px), la tapa de acento en vez de pintar todo de ámbar, y el split tipográfico Space Grotesk + Manrope. Descartes: el pin (cliché), el monograma "G" (contraste al filo, metáfora se pierde chica), la jerarquía por opacidad (se desvanece a 16px).
