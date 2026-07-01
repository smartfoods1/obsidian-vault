---
date: 2026-05-02
type: auditoria
tags: [smart-foods, meta-ads, marketing, diagnostico, clica-ads]
status: en-curso
proyecto: smart-foods
horizonte: 3x-ventas-3-meses
---

# Auditoría Meta Ads — Smart Foods (mayo 2026)

> Diagnóstico inicial corrido vía Meta MCP el 2026-05-02. Objetivo: plan accionable para 3x ventas en 3 meses.

## Contexto

- **Facturación actual:** $5M-15M ARS/mes (D2C + ML + B2B)
- **Target 3 meses:** $15M-45M ARS/mes
- **Budget Meta declarado:** $500k-1.5M ARS/mes
- **Cuello de botella percibido:** falta de tráfico de calidad
- **Modelo de gestión:** fee fijo mensual con agencia Clica Ads

## Cuentas publicitarias detectadas

| Cuenta | ID | Business | MCP | Notas |
|---|---|---|---|---|
| Smart Foods - Cuenta publicitaria | 261105152625517 | Smart Foods | ✅ Habilitada | **Cuenta principal con pixel histórico — sub-utilizada** |
| Smart Food - LC NEW | 756662553371632 | Clica Ads | ❌ Pendiente rollout Meta | **Donde corre la inversión real** — no auditable hasta que Meta habilite |
| Benthos.ar | 333542950618334 | Negocios Conscientes | ✅ Habilitada | Cuenta paralela (otro proyecto Andrés) |
| Atención al cliente | 823967187395709 | Smart Foods | ❌ Read-only | Sin uso operativo |
| Test WhatsApp Business | 2212545065946667 | — | ❌ Pendiente | Test |

## Hallazgos críticos cuenta principal

### Estado de actividad
- **Last 30d:** cero spend, cero data
- **Last 90d:** cero spend, cero data
- **Año 2025 completo:** 5.650 impressions, 2.971 reach, 176 clicks, CPM $4.361 ARS, CTR 3,12%
- **Lifetime (abr 2023 → may 2026):** 1,27M impressions, 19.789 clicks, 635k reach, CPM $698 ARS

> Implicación: la cuenta donde vive el pixel histórico de Smart Foods perdió +12 meses de aprendizaje del algoritmo. Cada compra/ATC que pasa por la web NO está alimentando este activo.

### Errores estructurales detectados
- 3 ad sets pausados por audiencia "Website Visitors" eliminada
- 1 ad set pausado por lookalike "P. similar (AR, 1%) - Website Visitors" eliminado
- 1 ad con error de procesamiento (no publicado)
- 31 campañas en la cuenta sin archivar (incluso de 2021-2022, "Smart Coffee", "[10/01/2022] Promoción", etc.)
- Sin nomenclatura consistente
- Vertical mal categorizado: "Household Goods - nonDurable" (debería ser Food/Health & Wellness)

### Métricas de calidad del setup (lo que NO encontré)
- ❌ Sin opportunity score con recomendaciones
- ❌ Sin anomaly signals
- ❌ Sin auction ranking benchmarks
- ❌ Sin industry benchmarks
- ❌ Sin performance trends de ROAS

> Razón probable: cuenta sin volumen suficiente para que Meta genere insights.

## Diagnóstico de gobernanza (problema raíz)

El problema **no es de creatividades, targeting ni budget**. Es estructural:

1. **Ceguera de C-Suite.** CEO paga fee fijo y no tiene acceso directo/visibilidad diaria de la cuenta donde corre el spend. Anti-patrón vs lo que harían Bezos, Thiel, Musk: ningún CEO escalando 10x está ciego sobre sus drivers críticos.

2. **Fee fijo + cuenta opaca = peor combinación.** Sin % sobre performance no hay incentivo a optimización agresiva. Sin acceso directo no hay auditoría posible.

3. **Pixel y aprendizaje algorítmico están en la cuenta equivocada.** El activo de medios real (los datos de comportamiento + lookalikes + retention audiences) debería estar en la cuenta del business "Smart Foods", no en la de la agencia.

