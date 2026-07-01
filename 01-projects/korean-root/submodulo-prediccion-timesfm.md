---
date: 2026-06-18
type: project
tags: [korean-root, smartbrain, analytics, forecasting, timesfm, ml]
status: live
---

# Submódulo de Predicción de Compras — Korean Root (TimesFM)

Submódulo de analytics que da **forecast predictivo de demanda y compras** para Korean Root usando **Google TimesFM 2.5** (foundation model de series temporales, zero-shot), desplegado y funcionando en el VPS de KR (`103.199.187.246`).

> Pedido original del CEO: *"un submódulo de analytics que dé información predictiva de compras usando este modelo de Google (TimesFM en BigQuery)"*. Se eligió correr **TimesFM open-source local** (no BigQuery) para evitar costo/ETL de GCP — mismo modelo, sin dependencia externa.

## Arquitectura

Motor **pluggable** detrás de una interfaz común, con **fallback estadístico por serie** (si TimesFM no carga o una serie falla, el submódulo igual produce forecast). Separación dura: el modelo NUNCA corre dentro de la API viva.

```
[cron nocturno 05:35 ART]
  → cron_timesfm_forecast.py  (venv aislado /opt/forecast-venv: torch CPU + timesfm 2.5)
      → lee v_all_sales (órdenes pagadas TN)
      → arma series SEMANALES: revenue, órdenes, top-8 productos por unidades
      → TimesFM forecast 8 semanas + banda P10–P90 + backtest SMAPE
      → escribe tablas demand_forecast_* (snapshot: borra corridas viejas)
  → /api/forecast/*  (router read-only, NUNCA importa torch)
  → tab "Predicción" en /analytics (recharts: histórico + forecast + banda)
```

### Por qué semanal y no diario
A resolución diaria la demanda de un CPG es intermitente (mayoría de ceros) y el SMAPE explota (~200%). Semanal suaviza, coincide con la cadencia real de reposición, y hace el error interpretable. Con datos densos de KR el SMAPE bajó a ~35% en revenue/órdenes.

### Por qué TimesFM local y no BigQuery
BigQuery `AI.FORECAST` requería proyecto GCP + billing + ETL SQLite→BQ. El dataset de KR es modesto (no "big data"). Correr TimesFM open-source en un venv aislado da el mismo modelo, gratis, sin dependencia externa que pueda romperse en silencio.

## Componentes (archivos en el VPS de KR)

| Componente | Path |
|---|---|
| Batch | `/root/.openclaw/workspace/scripts/cron_timesfm_forecast.py` |
| Router | `packages/ecommerce/backend/routers/forecast_demand.py` (registrado en `ecommerce/module.json`) |
| Frontend | `frontend/src/pages/Analytics.tsx` → tab "Predicción" (`ForecastTab`) |
| Cron | `smartbrain-forecast.service` + `.timer` (systemd, 05:35 ART, `MemoryMax=3400M`, `Nice=15`) |
| Venv | `/opt/forecast-venv` (torch 2.12 CPU, timesfm 2.5, pandas) — **aislado de la API** |
| Swap | swapfile 4GB (`/swapfile`, en fstab) — red de seguridad para el pico ~2.1GB de TimesFM |

### Tablas (en `ops_korean-root.db`)
- `demand_forecast_runs` — metadata de cada corrida (engine, status, duración, conteos)
- `demand_forecast_series` — resumen por serie (fc_sum, banda, trend %, SMAPE, reorden)
- `demand_forecasts` — puntos de forecast (ds, yhat, yhat_lower, yhat_upper)
- `demand_forecast_history` — últimas ~52 semanas de actuals (para graficar)

### Endpoints (`/api/forecast`)
- `GET /status` — última corrida, engine, frescura de datos
- `GET /summary` — headline (revenue + órdenes próx. 8 sem), productos, alertas de reorden
- `GET /series` — lista de resúmenes de series
- `GET /series-detail?key=...` — histórico + forecast de una serie (para el chart)

## Resultados primera corrida (2026-06-18)

10 series, **100% TimesFM** (0 fallback), 19s, status=ok. Datos frescos (lag 3 días).

| Serie | Forecast 8 sem | Tendencia | SMAPE backtest |
|---|---|---|---|
| Revenue total | ~70,5M ARS | −28,7% | 34,8% (buena) |
| Órdenes pagadas | ~958 | −34,7% | 34,6% (buena) |
| COMBO BOOSTER | 306 u | −14,4% | 32% |
| RITUAL CUÁNTICO | 160 u | −22,8% | 41% |
| LIMONADA CUÁNTICA | 132 u | −72,3% | 74% (ruidosa) |

> ⚠️ **Señal de negocio**: la tendencia a 8 semanas da **−28% en revenue y −35% en órdenes** vs el período previo. Puede ser estacionalidad (invierno AR, junio) o baja real — vale la pena que Victoria lo mire. El modelo es zero-shot sobre 50.678 órdenes (2020→hoy).

