---
date: 2026-07-16
type: playbook
tags: [gondola, lead-machine, ventas, primer-cliente, dfy, kaizen]
status: activo
---

# Kaizen Market Natural — Primer cliente de Gondola (prep call 17/07)

Primer cliente pago de Gondola. Compraron **Pro (200 leads, $119.000)** después de haber preguntado por el DFY "Tu equipo de ventas". Call de descubrimiento agendada para mañana. Objetivo: entenderlos a fondo + validar fit + tee del DFY. Este cliente = aprendizaje + caso de referencia, no margen.

## Quién es Kaizen (web: kaizenmarketnatural.mitiendanube.com)

- **Reventa pura, NO marca.** Venden online (Tienda Nube) marcas de terceros: Muscle Pro, Natural Nutrition, Wake Up, Vitalgy, Lappiel, Mudra, Bigual.
- Dietética online chica, **reabrió hace poco**. Ticket B2C $12k–$65k. Envío gratis desde $40k.
- Contacto: WA +54 9 11 7135-0793 · IG @kaizennaturalmarket.
- Sin sección mayorista/B2B visible.

## El hallazgo clave (resolver en los primeros 10 min)

Gondola sirve para que una MARCA/distribuidor encuentre dietéticas a las que venderle mayorista. Kaizen *es* una dietética (reventa). Bifurcación:

- **A (encaja):** quieren abrir brazo **mayorista/B2B** (venderle a otras dietéticas/gimnasios/farmacias). Su mensaje dice "desarrollar el canal comercial" → suena a esto.
- **B (no encaja):** quieren más compradores **B2C online** → Gondola NO hace eso. Si es B, reencuadrar/ser honesto, no cobrar por herramienta equivocada.

No asumir A. Preguntar. Ya pidieron DFY antes de comprar Pro → upsell tibio.

## Estado real del producto (auditoría código 16/07)

- ✅ Gating free vs pago YA funciona (free 5 leads contacto tapado; pago desbloquea). El problema del 10/7 (free==pago) está resuelto.
- ✅ CRM interno (pipeline nuevo→ganado, deal_value, notas), enriquecimiento Gemini (surtido + voz cliente + dossier), garantía "solo pagás los que tienen WhatsApp" + bonus x2 primera compra.
- ⚠️ **No prometer "leemos su IG automático":** business_discovery bloqueado por scope `instagram_manage_insights`; surtido IG va por extensión Chrome (fail-closed 403 sin `LM_INGEST_KEY`, hoy no seteada). El surtido actual sale de grounding web, NO del IG real del comercio.
- 🟢 **Informe ICP SÍ disponible para Kaizen (corregido 16/07):** brand 152 tiene `plan='mensual'` además de 200 créditos → `report_access=True`. La "trampa 403" NO aplica a Kaizen; se les puede mostrar el informe de compatibilidad en la demo. (El 403 solo pega en cuentas que compran pack de créditos SIN plan.)
- Cada lead trae `primer_mensaje_ia` (icebreaker personalizado con la oferta mayorista) — buen activo para la demo. La web B2C de Kaizen NO va a inferir bien su ICP mayorista: cargar a mano su oferta/targets mayoristas en el perfil.
- 🔴 **P0 seguridad SIGUE VIVO:** `sign()` (app.py:781) firma brand_id sin scoping de dominio; mismo esquema para cookie sesión + link baja mail + tracking → token de link de baja sirve como sesión → toma de cuenta. Con cliente real = prioridad esta semana.
- DFY hoy se entrega **a mano** (`dfy_consultas` captura y pinga a Andrés). El "equipo" = Andrés + Flor. No vender capacidad de fábrica inexistente.

### Precios reales
Free 5 · Buscador 60/$49k · **Pro 200/$119k** · Expansión 600/$290k · DFY a medida.

## Plan de la call

1. **Descubrimiento primero (no abrir app):** ¿canal comercial = B2B o B2C? ¿qué marca empujar? ¿exclusividad/margen mayorista? ¿ya vendieron a comercios? ¿zona? ¿quién contacta/visita?
2. **Demo en vivo corta:** correr búsqueda real de su ICP, mostrar 8–10 leads con fit + contacto + mensaje.
3. **Cómo sacarle jugo al Pro:** perfil/oferta → ICP → 200 leads → pipeline → garantía.
4. **Tee del DFY:** "Pro = ustedes con la máquina; DFY = nosotros manejándola por ustedes."

Expectativa honesta: son de los primeros, línea directa con Andrés, afinamos juntos.

