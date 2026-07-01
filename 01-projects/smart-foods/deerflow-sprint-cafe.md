---
date: 2026-06-18
type: design
tags: [deerflow, smartbrain, cafe, relanzamiento, research, agentes]
status: propuesta
derivado_de: project_deerflow_smartbrain
---

# Sprint DeerFlow #1 — Relanzamiento Café Melena de León

> Primer caso real para validar si un agente autónomo (DeerFlow) conectado a Smart Brain
> vía MCP justifica dedicar un VPS. **Sin gastar todavía**: este doc es el diseño; la corrida
> se puede prototipar gratis (ver §7).

Relacionado: [[estrategia-relanzamiento-cafe-melena]] · [[fichas-meli-cafe-anmat-safe]] ·
[[teardown-smush-relanzamiento-cafe]] · [[fuentes-mushroom-coffee-research]]

---

## 0. Por qué este caso primero
- Proyecto activo con meta concreta: **USD 25k/mes** y decisión de relanzamiento inminente.
- Mezcla exactamente lo que DeerFlow hace bien y SmartBrain no: **research externo multi-fuente
  (mercado, competidores, claims) + ejecución (P&L en sandbox) + artefacto largo**, todo
  **anclado en tu data propia** vía el conector MCP.
- Sirve de **vara**: si el dossier sale accionable sin rehacerlo, justifica el VPS y meterlo
  como entregable premium del Content Hub para otros clientes.

## 1. Objetivo del sprint (qué decisión sirve)
Producir un **dossier de relanzamiento** que responda, con evidencia:
> ¿Con qué **posicionamiento, precio, claims, bundle, canales y mensajes** relanzamos el café
> para encarar los USD 25k/mes, y el **P&L** cierra?

## 2. Lo que haría DeerFlow (workstreams → sub-agentes)
DeerFlow descompone la tarea y spawnea sub-agentes en paralelo:

| # | Workstream | Qué investiga | Fuente |
|---|-----------|---------------|--------|
| A | **Mercado & demanda** | Tamaño/crecimiento del mushroom coffee en AR/LATAM, tendencias de búsqueda, estacionalidad, willingness to pay | Web |
| B | **Competencia** | Mapa de players AR (Rytual Café y resto) + la **marca-espejo "Smart Coffee"**: pricing, formatos, claims, posicionamiento, share of voice | Web + MCP |
| C | **Regulatorio & diferencial** | Claims permitidos ANMAT/INAL para café con hongos; cómo blindar el diferencial **beta-glucanos + ANMAT** vs competidores sin registro | Web + MCP |
| D | **Data propia & baseline** | Ventas/márgenes reales del café, afinidad/cross-sell con extractos, ICP; **flagear gaps de data** | MCP |
| E | **Síntesis & P&L** | Posicionamiento + precio + bundle + canales + mensajes; **P&L** que modele el camino a 25k con supuestos explícitos (código en sandbox) | DeerFlow |

## 3. Mapa concreto a las tools del conector (brand_id=smart-foods)
| Workstream | Tool MCP | Para qué |
|-----------|----------|----------|
| B, C | `brand_context` | Diferencial real, productos café (Lion's Mane/Full Blend/Nespresso), tono. **Grounding base.** |
| B | `competitors` / `competitor_share_of_voice` | Mapa competitivo real (hoy lidera **Rytual Café**, 9 ads) |
| D | `smartbrain_get("/api/sales/product-mix")` | Baseline café + **afinidad/upsell** (qué bundlear) + márgenes |
| D | `revenue_analytics` / `business_overview` | Contexto financiero (revenue total, AOV, split B2B/B2C) |
| E | `meta_ads_summary` | Qué rinde hoy en ads (ROAS 7.91) para proyectar costo de adquisición |
| D | `ideal_customer_profile` | ICP — *ojo: CRM de SF vacío → caer a afinidad/b2c en su lugar* |

## 4. Hallazgos de baseline ya detectados (con la data en vivo, jun 18)
- Café Lions Mane Molido 210g (A003/A004): **mueve ~30 unidades en el período pero figura
  revenue $0** → confirma el gap conocido (**MeLi no sincroniza**; ver [[reference_smartfoods_sales_data_map]]).
  El sprint debe **cerrar ese gap o declarar el supuesto** antes del P&L.
- Extractos con margen **56,7%** → referencia de margen objetivo para el café.
- `product-mix` trae `affinity` y `upsell` → input directo para el **bundle café + extracto**.

## 5. Entregable
Documento **"Café Relanzamiento — Inteligencia + Plan"** (Markdown → Obsidian, alimenta los
docs existentes del proyecto; opcional deck/PDF para inversores):
1. Resumen ejecutivo + recomendación (go / no-go / ajustar).
2. Mercado & demanda.
3. Competencia (tabla comparativa + amenaza marca-espejo Smart Coffee).
4. Regulatorio & claims seguros.
5. Posicionamiento + pricing + **bundle** (basado en afinidad real).
6. Plan de canales (Shopify / MeLi / B2B).
7. Mensajes / ángulos.
8. **P&L y camino a USD 25k/mes** (supuestos explícitos).
9. Riesgos + **gaps de data a cerrar**.
10. Fuentes web citadas + data propia citada (trazable).

## 6. Dependencias a resolver (honesto)
- **Buscador web**: DeerFlow necesita un proveedor (Tavily o Serper) para el research externo.
  **No tenemos key.** Tavily tiene free tier (~1000 búsquedas/mes) → alcanza para el sprint.
  Es lo único nuevo además del host.
- **LLM**: Gemini 2.5 Flash, ya configurado (key reutilizada de SmartBrain). Poner **tope de
  tokens por corrida** (las tareas de horizonte largo queman).
- **Host**: un VPS (decisión pendiente). El conector MCP debería co-locarse con DeerFlow y
  tunelizar al VPS de SmartBrain.

## 7. Validación de ROI — y lo que se puede hacer YA, gratis
**La vara**: ¿el dossier sale accionable sin rehacerlo? ¿fuentes reales + cifras propias correctas?
¿corre desatendido en minutos vs. días a mano?

**Atajo sin gastar un peso**: el conector MCP ya está vivo. Claude (en esta sesión) puede actuar
como "el agente conectado a Smart Brain" y producir un **prototipo de 1-2 secciones** del dossier
ahora — combinando WebSearch + las tools del conector. Es la mejor forma de ver el output **antes**
de aprovisionar VPS + Tavily. Si convence → recién ahí se dedica infra.
