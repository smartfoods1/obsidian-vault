---
date: 2026-06-06
type: entregable-cliente
tags: [korean-root, email-marketing, smartbrain, proyeccion, content-hub]
status: listo-para-enviar
cliente: The Korean Root
---

# KR — Resumen Ejecutivo Email Marketing + Proyección 2026

> **Entregable para Victoria.** PDF presentable en `~/Desktop/Korean Root - Email Marketing - Resumen Ejecutivo 2026.pdf`. Enviar lunes 2026-06-08.

## Contexto interno (no va en el doc del cliente)

Documento de retención/valor del Content Hub. Construido a partir del análisis de las 266 campañas Perfit de KR (2022→jun 2026), clasificadas en **Smart Brain** (tag `smartbrain` + registradas en `unified_campaigns`, 22 enviadas) vs **manual** (equipo KR). Datos validados en vivo contra la API de Perfit (cuenta `koreanroot`).

**v2 (2026-06-07) — corrección post-auditoría con datos reales de Tienda Nube.** El v1 anualizaba el mes de Hot Sale (2,4M envíos/año × rev/1000 de mayo = $66,5M "ya logrado") → inflado y pinchable: ese volumen es blasting y el rev/1000 de $27.717 es de Hot Sale, no run-rate. El v2 (a) separa logrado (ARS 6,2M mes 1) de proyectado, (b) baja el volumen a cadencia sana, (c) mueve el caso de valor a la **recompra** (palanca real y defendible). PDF enviado = v2. Backup v1 en `/tmp/kr_resumen_v1_backup.pdf` + HTML v1 en `/tmp/kr_resumen.html`; HTML v2 en `/tmp/kr_resumen_v2.html`. Datos negocio: [[reference_kr_business_data]].

## Números clave (verificados)

| Grupo | Camp | Envíos | OPEN | CTR | CTOR | conv/click | rev/1000 |
|---|---|---|---|---|---|---|---|
| Manual 2025 (mejor año) | 89 | 2,48M | 8,4% | 0,199% | 2,38% | 14,3% | $20.738 |
| Manual 2026 (degradado x blasting) | 56 | 1,81M | 7,7% | 0,085% | 1,11% | 15,8% | $9.530 |
| **Smart Brain (may–jun)** | 22 | 224k | **12,6%** | 0,185% | 1,46% | **20,3%** | **$27.717** |
| Techo histórico de la lista (2024) | — | — | — | — | **4,07%** | — | — |

- Tendencia OPEN por año: 27% (2022) → 18% → 13% → 8,4% → 7,7%. **La lista se viene quemando por blasting hace 4 años.**
- El SB revirtió la caída (7,7%→12,6%) y monetiza 2,9x vs manual 2026 / +34% vs mejor año.
- Cuello de botella: el **clic** (1,5% vs techo 4%). Recuperable. Lo ataca el Paso 2.

## Bugs descubiertos (entran al Paso 2)
1. CTAs a `google.com` (campañas viejas) y a home genérica (educativas) — fallback débil en `url_catalog.py`.
2. Emails texto plano, sin imágenes, 1 solo CTA al fondo (prescripto en prompt `proposals.py:94` + `_md_to_html`).
3. `GOOGLE_ANALYTICS:"0"` y `PREHEADER:""` en Perfit → atribución ciega + open rate penalizado.
4. Sin UTM en ninguna campaña.

## Proyección 2026 (resumen) — v2 honesta
- **Logrado mes 1 (mayo, Hot Sale):** ARS 6,2M atribuidos al email. NO anualizar el Hot Sale (mayo = máx. demanda; junio fija el piso de mes normal).
- **Palanca grande = RECOMPRA:** base 38.280 clientes pagadores, recompra real **19,8%** (no 0% del campo roto), AOV ARS 71.004. Cada punto recuperado ≈ ARS 27M/año → +1,5 a 3 pts = **ARS 41–82M/año**. Es POTENCIAL (requiere ejecutar fase de retención), no logrado.
- **Email a cadencia sana:** sostiene la ventaja de eficiencia (2,9x vs manual 2026; +34% vs mejor año 2025); el volumen se subordina a la salud de la lista, no se maximiza (eso fue lo que la quemó).
- Email ≈ 8,5% del revenue total de KR → el peso grande del negocio está en la base de clientes, no en el canal email.

## Próximo paso
Implementar Paso 2 — ver plan de 6 frentes (formato con imágenes + botones, gate de links, sync imágenes TN, prompt nuevo, UTM/GA, anti-blasting). Relacionado: [[content-hub-status]].
