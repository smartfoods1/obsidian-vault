---
date: 2026-07-20
type: brief
tags: [gondola, lead-machine, red-comercios, dieteticas, product-strategy, para-revision]
status: borrador
---

# Brief para revisión — Red de comercios adheridos (Gondola)

> Documento preparado para que un agente de IA externo revise la idea de punta a punta: coherencia, riesgos, viabilidad técnica/operativa y secuencia sugerida. Es autocontenido — no asume que quien lo lee tiene contexto previo de Gondola. Todos los datos son al 20-jul-2026 y pueden haber cambiado.

## 1. Qué es Gondola hoy

Gondola (ex "Lead Machine") es una plataforma B2B de dos lados en Argentina:

- **Lado marcas/distribuidoras (quien paga hoy):** compran acceso a datos de puntos de venta (dietéticas/almacenes naturistas) — packs de leads calificados (Google Places + enriquecimiento con IA: fit score, posicionamiento premium/granel, qué vende, WhatsApp, mensaje de apertura) o una suscripción CRM (tablero kanban para gestionar su pipeline de venta mayorista).
- **Lado dietéticas (hoy son solo datos, no usuarios):** aparecen en la plataforma como resultado de búsqueda para las marcas. No tienen cuenta, no opinan, no reciben nada directamente de Gondola salvo que una marca las contacte con los datos comprados.

**Estado comercial real (20-jul-2026):** ~25 marcas reales registradas, 2 clientes pagos: Kaizen Market Natural (distribuidora, no marca — compró pack Pro $119.000/200 leads y está evaluando CRM a $39.000/mes precio fundador) y Hierbas & Esencias (compró 120 créditos, aún sin usar). **Insight de ICP validado:** el mejor cliente de Gondola es la distribuidora (compra recurrente, presupuesto, multi-rubro), no la marca chica ni el done-for-you self-serve.

**Pivote previo relevante (9-jul-2026):** Gondola intentó reclutar dietéticas para que "opten in" (dejen su WhatsApp voluntariamente) en vez de scrapearlas en frío, porque el outreach frío tenía datos podridos (números fijos marcados como WhatsApp) y cero respuesta. Se lanzó landing `gondola.ar/sumate` + campaña de mail a la base propia de Smart Foods (538 dietéticas, relación previa).

**Resultado de ese pivote, medido hoy:** **538 emails enviados → 8 opt-ins totales (2 en los últimos 7 días) → ~1,5% de conversión.** El canal de entrega funciona bien (sin problemas de deliverability); el mensaje era genérico ("te quiero sumar a algo que armamos para dietéticas" + promesa vaga de "marcas nuevas, mejores precios, consignación"). Este dato es el disparador de todo lo que sigue: la oferta actual no es lo bastante concreta para que una dietética se moleste en sumarse.

## 2. El problema real (hipótesis de origen de esta rama)

Dos dolores que hoy Gondola no resuelve y que podrían ser la base de una propuesta de valor genuina para las dietéticas:

1. **Ruido, no falta de acceso.** Las dietéticas ya reciben demasiadas propuestas de marcas nuevas por WhatsApp y mail, sin tiempo ni criterio para filtrarlas. Ofrecerles "más acceso a marcas" (la propuesta original de `/sumate`) ataca el problema equivocado — puede incluso sonar a más de lo mismo que ya les sobra.
2. **Descubrimiento de demanda real.** Las dietéticas no tienen forma sistemática de saber qué les pide su propio cliente (qué producto buscan y no consiguen) más allá de la intuición del mostrador.

## 3. La propuesta — evolución dentro de esta conversación

### V1 (descartada en la conversación): "vidriera + ficha gratis"
Ofrecerle a la dietética más visibilidad hacia las marcas + un informe gratis de cómo la ve el mercado. Se descartó como insuficiente porque no resuelve el dolor real (ruido) y porque la pieza más persuasiva (consignación/mejores precios) requeriría que Gondola garantice condiciones comerciales que no controla.

### V2: Curación en vez de acceso
Idea del usuario: que Gondola ayude a la dietética a **encontrar lo que el consumidor realmente pide**, reciba ofertas de marcas de forma centralizada, y solo vea propuestas alineadas con lo que busca — no bombardeo. Mejora sobre V1 porque el "pago" de Gondola no es prometer condiciones comerciales, es prometer curación (que sí controla).

### V3 — Versión final a revisar: cuenta propia + bandeja de propuestas + verificación como diferenciador
Aclaración del usuario sobre V2: no es que Gondola centralice y reenvíe todo junto, sino que:

- **Cada dietética tiene login propio dentro de la app Gondola** (hoy no existe — hoy la dietética es un registro pasivo, no un usuario).
- Dentro de su cuenta hay una **"bandeja de entrada"** con propuestas de marcas.
- La dietética puede **marcar qué tipo de productos/categorías quiere incorporar** (preferencia declarada, filtra lo que le llega).
- Las marcas pueden ofrecer **propuestas diferenciales/exclusivas a dietéticas verificadas en Gondola** (verificación como estatus que desbloquea mejores condiciones).
- Objetivo explícito del usuario: que sea **ganar-ganar-ganar** — dietética, marca y Gondola.

Esta es la versión que se pide revisar.

## 4. Refinamientos propuestos durante el análisis (a validar, no son decisión tomada)

Estos puntos los aportó el asistente durante la conversación — se marcan aparte porque el agente revisor debería evaluarlos con el mismo escepticismo que al resto:

1. **Arquitectura espejo de un producto que ya existe.** Gondola ya construyó (19-jul-2026) "Gondola CRM": cuenta con login + tablero kanban de estados, vendido a Kaizen a $49.000/mes ($39.000 precio fundador). Es el mismo patrón técnico (cuenta, autenticación, objeto con estados) aplicado hoy a "leads que la distribuidora gestiona". La propuesta de este brief sería el espejo: "propuestas que la dietética recibe". La hipótesis es que gran parte del esqueleto (auth, gating de suscripción/plan, UI de estados) es reutilizable, no hay que diseñarlo de cero.
2. **Verificación como gate de acceso — con una deuda a saldar antes.** Hoy existe verificación real de WhatsApp (proveedor CheckNumber.ai, validado empíricamente: 552 números reales, 78% con WhatsApp confirmado, 0 discrepancias contra control manual). PERO: en un incidente reciente (17-jul-2026) se detectó que el sistema de facturación a marcas NO distingue entre WhatsApp verificado y WhatsApp simplemente inferido — cobra créditos igual en ambos casos, pese a que a un cliente (SIP) se le había comunicado lo contrario. Fue decisión consciente de negocio no corregirlo por ahora (no bug, decisión tomada). Si "verificada" pasa a ser una promesa pública hacia la dietética (acceso a mejores ofertas), esta inconsistencia deja de ser un detalle interno y se vuelve una promesa de cara al usuario — se recomienda resolverla antes de construir el gate.
3. **Tope de frecuencia como garantía estructural anti-ruido.** Sugerencia: además del filtro por categoría, un límite explícito ("máximo N propuestas por semana") como promesa dura y fácil de comunicar, no solo un filtro temático que en teoría podría seguir siendo mucho volumen.
4. **Canal de notificación vs. canal de configuración.** Hipótesis: el dueño/a de dietética probablemente no entra a revisar una app todos los días (perfil de usuario de bajo uso de herramientas digitales, según lo observado con el equipo de Kaizen). Sugerencia: WhatsApp como canal de aviso ("tenés una propuesta nueva alineada con lo que buscás"), la app como lugar de configuración inicial (preferencias, verificación) y de detalle/decisión — no como el único punto de entrada.
5. **Riesgo de canibalizar a las distribuidoras (caso Kaizen).** Kaizen es hoy el mejor cliente de Gondola y es justamente una distribuidora que vende a ~200 dietéticas. Si las marcas pueden ofrecer trato directo a dietéticas verificadas dentro de la app, existe el riesgo de desintermediar el canal que la propia Kaizen usa para vender. Resolución propuesta (no validada): que la bandeja de propuestas no sea exclusiva de "marca directa", sino que cualquier vendedor —incluidas distribuidoras— pueda publicar propuestas ahí, convirtiendo la bandeja en un canal adicional para Kaizen en vez de un competidor.
6. **Modelo de cobro sugerido:** la dietética nunca paga por estar en la red (su "pago" es dato + atención + preferencia declarada, que es lo que le da valor a la red frente a las marcas). La marca paga por propuesta publicada / matcheada / aceptada, no por volumen de contactos crudos. Esto se alinea con un riesgo ya identificado internamente en junio-2026 ("cobrás por volumen, el mercado quiere pagar por resultado").
7. **Secuencia sugerida:** no construir cuenta+login+bandeja completa como primer paso. Empezar con un MVP manual: agregar 2-3 campos de preferencia (categoría, criterio) al formulario `/sumate` que ya está en producción, y simular la "bandeja" curando a mano 1-2 propuestas por WhatsApp con 2-3 marcas activas. Si eso mejora la conversión frente al 1,5% actual, recién ahí se justifica construir el producto completo.

## 5. Activos técnicos que ya existen (reducirían el costo de construir esto)