4. **Falta sistema operativo de marketing.** Sin naming convention, sin proceso de archivo, sin auditorías recurrentes. 31 campañas legacy es un síntoma.

## Plan de acción

### Inmediato (esta semana)

**1. Pedir a Clica Ads:**
- Habilitar MCP/API access en cuenta LC NEW (cuando Meta lo habilite)
- Reporte últimos 90 días con: spend, ROAS por campaña, CPA, frecuencia, audiencias activas, top creatives
- Acceso de viewer a la cuenta para Andrés y CMO (si no lo tiene)

**2. Decisión de modelo de gestión:**
- Opción A: mantener Clica Ads + exigir transparencia + migrar a fee + % performance
- Opción B: traer trafficker in-house o freelance que rinda directo a CEO ← **recomendado**
- Opción C: híbrido (agencia para prospecting, in-house para retargeting + catalog)

**3. Limpieza de cuenta principal:**
- Archivar las 31 campañas legacy
- Recrear audiencias core:
  - Website Visitors 30/60/180d
  - Engagers IG/FB 90d
  - Lookalikes 1-3% AR de compradores Shopify (CSV ≥1.000 personas)
  - Custom audiences de Klaviyo (top spenders, repeat buyers)
- Verificar pixel + CAPI Shopify (Event Match Quality score)
- Catálogo Shopify sincronizado para Advantage+ Catalog Ads
- Re-categorizar vertical en Meta

### Mes 1 — Sentar bases

- Estructura ABO+CBO testeada
- Mínimo 3 ángulos creativos por línea (Brain Boost, Longevity, Immune, Inner Glow)
- Funnel: TOFU video UGC → MOFU testimonial/educativo → BOFU oferta+retargeting
- Budget objetivo: $2M-3M ARS/mes
- KPI mes 1: pixel sano + 3 audiencias performing + ROAS ≥ 2,0 en cold

### Mes 2-3 — Escalar

- Subir budget a $3M-5M ARS/mes con CBO horizontal
- Iteración semanal de creatives (mínimo 6 nuevos por semana)
- Activar Advantage+ Shopping con catálogo entero
- B2B en LinkedIn + outbound desde SmartBrain (no Meta)
- KPI mes 3: ROAS blended ≥ 2,5 con spend 3x

### Inversión necesaria realista

Para 3x ventas (de ~$10M a ~$30M/mes blended) con LTV/CAC sano:
- Meta Ads: $3-5M ARS/mes (vs $500k-1.5M actual)
- Email/WA (Klaviyo + journeys SmartBrain): mantener
- Influencer/UGC: $500k-1M ARS/mes
- B2B prospecting: ya cubierto por SmartBrain

## Riesgos y puntos ciegos del plan

- 3x en 3 meses depende fuertemente de capacidad de cumplimiento operativo (stock, packing, atención). Si Florencia se satura, escalar ads agrava el problema.
- Pasar de Clica Ads a in-house tiene curva de aprendizaje 30-45 días — durante ese tiempo puede haber bajón temporal.
- Si el LTV no soporta CAC más alto, escalar genera pérdida. Hay que validar contribution margin antes de subir budget.
- Argentina: variables macro (inflación, devaluación) pueden alterar economics rápido.

## Sources / data points

- Meta MCP — `ads_get_ad_accounts` (2026-05-02)
- Meta MCP — `ads_get_ad_entities` lifetime + last_year cuenta 261105152625517
- Meta MCP — `ads_get_errors` cuenta 261105152625517
- Meta MCP — `ads_insights_advertiser_context` (vertical Ecommerce / Household Goods-nonDurable)
- Conversación CEO — Andrés Special, 2026-05-02

## Próximos pasos

- [ ] Pedir export CSV últimos 90d a Clica Ads (cuenta LC NEW)
- [ ] Subir CSV o screenshots para auditoría de la cuenta donde corre el spend real
- [ ] Decidir modelo de gestión (mantener / migrar / híbrido)
- [ ] Empezar limpieza de cuenta principal en paralelo
- [ ] Validar contribution margin para definir CAC máximo soportable

---

> Próxima revisión: una vez que llegue data de Clica Ads (objetivo: 2026-05-09)
