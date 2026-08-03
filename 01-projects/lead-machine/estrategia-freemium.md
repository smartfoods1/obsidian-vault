---
date: 2026-07-06
type: estrategia
tags: [gondola, lead-machine, freemium, monetizacion, pricing, retencion, producto]
status: fase-2b-deployada
derivado_de: workflow multi-agente (6 lentes + verificación adversaria + síntesis)
---

# Gondola — Rediseño Freemium (free/paid)

## Estado de ejecución

**Fase 1 DEPLOYADA (6/7/2026, `./deploy.sh` OK, 281 tests verdes):** anti-farming testimonial (reward on-approve, no on-submit; backfill `rewarded=1` a los previos), anti-farming cupón (`new_only` → `pending_coupon_credits`, se activa con la 1ra compra), bonus x2 dinámico 1ra compra (pack entrada, toggle `LM_FIRST_PURCHASE_X2`), unlock ICP para Pro/Expansión (`plan='mensual'` en `mp_webhook`), `/api/me` expone pending + elegibilidad bonus. Todo backend en `app.py`; columnas nuevas migradas y verificadas en prod.

**Fase 2a DEPLOYADA (6/7/2026, Fork A elegido, 292 tests verdes):** gate central de contacto backend (`_brand_has_paid` por `mp_payments`/plan/unlimited — nunca `paid_credits`; blanqueo on-read en `/api/leads`, `/api/my-leads`, `/api/lead/:id`, `/api/export`; `followup`→402) + front (componente `UnlockContact`, lock+CTA en grilla/resultados/ficha, driven por `contact_locked`). El free ve el fit; WhatsApp/dueño/email/IG/mensaje se destapan al 1er pago, a nivel cuenta, sin re-enriquecer. Verificado contra usuario free real (brand 127: 15 leads, contacto intacto en `saved_leads.data`).

**Fase 2b DEPLOYADA (6/7/2026, 2 olas, 309 tests):**
- **Ola 1:** export PDF/XLSX solo pagos (CSV/JSON libres) · ancla honesta `best_deal_ars` (mayor venta cerrada) en el paywall · Paywall muestra bonus x2 en el pack de entrada + créditos reservados.
- **Ola 2 — blur del pescado gordo:** backend enriquece PEEK_EXTRA leads extra para la cuenta sin pago (fit visible, contacto tapado, nombre "Dietética N***"), aislado + fail-soft, no se guardan ni cobran; front los renderiza bajo los resultados.

**TODO PRENDIDO Y VERIFICADO EN VIVO (7/7/2026):** `LM_PEEK_EXTRA=10` en prod → búsqueda real de cuenta free en Palermo devolvió 5 full + **10 peek** (fit 95/93/90, nombres enmascarados, contacto vacío). Cuenta de prueba borrada. Teaser ICP: `InformeCompatibilidad` muestra card "Disponible con Pro" + adelanto de rubros + CTA a Pro para el free. Copy "sin calificar" en el paywall. **Nada pendiente.**

**Guardrail #1 a medir:** tasa signup→primera-búsqueda 2 semanas; si cae fuerte, aflojar a Fork B (mostrar nombre_contacto, tapar WhatsApp+mensaje). Toggles: `LM_PEEK_EXTRA`, `LM_FIRST_PURCHASE_X2`, `LM_TESTIMONIAL_MIN_QUOTE`.

## Diagnóstico de raíz

Hoy **free y pago entregan EL MISMO lead**: misma calidad, mismos campos, mismo `primer_mensaje` ejecutable. La única diferencia es cantidad (5 vs 60/200/600). Por eso pagar da "más de lo mismo" y la disposición a pagar (WTP) se muere: una marca con TAM chico en zona densa saca sus 5 leads full + WhatsApp + mensaje escrito + export, cierra sus primeras cuentas y **no vuelve nunca**. La escalera es 100% cantidad ($817→$595→$483 por lead), así que no hay razón para elegir Pro salvo el label "el más elegido". Encima los rewards se acreditan **antes de verificar** (testimonial +15 pre-moderación, cupón +10 al alta) → medio pack gratis por cuenta trucha en <10 min. El problema no es el COGS (margen >95%): es que **el producto nunca separa la PRUEBA del canal (gratis) de la EJECUCIÓN sobre el canal (paga)**.

## Principio rector

**El free PRUEBA que el canal existe; el pago te deja OPERARLO.**
Se ve todo (fit, match, marcas que ya vende, cuántos comercios hay en tu zona), pero **el contacto y el mensaje listo** — lo único caro de reproducir a mano y lo que convierte un lead en una venta — se destapan pagando. Gating por **profundidad y acción**, nunca solo por cantidad. Cada escalón desbloquea algo que el usuario **ya vio tapado** en el escalón de abajo.

