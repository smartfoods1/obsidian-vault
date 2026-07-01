---
date: 2026-06-11
type: estrategia
tags: [findemes, instagram, marketing, viral, juego]
status: activo
---

# FIN DE MES — Estrategia creativa Instagram

> Juego: [findemes.com.ar](https://findemes.com.ar) — el kiosco contra la economía argentina.
> Assets generados en `~/kiosco-argento/marketing/` (logo + 3 piezas + HTMLs editables).

## Big idea

**"El simulador de algo que ya vivís todos los días."**

FIN DE MES no compite con otros juegos: compite con la catarsis argentina. La cuenta no habla de un juego, habla de la experiencia argentina de llegar (o no) a fin de mes — y el juego es el punchline. Cada dolor económico real (inflación, blue, alquiler, fiado, tarifazo) es un meme jugable.

Tagline de marca: **REMARCÁ O MORÍ**.

## Posicionamiento de la cuenta

- No es una cuenta de gaming. Es una cuenta de **humor económico argentino** que tiene un juego.
- Tono: kiosquero canchero. Voseo, ironía afilada, cero lástima. Tipo el grupo de WhatsApp del barrio.
- Regla de oro: **nunca explicar el chiste, nunca bajar línea política**. La inflación es el villano del juego, no de un partido.

## Loops virales (en orden de potencia)

1. **Desafío diario** (ya existe en el juego): misma economía para todos, resultado compartible estilo Wordle (🟩🟩🟩⬜). Post diario/template con el "kiosquero promedio de hoy" → FOMO de ganarle al promedio.
2. **Share del resultado**: el juego ya genera texto + tarjeta 1080. Pedir explícitamente en cada caption: "subí tu resultado a stories y etiquetanos, reposteamos los mejores y los peores".
3. **Muro de la vergüenza / salón de la fama**: stories destacadas con los que fundieron en 2 meses y los que aguantaron 24. La derrota es más compartible que la victoria.
4. **Duelos**: retar por comentarios ("etiquetá al amigo que remarca la birra antes que vos"). Cada pieza termina con una pregunta etiquetable.
5. **Newsjacking económico**: cada dato real (INDEC, blue, tarifas) es un post en menos de 24h: "La inflación de mayo fue X%. En FIN DE MES eso es un martes."

## Pilares de contenido (mix semanal)

| Pilar | % | Formato | Ejemplo |
|---|---|---|---|
| Humor jugable (eventos del juego como memes) | 40% | carrusel / estática | "POV: tenés un kiosco en Argentina" |
| Desafío diario + resultados de la comunidad | 30% | estática template + stories | "Desafío #27 — ¿le ganás al promedio?" |
| Newsjacking económico | 15% | estática rápida | dato real vs. el juego |
| Behind the game / founder | 15% | reel hablado | "Hice un juego donde el jefe final es el alquiler" |

## Reels (cuando arranque video)

- Screen-recording del juego + voz: "Día 1: tengo un kiosco. Día 90: debo el alquiler" (formato storytime).
- "Le di mi kiosco a mi vieja/mi amigo economista/un español" — reacciones jugando.
- Velocidad: "¿En cuántos minutos fundís un kiosco?" challenge.

## Plan de lanzamiento (2 semanas)

- **Día 1**: Post 1 (lanzamiento) + bio + destacadas "Cómo se juega".
- **Día 2**: Carrusel POV (pieza 2) — el post diseñado para compartir.
- **Día 3**: Desafío diario (pieza 3) — arranca el ritual. De acá en adelante, el template del desafío sale 3x/semana.
- **Días 4–14**: alternar pilares. Repostear TODO resultado que la gente comparta (al principio, aunque sean 2). Comentar desde la cuenta en posts de cuentas de economía/memes (Ámbito, El Gato y la Caja de la economía: @ahorroinvertí, etc.) con personalidad de kiosquero.
- Semana 2: primer reel founder-led + buscar 3 micro-cuentas de memes económicos para colaboración/seeding (mandarles el link del desafío, no pedirles nada).

## Bio de Instagram

**Opción A (recomendada):**
```
🏪 El juego del kiosco contra la economía argentina
🔥 Inflación, dólar blue y el alquiler que ajusta
🏆 Desafío diario: ¿cuántos meses aguantás?
👇 Jugá gratis
```

**Opción B (más corta/punchy):**
```
🏪 Remarcá o morí
El juego de llegar a fin de mes en Argentina 🇦🇷
Desafío nuevo todos los días 👇
```

Nombre del perfil (campo "nombre", es buscable): `FIN DE MES 🏪 | Juego argentino`

## Captions de las 3 piezas

**Post 1 (lanzamiento):**
> Hicimos un juego sobre la cosa más difícil de la Argentina: llegar a fin de mes.
> Manejás un kiosco. La inflación remarca, el blue salta, el alquiler ajusta y el vecino pide fiado.
> ¿Cuántos meses aguantás? Jugá gratis 👉 link en bio
> #findemes #kiosco #inflacion #juegoargentino #dolarblue

**Post 2 (carrusel POV):**
> Todo lo que pasa en este carrusel pasa en el juego. Y en tu vida. 🫠
> Etiquetá a ese amigo que tiene alma de kiosquero 👇
> Jugá gratis en findemes.com.ar (link en bio)

**Post 3 (desafío diario):**
> Desafío de hoy: la misma economía para todos, una sola chance.
> El kiosquero promedio aguantó 13 meses. ¿Le ganás?
> Subí tu resultado a stories y etiquetanos — reposteamos los mejores (y los peores 🪦)

## Hashtags base

`#findemes #juegoargentino #inflacion #dolarblue #kiosco #memesargentinos #economiaargentina #humorargentino` — rotar, máx 8 por post.

## KPIs primeras 4 semanas

- Shares por post (la métrica que importa, no likes)
- Jugadas con `?ref=` desde IG (ya trackeado en el backend)
- % de jugadores del desafío diario que vuelven al día siguiente

## Assets

| Archivo | Uso |
|---|---|
| `marketing/logo.png` | Avatar IG (1080×1080, legible en círculo) |
| `marketing/post1_lanzamiento.png` | Post 1 estática |
| `marketing/post2_slide1..6.png` | Post 2 carrusel 6 slides |
| `marketing/post3_desafio.png` | Post 3 template desafío (editar # en el HTML y re-renderizar) |

Los `.html` son la fuente: editar texto → re-render con Chrome headless (comando en el repo).