## Propuesta DFY "Tu equipo de ventas" (piloto 90 días, ponderado por resultado)

- **Scope:** ICP mayorista + guion de oferta · prospección gestionada · outreach nuestro hasta agendar · reunión entregada a Kaizen para cerrar · reporte quincenal en CRM.
- **Precio FINAL — modelo CAZADOR (decidido 16/07):** **USD 600/mes + USD 75 por cuenta abierta** (comercio nuevo con 1ª orden pagada, sin importar el monto) **+ reórdenes 100% de ellos + 3 meses mínimo.** Se factura en pesos al TC del día; el Pro que ya pagaron queda integrado sin cargo extra. One-pager PDF generado (plantilla para las otras distribuidoras).
- **Por qué cazador (y no comisionista ni plataforma):** cazar escala, cultivar no. Cobrar % de reórdenes = o te puentean (fuga) o te atás a account-management eterno (el tiempo operativo que Andrés NO quiere). Modelo intermediario/take-rate 10% GMV se descartó para distribuidoras: como rieles competís con el distribuidor, no le vendés; y el fee se calcula sobre MARGEN, no sobre facturación (error a evitar: 50% de la orden > margen del distribuidor = pierden plata). Cartera objetivo ~4 marcas en cazador ≈ USD 2.400/mes base + aperturas. **El modelo plataforma/intermediario queda PARKED para "marcas" (no distribuidoras), a validar aparte (engancha con la red opt-in de dietéticas).**
- **No cerrar mañana.** Presentar como destino: arrancar con Pro, probar en 2–3 semanas, después activar DFY con la prueba en mano.

## Checklist esta noche
1. Correr prospección de prueba del ICP de Kaizen y entrar con la lista en mano.
2. Verificar que la cuenta Pro esté acreditada (200 créditos, contacto desbloqueado).
3. No poner IG-auto al frente.
4. Agendar fix del P0 de seguridad para esta semana.

## Update 16/07 (noche) — Diagnóstico técnico + fix

**FIT CONFIRMADO:** Kaizen es DISTRIBUIDORA y ya vende a dietéticas. Gondola encaja perfecto: DFY = abrirles bocas nuevas (dietéticas/gimnasios/farmacias) sin frenar su operación. La duda B2B vs B2C quedó saldada; el foco de la call pasa a *madurez de su departamento comercial*, no a "¿les sirve?".

**"Da cero" (RESUELTO):** la causa NO era el pago de Kaizen (créditos OK: brand 152, 200 paid_credits + plan mensual). Era la API de Gemini devolviendo **403 por un problema de billing en Google** que Andrés resolvió. Sin Gemini, el enriquecimiento fallaba y todo lead sin `fit_score` se descartaba (app.py:4071) → 0 resultados y 0 créditos consumidos. Verificado post-fix: pipeline OK, 6/6 dietéticas de Palermo scoreadas con icebreaker. La demo en vivo va a funcionar.

**P0 seguridad: ARREGLADO (local, testeado), PENDIENTE DEPLOY.** `sign()`/`unsign()` ahora scopean por propósito (session/unsub/click); 6 call-sites aislados; 6 tests de regresión nuevos, suite verde. `./deploy.sh` invalida sesiones vigentes (Kaizen re-loguea) — decidir timing.

**Lectura de Instagram (item 5):** la vía oficial (business_discovery) es callejón (solo cuentas Business + App Review 2-4 sem + no cubre cuentas personales). Recomendado: **Apify Instagram Profile Scraper** (~$2,6/1000 perfiles, 1 REST, JSON estructurado con bio+category+últimos posts) como #1; **HikerAPI** como #2/fallback (real-time, ~$0,001/req). Roadmap, no urgente.

**Discovery afinado (madurez comercial B2B):** cómo consiguen dietéticas hoy (frío/referidos/inbound); vendedor dedicado o el dueño; qué sistema de seguimiento usan (Excel/CRM/WA suelto); cuántos PDV activos y cuántos quieren sumar/mes (= meta del piloto); qué los frena (tiempo / a quién contactar / conversión); si buscan sumar marcas nuevas o exprimir las que tienen; márgenes/mínimos/zonas; **ticket y recompra de una cuenta mayorista (= ROI del fee DFY)**.

One-pager DFY generado: `~/lead-machine` → PDF en scratchpad de la sesión.

Relacionado: [[brand-gondola]] · [[estrategia-freemium]] · [[../growth-b2b-canal-dieteticas/index|Growth B2B canal dietéticas]]