## Free redesign — qué queda / qué se corta

**Queda gratis (la prueba intacta):**
- 5 leads con fit_score, fit_reason, posicionamiento/match, marcas_complementarias, ecosistema, actividad, rating/reviews y localidad **completos**.
- Preview de zona read-only con **conteo real** de comercios que matchean (dato Places, cero costo IA) + top-3 nombres con contacto oculto.
- 10 leads extra en **"blur del pescado gordo"**: se ve fit_score y por qué encaja, tapado contacto + primer_mensaje.
- CRM/pipeline completo (estados, notas, timeline) → el anzuelo de switching cost.
- Export CSV/JSON de sus 5 leads (crudo).
- 1 follow-up gratis de por vida. Re-enrich libre (choca con la garantía, no se toca).
- Teaser del ICP (3-5 rubros + 1 frase).

**Se corta / gatea (la ejecución):**
- **Contacto accionable** (whatsapp, teléfono, nombre_contacto, email, IG, primer_mensaje) de los leads no facturados.
- Export **PDF** (dossier con marca) y **XLSX** (planilla de ruteo).
- 2º follow-up en adelante (la secuencia es donde se cierra el 80% del B2B).
- Filtro/orden por fit + heatmap de zona.
- Informe ICP completo (research plan→síntesis→crítica con targets).

**Regla dura:** el gate es a nivel CUENTA (nunca pagó), **on-read con whitelist server-side** (nunca blacklist ni blur CSS — que devtools no filtre el dato). Al primer pago MP todos los leads se desbloquean solos, sin re-enriquecer (el valor ya vive en `saved_leads.data`). Nunca gatear por `paid_credits>0` (castiga al que ya gastó el pack): computar "alguna vez pagó" por query sobre `mp_payments` o `plan`/`unlimited`.

## Matriz de features

| Feature | Free | Buscador $49k | Pro $119k | Expansión $290k | DFY |
|---|---|---|---|---|---|
| Leads | 5 | 60 | 200 | 600 | gestionado |
| Fit score + análisis | ✅ completo | ✅ | ✅ | ✅ | ✅ |
| Contacto accionable (WA/nombre/email/IG) | 🔒 tapado | ✅ | ✅ | ✅ | equipo contacta |
| primer_mensaje (icebreaker) | 🔒 | ✅ | ✅ | ✅ | lo escribe el equipo |
| Follow-ups | 1 de por vida | ilimitados | ilimitados | ilimitados | gestionado |
| Export CSV/JSON | sus 5 | ✅ | ✅ | ✅ | entregado |
| Export PDF (dossier) + XLSX (ruteo) | ❌ | ❌ | ✅ | ✅ | ✅ |
| Filtro/orden por fit + heatmap | ❌ | ✅ | ✅ | ✅ | — |
| Informe ICP completo | teaser | teaser | ✅ regenerable | ✅ regenerable | hecho por equipo |
| CRM/pipeline | ✅ | ✅ | ✅ | ✅ | ✅ + gestión |
| Bonus x2 primera compra | — | ✅ (pack entrada) | — | — | — |

## Qué desbloquea cada pack (features, no solo saldo)

- **Buscador ($49k):** destapa TODO el contacto + primer_mensaje de sus leads (incluidos los 5 free y los 10 en blur que ya vio) + follow-ups ilimitados + filtro/orden + export completo + bonus x2 (60→120, solo pagás los que tienen WhatsApp). *"Validá el canal: destapá lo que ya viste. Doble por ser tu primera compra."*
- **Pro ($119k, destacado):** todo Buscador + **informe ICP completo** (el cerebro que te dice a qué rubros/zonas apuntar, regenerable) + export PDF con tu marca (dossier presentable al dueño de góndola) + ICP que se afina con tu pipeline. *"No comprás más leads, comprás el cerebro que te dice a quién apuntar y la herramienta para cerrar."*
- **Expansión ($290k):** todo Pro + volumen multi-zona + mejor precio por lead. *"Escalá."*
- **DFY:** prospección + contacto + seguimiento gestionado, sin precio público. *"Delegá."*

## Mecánicas de conversión