- **Captura de preferencia por categoría/criterio:** ya diseñada (aunque dormida) en un flujo de reclutamiento por WhatsApp Business API construido en julio: 9 categorías predefinidas + 3 criterios comerciales (margen / consignación / novedad), con columnas dedicadas para guardarlo por comercio. Hoy bloqueado por un trámite de aprobación de nombre de marca ante Meta, no por falta de diseño.
- **Señal de demanda real del consumidor ("voz del cliente"):** pipeline que extrae de reseñas de Google Maps (validado que funciona para dietéticas argentinas — a diferencia de Instagram, que está bloqueado por restricciones de acceso de Meta a scraping no autenticado) qué mencionan/piden los clientes reales. Hoy ese dato se le muestra únicamente a la marca que compra el lead — nunca a la dietética dueña del dato.
- **Motor de matching/calificación:** ya existe un sistema que puntúa comercios contra el perfil de una marca (posicionamiento premium vs. granel, marcas complementarias que ya vende, actividad, reputación). Diseñado para calificar leads hacia la marca; para esta propuesta habría que invertir el sentido (calificar propuestas hacia la dietética).
- **Verificación de WhatsApp real:** proveedor externo integrado y validado (ver punto 4.2).
- **Patrón de cuenta con login + estados/kanban + gating por plan:** ya construido y en producción para el lado marca/distribuidora (Gondola CRM).
- **Landing de opt-in en producción:** `gondola.ar/sumate`, formulario simple (nombre, comercio, WhatsApp, zona, email), sin campos de preferencia todavía.

## 6. Lo que es genuinamente nuevo (no existe hoy, hay que construirlo)

- Modelo de cuenta/autenticación para dietéticas como tipo de usuario (hoy solo existen cuentas de marca/distribuidora).
- Objeto "propuesta" estructurado del lado marca (categoría, zona, tipo de trato, condición comercial) — hoy una marca que compra en Gondola se lleva una lista de contactos y pitchea por su cuenta, no existe el concepto de "oferta publicada dentro de la plataforma".
- UI de bandeja de entrada + panel de preferencias para la dietética.
- Motor de matching invertido (propuesta → dietéticas que calzan), distinto del que ya existe (lead → marca).
- Corrección de la inconsistencia de "verificado" antes de usarlo como gate público (ver 4.2).
- Definición y medición de "propuesta matcheada/aceptada" como evento facturable (para el modelo de cobro sugerido en 4.6).

## 7. Datos de referencia (20-jul-2026)

- Opt-ins en la red hoy: 8 totales, 2 en los últimos 7 días.
- Campaña de reclutamiento a la base B2B propia: 538/538 emails enviados, ~1,5% de conversión a opt-in.
- Marcas activas reales en el sistema: ~25.
- Clientes pagos: 2 (Kaizen — pack + evaluando CRM; Hierbas & Esencias — créditos sin usar todavía).
- Costo marginal de enriquecimiento por comercio (Gemini + Places): del orden de USD 0,02-0,03.
- Verificación WhatsApp: ~78% de hit rate sobre números inferidos, validado sobre 552 números reales.

## 8. Preguntas específicas para el agente revisor

1. ¿Es prematuro diseñar/construir cuenta + login + bandeja completa con solo 8 opt-ins reales? ¿Qué umbral de liquidez (opt-ins, marcas con propuestas activas) sería razonable antes de justificar ese desarrollo?
2. ¿El riesgo de canibalizar el canal de las distribuidoras (caso Kaizen) es real, y la resolución propuesta (que también ellas publiquen propuestas) lo neutraliza de verdad o solo lo pospone?
3. ¿El modelo de cobro por "propuesta matcheada/aceptada" es operativamente medible sin fricción, o requiere instrumentación no trivial (cómo se define/verifica una "aceptación")?
4. ¿Hay una secuencia de validación más chica todavía que el MVP manual sugerido en 4.7?
5. ¿Riesgos de adopción/UX no contemplados, dado el perfil de usuario (dueños de dietética, bajo uso de herramientas digitales, tiempo escaso)?
6. ¿Riesgos legales o de compliance de que Gondola intermedie ofertas comerciales entre terceros (marcas y dietéticas) dentro de su plataforma — responsabilidad si una condición ofrecida no se cumple?
7. ¿Falta algún punto ciego relevante no cubierto en este brief?

## 9. Nota sobre vigencia de los datos

Este brief se armó reconstruyendo contexto de memoria conversacional (proyecto Gondola) al 20-jul-2026. Antes de tomar decisiones de inversión de desarrollo sobre esta base, verificar contra el estado actual del código y la base de datos de producción — varios de los datos citados (opt-ins, estado de aprobación de WABA, etc.) cambian día a día.
