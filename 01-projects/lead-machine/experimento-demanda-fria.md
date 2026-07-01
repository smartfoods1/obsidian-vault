---
date: 2026-06-23
type: project
tags: [gondola, lead-machine, experimento, validacion, demanda-fria, storm]
status: por-correr
derivado_de: "[[storm-gondola-ingresos-jun22]]"
---

# Experimento — ¿La demanda FRÍA compra Góndola? (el gate fatal)

> Insumo de decisión del STORM (jun 22). Este es el riesgo asesino #1: si no lo corrés, todo plan financiero de Góndola descansa sobre el 5% de conversión actual, que es tráfico CÁLIDO (gente que ya te conoce). Hasta probar el frío, no sabés si tenés un producto o la agenda de contactos de Andrés con una UI.

## 1. Por qué este experimento decide todo

- El 5% de conversión free→pago de hoy viene de tibios: tu red de ex-CEO, gente que llegó por vos. Eso NO prueba demanda de mercado.
- Cuando metas tráfico pago (ads), el funnel se llena de FRÍO. Si el frío convierte a 1-2% en vez de 5%, el CAC de ads se come el ticket entero y el motor de adquisición "barato" es un mito.
- Si el frío no compra, Góndola es un servicio de relación (DFY a mano, techo cliente #8-10), no un SaaS self-serve. Cambia toda la estrategia: dejás de invertir en el funnel y doblás en el servicio.
- **Es barato y rápido de probar (3 semanas, ~$50-100k ARS). No hay excusa para construir más antes de correrlo.**

## 2. Hipótesis (falsable)

> Una marca de alimentos/suplementos en AR que NO conoce a Andrés, al toparse con Góndola por un anuncio, se registra, prueba los 5 leads gratis y compra un pack — a una tasa ≥3%.

Si es verdad: hay motor de adquisición pago, vale escalar el funnel.
Si es falso (<2%): Góndola es negocio de relación, no de self-serve. Pivote.

## 3. Diseño

**Audiencia (la clave: que sea FRÍA de verdad).** Meta Ads a dueños/marketing de marcas de alimentos funcionales, suplementos, dietética, bebidas saludables en AR, SIN ninguna conexión con Andrés/Smart Foods/Korean Root:
- Excluir: lista de tus 30 contactos del sector, seguidores de @smartfoods.ar y @specialandres, cualquier custom audience tuya.
- Targeting: intereses (suplementos, emprendedurismo gastronómico, ANMAT, venta mayorista, dietéticas), cargos (founder/dueño/comercial) si el placement lo permite. Lookalike NO (arranca de tu data = contamina con cálido). Interés + comportamiento puro.
- Geo: AMBA + principales ciudades. Edad 25-55.

**Creatividad (1 ángulo, 2-3 variantes).** Ángulo ROI directo, no "software":
- Hook: "¿Vendés un producto saludable y no tenés vendedor para meterlo en dietéticas?"
- Promesa: "Góndola te dice qué comercios de tu zona te van a comprar — y te arma la ruta. Probá gratis."
- CTA: "Probá gratis" → freemium (5 leads).
- Evitá hablar de "leads/base de datos" (suena a lista). Hablá de PDV calificados / ganar góndola.

**Landing = el freemium actual.** No construyas nada nuevo. El anuncio cae en el signup con 5 leads gratis. El onboarding tiene que dejar elegir zona/rubro rápido (si el cold-start está roto, el experimento mide el onboarding, no la demanda — arreglá eso primero o medilo aparte).

**Presupuesto:** $50.000-100.000 ARS total, 2-3 semanas. Objetivo de volumen: ~150-300 signups fríos (suficiente para que un 3% vs 1% sea distinguible; con <100 el número es ruido).

**Tracking (prerequisito técnico — el único bloqueante):** hay que poder AISLAR la cohorte fría. Mecanismo: URL dedicada con UTM (ej. `?ref=ads-frio-jun26`) que Góndola capture y guarde como `signup_source` en la cuenta. Así medís conversión de ESA cohorte separada del tráfico cálido orgánico. Si Góndola no guarda el source del signup hoy, es un fix chico y es lo primero a hacer (se conecta con la instrumentación del output: ya hay precedente con el `?ref=` del landing B2B de KR).

## 4. Métricas

**Primaria:** conversión free→pago de la cohorte fría (signups con `ref=ads-frio` que compran cualquier pack) / total signups fríos.

**Guardarraíl (para no auto-engañarte):**
- Costo por signup frío (CAC de registro).
- Activación: % de fríos que gastan los 5 leads gratis (si no activan, no es problema de precio, es de onboarding).
- Costo por pago = gasto en ads / pagos. Comparalo contra el ticket del pack ($49k-290k): ¿el CAC deja margen?

## 5. Regla de decisión (decidí ANTES de ver los datos)

| Conversión fría | Lectura | Acción |
|---|---|---|
| **≥3%** | Hay demanda de mercado self-serve | Escalá el funnel: más ads, optimizá CAC, construí recompra (#6) para LTV |
| **2-3%** | Ambiguo / depende del CAC | Mirá costo por pago vs ticket. Si el CAC cierra, seguí; si no, es marginal |
| **<2%** | NO hay demanda fría self-serve | Pará de invertir en el funnel. Góndola = negocio de relación → doblá en DFY/servicio. El unicornio queda descartado, y está bien |

## 6. Confounders a vigilar

- **Contaminación cálida:** si no excluís bien tus audiencias, parte del "frío" es tibio y el número infla. Excluí agresivo.
- **Onboarding roto ≠ demanda muerta:** si los fríos se registran pero no llegan a ver valor (cold-start: no saben qué zona buscar), medís el onboarding, no la demanda. Por eso el guardarraíl de activación.
- **Volumen insuficiente:** con <100 signups, 3% vs 1% es indistinguible. Bancá el presupuesto hasta tener N suficiente o no corras conclusiones.
- **Atribución:** el pago puede tardar días post-signup. Dale una ventana de 14 días antes de cerrar el número.

## 7. Secuencia (3 semanas)

1. **Días 1-2:** fix de `signup_source` por UTM (si falta) + armar la URL con `?ref=ads-frio-jun26`.
2. **Días 2-4:** crear las 2-3 creatividades + el público frío con exclusiones.
3. **Días 4-18:** correr ads, $50-100k, monitorear CAC de signup y activación a mitad de camino (ajustar creatividad si el CTR es malo, NO el experimento).
4. **Días 18-21:** ventana de atribución, calcular conversión fría aislada, aplicar la regla de decisión.

## 8. Relación con los otros frentes

- Este experimento valida (o mata) el **stream #1 (packs self-serve)** y, por extensión, toda la tesis de "motor de adquisición barato".
- El **#6 (recompra)** y la **instrumentación del output** (ya desplegables) son lo que convierte un pago único en LTV — son la diferencia entre "el frío compra una vez y chau" y "negocio". Corré este experimento en paralelo a tenerlos prendidos.
- Si el frío valida Y la recompra funciona, recién ahí la conversación venture (riel #5) tiene base.