1. **Blur del pescado gordo** (free ve 15, toca 5): enriquecer 15, servir 5 top completos, devolver 10 en `locked_leads` con whitelist server-side (fit visible, contacto NO en el JSON, nombre pre-mascarado "Dietética N***"). No se guardan, no consumen crédito. → *Endowment invertido: pagar es "recuperar" leads que ya siente suyos, no comprar algo nuevo.*
2. **Preview de zona = ancla de abundancia honesta:** "En Palermo hay 34 dietéticas · calificaste 5 con IA · quedan 29 SIN CALIFICAR". Conteo factual de Google → FOMO cuantificado que el producto nunca traiciona.
3. **Ancla "1 venta mayorista paga el pack":** parsear `ticket_mayorista_ars` del wholesale_offer que la marca ya carga; en el 402/pricing: "Una dietética que reponga 1×mes ≈ $X. Buscador ($49k) se paga con el primer pedido." Si hay deal cerrado real en el pipeline, usar ESE número. → Mueve el ancla de "precio por lead" a "precio vs cliente recurrente".
4. **Bonus x2 primera compra reencuadrado:** elegibilidad dinámica (sin fila previa en `mp_payments`), solo pack de entrada. Copy: "60 se convierten en 120, y solo pagás los que tienen WhatsApp."
5. **Prueba social real de par argentino:** testimonial acreditado solo al aprobar; author_name = "Marca real — rubro — resultado" ("La Receta — cosmética natural — cerró 3 dietéticas en Palermo"). → La confianza es el cuello real free→pago en este segmento, no el precio.
6. **Nudge de expansión por pipeline lleno (no por créditos agotados):** flag en `/api/my-leads` si `pct_nuevos<0.20 AND cerrados>=1 AND trabajados>=5`. Banner: "Ya trabajaste [zona] y cerraste 1. Buscá más antes de que se enfríe." → Ataca WTP en el pico exacto de valor demostrado.

## Anti-farming (desplegar PRIMERO)

1. Testimonial: eliminar el `UPDATE paid_credits` del submit (app.py:3512). Submit solo inserta `status='pending'`. Validar `len(quote)>=80` antes del INSERT.
2. Acreditar solo al moderar: columna `testimonials.rewarded`; en aprobar, UPDATE atómico gateado por rowcount y recién ahí sumar reward.
3. Cupón de bienvenida: columna `brands.pending_coupon_credits` (no gastable). En `/api/redeem` con new_only → acreditar ahí; en el 1er pago MP hacer flush a `paid_credits`. El cupón queda como incentivo a comprar, no crédito farmeable.
4. GONDOLA10 con `new_only=1 + min_created_at`. Dedup por email en `coupon_redemptions` (UNIQUE(code,email)) — el email es el eje real, la IP es débil.
5. Resultado: los 25 créditos gratis instantáneos → 0. Ninguna rama toca `mp_payments` ni `external_reference`.

## Roadmap priorizado

**Quick wins (backend puro, esta semana):**
- Anti-farming testimonial + cupón (S) — **alto**, protege toda la escalera.
- Ancla "1 venta paga el pack" en 402/pricing (S) — medio.
- Bonus x2 por elegibilidad dinámica, expuesto solo a quien nunca pagó (S) — **alto**.
- Preview de zona con conteo real + copy "29 sin calificar" (S) — **alto**.
- Gate 2º follow-up (S) + gate export PDF/XLSX a Pro+ (S) — medio (tocan front para que el 402 abra el modal).

**Bigger bets (requieren rebuild del SPA):**
- Gate central de contacto a nivel cuenta (`_gate_lead` con whitelist en todos los consumidores) — **alto**, es el corazón.
- Blur del pescado gordo (free ve 15, toca 5) — **alto**.
- Pack desbloquea ICP completo (`plan='mensual'` para Pro/Expansión) + teaser en onboarding — **alto**.
- Nudge de expansión por pipeline lleno — **alto**.
- ICP v2 que se afina con el pipeline (rubros ya cerrados) — palanca de NRR/recurrencia (L).

## Guardrails

- **Adquisición:** el WhatsApp NUNCA se muestra en free (es el valor + base de la garantía). Si baja signup→primera-búsqueda, aflojar mostrando nombre_contacto (a quién) pero manteniendo tapados whatsapp + primer_mensaje (el cómo).
- **Costo:** enriquecer 15 en vez de 5 triplica el burn en el único tier no monetizado → cache del preview redactado por (brand_id, region, targets), solo en la 1ª búsqueda de zona nueva.
- **Whitelist server-side**, nunca blacklist ni blur CSS.
- **No romper billing:** gate por "alguna vez pagó" (query mp_payments), no por saldo actual.
- **No tocar** la garantía "sin WhatsApp no te lo cobro", ni `/enrich`, ni `mp_payments`/`external_reference`/keys de packs.
- **Secuencia:** anti-farming ANTES que cualquier feature-gate (si no, farmean créditos para saltar el gate).

## Fork de decisión pendiente (Andrés)

Qué tan agresivo el free: **(A)** tapar todo el contacto (mayor conversión, algo de riesgo de adquisición) vs **(B)** mostrar nombre_contacto pero tapar whatsapp + primer_mensaje (más suave). Recomendación: arrancar en A con el guardrail de medir signup→búsqueda y caer a B si cae.
