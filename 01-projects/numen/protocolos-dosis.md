---
date: 2026-08-07
type: protocolo
tags: [numen, luz-roja, fotobiomodulacion, dosis, producto]
status: activo
derivado_de: "[[research-competencia]]"
---

# NUMEN — Protocolos de dosis

Tabla operativa por objetivo. Cubre el **Hueco 3** del [[research-competencia|research competitivo]]: ninguna marca de la categoría publica "para tu objetivo, a X cm, Y minutos, Z veces por semana, y este es tu J/cm²".

Alimenta tres cosas: la respuesta comercial por WhatsApp, la tabla de dosis de la app companion (el moat declarado del MVP) y el pilar de contenido "el instrumento".

## La cuenta base

```
Fluencia (J/cm²) = Irradiancia (mW/cm²) × segundos ÷ 1000
```

NUMEN: **40 mW/cm² medidos a 30 cm** → **2,4 J/cm² por minuto**.

| J/cm² | Tiempo a 30 cm |
|---|---|
| 1 | 0:25 |
| 2 | 0:50 |
| 3,8 | 1:35 |
| 5 | 2:05 |
| 8 | 3:20 |
| 10 | 4:10 |
| 15 | 6:15 |
| 20 | 8:20 |
| 30 | 12:30 |
| 40 | 16:40 |
| 48 | 20:00 ← techo |

## Protocolos por objetivo (a 30 cm)

| Objetivo | Dosis | Minutos | Frecuencia | Horizonte | Fuerza de evidencia |
|---|---|---|---|---|---|
| Rostro — arrugas, textura | 3–6 J/cm² | 1:15 – 2:30 | 3–5×/sem | 4–12 sem | **Alta** (RCT humano) |
| Piel corporal — calidad, cicatrices | 4–10 J/cm² | 1:40 – 4:10 | 3–5×/sem | 8–12 sem | Media |
| Mantenimiento general | 8–14 J/cm² | 3:20 – 6:00 | 4–6×/sem | continuo | Media |
| Recuperación muscular | 15–30 J/cm² | 6:15 – 12:30 | 3–5×/sem, post-entreno | 4–8 sem | **Baja a moderada** (declarada por los propios autores) |
| Zona profunda (rodilla, hombro, lumbar) | 20–40 J/cm² | 8:20 – 16:40 | 3–4×/sem | 6–8 sem | **Baja** — mayor riesgo de claim |

**Rampa de entrada:** primeras 2–3 semanas arrancar en 1–2 min y subir progresivamente hasta el objetivo (formato JOOVV).

## Reglas transversales

1. **Techo por sesión: 20 min a 30 cm** = 48 J/cm², justo debajo del <50 J/cm² que GembaRed fija como tope. La respuesta es bifásica: pasado el umbral, se aplana o se invierte.
2. **Máximo 2–3 zonas por día** (PlatinumLED). Dos sesiones el mismo día → **6 h de separación** (Rouge).
3. **La misma dosis a distinta potencia no da el mismo resultado.** Hamblin 2011: 670 nm a 4 mW/cm² × 1.250 s funcionó; los mismos 5 J/cm² a 15 mW/cm² × 333 s perdieron el efecto. Nadie puede acercarse al panel para "hacer lo mismo en menos tiempo".
4. **Constancia por encima de intensidad.**
5. **Seguridad:** no mirar los LEDs (850 nm invisible, sin reflejo pupilar protector). Consulta médica previa con medicación fotosensibilizante, embarazo, tratamiento oncológico o condiciones oculares.

## Límites honestos de esta tabla

- **Solo vale a 30 cm.** Es el único punto medido. En campo cercano un array de 16 LEDs no sigue la ley del cuadrado inverso → cualquier extrapolación a 10/15/20/45 cm es invento. **Bloqueante abierto.**
- **Instrumento sin confirmar.** Si los 40 mW/cm² se midieron con solarímetro, corresponde el factor 0,40–0,45 (multiplicador publicado por Mito Red) y toda la tabla se corre.
- **Uniformidad no medida.** Haz de 20°, array de 33×11 cm. Los minutos aplican al centro; los bordes reciben menos. Falta el isoplot.
- Los rangos musculoesqueléticos vienen de literatura mayormente con láser puntual, donde la dosis por punto no traduce limpio a J/cm² de panel.

## Claims

Nivel 1–2. **Prohibido:** "grado médico", "clínicamente probado", claims de tratamiento, cognitivos, metabólicos o de quema de grasa. La evidencia cognitiva (Jeffery/Huberman, 670 nm) es transcraneal y **no transfiere** a panel corporal.

## Fuentes

- Huang, Sharma, Carroll & Hamblin — *Dose-Response* 2011, PMC3315174. Curva de Arndt-Schulz: fibroblastos máx. 0,88 J/cm², reducido a 8,68. *"Too much power density and/or time may have inhibitory effects."*
- Mota et al. 2023 — PMID 36780572. RCT split-face, 137 mujeres 40–65 años, 10 sesiones en 4 semanas, 660 nm a 3,8 J/cm², −31,6% volumen de arrugas perioculares.
- Vanin et al. 2018 — PMID 29090398. Revisión sistemática, rendimiento y recuperación muscular, *"very low to moderate quality of evidence"*.
- Celluma — ventana terapéutica ~2–10 J/cm².
- Mito Red — 4–12 J/cm² piel, 20–50+ musculoesquelético; fórmula de fluencia; factor de corrección de solarímetro 0,40–0,45.
- GembaRed — 1–10 J/cm² superficial, 10–50 profundo, 8–14 diario, tope <50; máx. 2×/día, 20 min por sesión, 2–5×/semana.
- PlatinumLED — 10–20 min por zona, máx. 2–3 zonas/día, 3–5×/semana.
- Rouge — mínimo 3×/semana, 6 h entre sesiones del mismo día.
- JOOVV — escalar de 1–2 a 10 min en 2–3 semanas.

Relacionado: [[index]] · [[research-competencia]] · [[estrategia-contenido]]
