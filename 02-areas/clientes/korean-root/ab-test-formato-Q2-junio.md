---
date: 2026-06-07
type: plan-experimento
tags: [korean-root, email, ab-test, formato, smartbrain]
status: en-revision
cliente: The Korean Root
---

# A/B Test de Formato — Email KR — Q2 Junio 2026

## Por qué
El equipo cree que el texto plano performa mejor, pero **es percepción, no dato**: KR nunca mandó emails con imágenes (las 266 campañas en Perfit eran todas texto plano). En vez de discutir opiniones, medimos. El test resuelve el debate con evidencia y, de paso, nos dice si hay un problema de **deliverability** con el formato nuevo.

## Hipótesis (medimos las dos)
- **Engagement:** el formato visual (imágenes + botones) sube el **CTOR** (clics sobre aperturas) vs texto plano.
- **Deliverability:** con el mismo asunto, si el texto plano abre más, es porque entra mejor a la bandeja (esquiva Promociones). El open rate, a igual asunto, mide entregabilidad del formato.

## Variantes — única variable: el formato
| | A — Visual | B — Texto plano |
|---|---|---|
| Cuerpo | Imágenes de producto + botones + header/footer | Markdown simple, sin imágenes, link de texto (el render anterior) |
| Todo lo demás | **Idéntico**: mismo asunto, preheader, copy base, segmento, horario, oferta | **Idéntico** |

Si cambia algo más que el formato, el test no sirve (no sabés qué causó el resultado).

## Diseño
- **Split 50/50 aleatorio** del segmento por cada pieza. **Misma persona = misma variante** toda la quincena (no re-aleatorizar, para no contaminar).
- **Volumen:** 3 emails/semana × 2 semanas = **6 piezas**. Sobre el segmento grande (~13.500 → ~6.750 por variante).
- **Cap de 3/semana por contacto** (anti-blasting recién definido) — el test vive adentro de ese límite.
- **Tracking:** `utm_content=img` vs `=plain` + GA + Perfit, para leer limpio por variante.
- El split y las 2 campañas por pieza las maneja el Smart Brain (genera A y B a las dos mitades).

## Qué puede concluir el test (poder estadístico real, no impresión)
| Métrica | Qué mide | 1 pieza | 6 piezas acumuladas | Veredicto |
|---|---|---|---|---|
| **CTOR** (primaria) | Engagement del formato | ±1,57 pp | **±0,64 pp** | Concluyente (esperamos +1,5pp: amplio) |
| **Open rate** (secundaria) | Deliverability del formato | ±1,7 pp | **±0,68 pp** | Concluyente |
| Conversión | Ventas | — | ±17 pp | **NO concluyente** — solo direccional |

> Clave: el test **se juzga por CTOR + open**, no por ventas. La conversión de KR es de ~2 por campaña → con 6 piezas partidas no hay eventos suficientes para concluir sobre revenue en 2 semanas. Si el equipo lo juzga por "cuál vendió más", el ganador va a ser azar.

## Criterio de decisión (acordado ANTES de arrancar)
1. **Visual gana CTOR** con significancia y el open no cae >2pp → **adoptar formato visual**.
2. **Texto plano gana open** con significancia **y** Visual no mejora CTOR → el problema es **deliverability** del formato → adoptar plano o arreglar entregabilidad (peso del HTML, ratio texto/imagen, autenticación).
3. **Empate en CTOR** → gana el de mejor open (probablemente plano).
4. **Conversión** → desempate direccional, nunca juez.

## Lectura y entregable
Al cierre de la quincena: comparar A vs B por variante (open, CTOR, clics, conversión direccional) con test de proporciones. Reporte de 1 página con ganador + recomendación de formato definitivo.

## Qué construye el Smart Brain
1. Variante B = renderer de texto plano como opción del builder (recuperar el `_md_to_html` previo).
2. Split 50/50 aleatorio + persistencia de variante por contacto durante la quincena.
3. 2 campañas por pieza (A/B) con UTM diferenciado.
4. Lectura por variante (query / mini-reporte de resultados).
5. **Cap de 3/semana por contacto** (anti-blasting) — se implementa en la misma tanda.

## Riesgos / honestidad
- Conversión no medible en 2 semanas — no venderlo como "test de ventas".
- Deliverability puede mover el open independiente del contenido — por eso medimos ambos por separado.
- Si el segmento usado es más chico que ~13.500, el MDE sube (test menos sensible). Para máxima señal, correr el A/B sobre el segmento más grande disponible.

Relacionado: [[resumen-ejecutivo-email-2026]], [[motor-retencion-360]].
