---
date: 2026-06-18
type: design
tags: [deerflow, smartbrain, b2b, crm, outreach, multitenant]
status: propuesta
derivado_de: project_deerflow_smartbrain
---

# Caso de uso DeerFlow #2 — Motor de Inteligencia de Cuentas B2B

> Segundo caso para DeerFlow conectado a Smart Brain. Forma distinta al café: en vez de un
> research one-shot, es **fan-out sobre cientos de ítems en paralelo**, recurrente y multi-tenant.
> Relacionado: [[deerflow-sprint-cafe]] · [[project_kr_smartfoods_channel_overlap]] · [[b2b-core-auditoria]]

## El problema
Tenés **665 prospectos B2B** en el CRM. Con el conector confirmé en vivo: **276 con score ≥70 y
274 con info webeable** (nombre, dirección, IG/sitio, rating, etapa, tipo). Hoy esos leads se
scorean (Places API) pero **no hay un dossier por cuenta ni un ángulo de pitch personalizado** —
se hace a mano o no se hace. Y SF + KR **comparten el mismo canal** (dietéticas/naturistas AR),
así que el laburo sirve para las dos marcas.

## Por qué DeerFlow (y no SmartBrain solo)
SmartBrain ya scorea y lista. Lo que NO hace: **investigación profunda multi-fuente por cuenta**
+ síntesis + mensaje personalizado, a escala. Eso es la forma nativa de DeerFlow: **un sub-agente
por cuenta, en paralelo**, cada uno con su contexto y herramientas.

## Qué hace DeerFlow por cada cuenta
1. **Input** (del conector): lead con nombre, dirección, IG/sitio, rating/reviews, etapa, tipo.
2. **Enriquecimiento** (sub-agente): Google Maps/Places (reviews, rating, horarios, nº sucursales) +
   scrap de IG/sitio → determina **surtido** (¿venden funcionales/adaptógenos/marcas premium?),
   **público**, **tamaño**, **qué competencia ya tienen en góndola**, **decision-maker** y **tono**.
3. **Output por cuenta**: mini-dossier + *fit score* cualitativo + **ángulo de outreach
   personalizado** + primer mensaje sugerido (respetando las reglas de plantilla WA — una línea,
   sin saltos; ver [[wa-template-rules]] equivalente).

## Mapa a las tools del conector
| Paso | Tool / fuente | Para qué |
|------|---------------|----------|
| Lista + filtros | `b2b_leads(etapa, zona, score_min)` | Traer el lote (ej. 20 hot de una zona) |
| Detalle | `smartbrain_get("/api/crm/leads/{id}")` + `/interactions` + `/wa-status` | Historial, ventana WA, secuencia |
| Personalización | `brand_context` (brand_id=smart-foods **o** korean-root) | Adaptar el pitch al diferencial de cada marca |
| Enriquecimiento | DeerFlow + Places/IG/sitio | Lo que SmartBrain no trae: research profundo por cuenta |

## Entregable
Por lote: **set de dossiers + cola de outreach priorizada**. Se puede escribir de vuelta al CRM
(nota/secuencia vía endpoint de SmartBrain) o exportar. Repetible cada vez que entran leads nuevos.

## Ejemplo trabajado (cuenta real, en vivo)
**Árima — Tienda Natural** · score 95 · Núñez · Washington 3890 · IG @arima.tiendanatural ·
etapa: primer_contacto · tipo: dietética.
Plantilla de dossier que DeerFlow llenaría: surtido y marcas que vende · ¿ya tiene café funcional/
adaptógenos? · ticket/público · reviews y reputación · decision-maker · **ángulo** (ej. "suman la
única línea con ANMAT a una góndola que ya vende funcionales") · primer mensaje WA.
*Nota honesta:* el search genérico no alcanza para esto (probado: "Árima" devuelve dietéticas
genéricas). El engine real combina Places + IG + sitio — exactamente la tarea multi-paso por ítem
de DeerFlow.

## Multi-tenant / monetización
- **SF + KR**: un solo motor sirve ambas marcas cambiando `brand_id` (canal compartido).
- **Content Hub**: "Inteligencia de cuentas B2B as a service" — entregable premium recurrente para
  cualquier marca que venda mayorista. Diferencia el Hub de "te genero posts".

## ROI / la vara
274 cuentas webeables × dossier + outreach personalizado vs. el pitch genérico actual. Si el output
mejora la tasa de conversión del primer contacto, paga el VPS solo. Y a diferencia del café
(one-shot), este caso es **recurrente** → amortiza la infra.

## Otros casos en cola (para no casarse con uno)
- **Auditoría estratégica trimestral** (SF/KR): data interna + benchmarks de industria → informe.
- **Research de categoría grounded para KR** (monoproducto, hoy alucina sin grounding).
- **Vetting profundo de influencers** (autenticidad de audiencia, fit, banderas rojas).