## Caveats
- **KR no es monoproducto** (220 productos / 320 SKUs vendidos): el forecast por producto tiene valor real para compras.
- **Sin datos de stock** cargados para KR → las alertas de reorden quedan en null (sólo se muestra demanda predicha). Si se carga `stock` con `brand_id='korean-root'`, el reorden se activa solo.
- Productos muy intermitentes (ej. Limonada suelta) tienen SMAPE alto: usar el **total a 8 semanas** como guía de compra, no la semana puntual.

## Robustez (post code-review adversarial)
- `flock` anti-doble-corrida (mata race condition del snapshot)
- Guards: `HORIZON≥1`, `MIN_POINTS≥2`, serie vacía en fallback, validación de forma de cuantiles TimesFM
- `busy_timeout` 40s, status `empty` si no hay series
- Banda recharts vía `Area dataKey=[min,max]` — patrón oficial verificado en docs (no era bug pese al flag del reviewer)

## Consolidación de forecast (jun 18, decisión CEO)

Había **3 forecasts de revenue compitiendo** en Analytics (Estacionalidad: estimado anual ARIMA-ish; Tendencias: proyección 6m hand-rolled; Predicción: TimesFM). Decisión: **Predicción = única fuente del futuro**.

- **Tab "Tendencias" eliminado** y fusionado dentro de Predicción: su contexto descriptivo (revenue+MA3, crecimiento MoM, anomalías) se reusa como sección "Contexto de tendencia"; su proyección 6m hand-rolled se **reemplazó por escenarios TimesFM** (P10/P50/P90 = conservador/base/optimista a 26 semanas, serie `revenue_daily_midterm`).
- **Estacionalidad** quedó como **patrón puro** (heatmap + día/semana + anomalías + pacing del mes en curso); se le sacó el card "estimado anual".
- Batch ahora computa también `*_midterm` (26 sem) para revenue/órdenes, con `kind='*_midterm'` para no contaminar el headline operativo de 8 semanas.
- Tabs finales: Facturación · **Predicción** · Estacionalidad · Productos · Clientes · Geografía.

## Toggle Semanal / Mensual (jun 18)

El CEO notó que Estacionalidad (mensual) y Predicción (semanal) "mostraban datos distintos". Se verificó que **el dato es idéntico** (misma fuente `v_all_sales`, reconciliado mes a mes al peso); la diferencia era solo la **unidad de tiempo**. Solución: el batch ahora genera **ambas granularidades** y Predicción tiene un **toggle Semanal/Mensual**:
- **Semanal**: horizonte 8 sem (operativo/compras) + escenarios 6m + contexto.
- **Mensual**: horizonte 6 meses, matchea 1:1 con Estacionalidad. **Mejor precisión** (revenue SMAPE 27% mensual vs 35% semanal — menos ruido).
- Series mensuales: keys `revenue_monthly`, `orders_monthly`, `product:<x>@m`, `freq='M'`. Endpoint `GET /api/forecast/summary?freq=W|M`; `available_freqs` indica cuáles existen. Columna `horizon` agregada a `demand_forecast_series`.

## Análisis "Por qué + Qué hacer" + merge de Estacionalidad (jun 18)

El CEO pidió: un solo submódulo (no Predicción + Estacionalidad separados) y que el dato venga con **análisis del por qué** y **acciones concretas**.

- **Tab Estacionalidad eliminado** → su heatmap/patrón pasa a "contexto detallado" colapsable dentro de Predicción (la estacionalidad ES el driver principal del forecast). Tabs finales: Facturación · **Predicción** · Productos · Clientes · Geografía.
- **Endpoint `/api/forecast/analysis?freq=W|M`**: calcula DRIVERS *grounded* (índice estacional robusto a inflación con un `note` que distingue baja **estacional** de baja **real**; tendencia MoM; productos que más mueven la cifra) y genera **diagnóstico** (por qué) + **acciones** (qué hacer). La narrativa la escribe el LLM (`llm_client`, rutea por OpenRouter) *grounded* en los drivers → **anti-alucinación**; con **fallback determinístico** por reglas si el LLM no responde. Cacheado por corrida.
- **UI**: sección "Por qué da esta cifra" + "Qué hacer" justo debajo de los KPIs.

Ejemplo real (KR, semanal): detectó que la baja de revenue (−28.7%) es **real, no estacional** (jun-jul rinde +20% estacionalmente pero el forecast cae), concentrada en LIMONADA (−72%) y FORMULACIÓN (−43%), con HOLY GOLD (+328%) y KOREAN SCALP (+20%) creciendo → acciones: investigar/promocionar las que caen, reforzar las que crecen, revisar precios para la temporada.

## Próximos pasos posibles
- Conectar `stock` de KR para activar alertas de reorden reales
- Cruzar con calendario de lanzamientos/campañas (señales exógenas) como hace `forecast_v4` en SF
- Exponer el mismo submódulo en Smart Foods (código tenant-agnóstico, lee `v_all_sales`)
