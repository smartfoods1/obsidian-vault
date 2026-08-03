---
date: 2026-07-20
type: revision
tags: [gondola, red-comercios, dieteticas, product-strategy, decision]
status: final
derivado_de: "[[01-projects/lead-machine/red-comercios-adheridos-brief-2026-07-20|Brief red de comercios adheridos]]"
---

# Revisión — Red de comercios adheridos (V3)

## Veredicto

La V3 es coherente y es la mejor de las tres versiones: el "pago" de Gondola es curación (que controla) y no condiciones comerciales (que no controla). Pero tal como está planteada tiene tres problemas:

1. **Error de interfaz**: cuenta + login + bandeja en la app para un usuario que el propio brief describe como de bajo uso digital. La dietética no va a entrar nunca. El lado dietética debería ser 100% WhatsApp-native; la única UI nueva que se justifica es del lado oferente (publicar propuestas), que reusa el esqueleto del CRM.
2. **Error de secuencia**: se está diseñando la demanda (bandeja, preferencias, matching) cuando el lado escaso es la OFERTA. Hoy hay ~25 marcas, 2 pagaron, 1 ni usó los créditos. ¿Quién publica propuestas con condiciones diferenciales reales? Sin eso, la bandeja nace vacía y la promesa anti-ruido muere en la primera semana.
3. **Punto ciego de costo de oportunidad**: el brief valida en su propia sección 1 que el ICP es la distribuidora (paga hoy, recurrente). La red monetiza recién con liquidez, dentro de meses. Con la atención de Andrés repartida (disolución SF, KR, PGN, agencia growth), duplicar en el camino distribuidora domina; la red debería ser subproducto de eso, no apuesta principal.

**Recomendación**: no construir producto todavía. Test manual esta semana con los 8 opt-ins existentes, usando el portfolio de Kaizen como primera oferta — un solo movimiento que testea demanda, resuelve el cold start de oferta y convierte el riesgo de canibalización en sociedad.

## Respuestas a las 8 preguntas

### 1. ¿Prematuro construir con 8 opt-ins?

Sí, sin ambigüedad. Umbral razonable antes de escribir código: **~100 opt-ins con preferencia declarada + ≥5 oferentes con propuestas activas concretas + matching manual mostrando ≥30% de respuesta**. Hoy: 8 / ~2 / sin dato. Y aún cruzado el umbral, lo que se construye no es lo que dice el brief: lado dietética = WhatsApp (captura de preferencias por conversación — el flow WABA con 9 categorías + 3 criterios ya está diseñado), lado oferente = UI de propuestas sobre el esqueleto CRM. La "cuenta de la dietética" puede ser una fila en la DB + un hilo de WA durante mucho tiempo.

### 2. ¿Canibalización de Kaizen?

Real como riesgo de **percepción**, limitado como riesgo material. Las marcas chicas no pueden servir dietéticas directo (logística, mínimos, cobranza, reposición) — por eso existen las distribuidoras; Gondola no hace fulfillment. Pero Kaizen no necesita perder ventas para churnear: alcanza con que vea a Gondola construyendo un canal que la puentea, y Kaizen es hoy ~100% del revenue recurrente.

La resolución propuesta ("que las distribuidoras también publiquen") **pospone, no neutraliza**: le pedís a Kaizen que pague por competir en una subasta por cuentas que considera suyas, cuando su alternativa es seguir vendiendo como hoy. Lo que sí neutraliza: dar vuelta el framing — la bandeja como **demand-gen para distribuidoras**. La dietética declara "quiero incorporar X", Gondola rutea esa demanda a quien puede servirla, distribuidoras con CRM pago tienen first look. Kaizen pasa de amenazado a beneficiario. Honestidad estratégica: un marketplace marca↔dietética ES competitivo con distribuidoras a largo plazo; se puede secuenciar alrededor del conflicto, no eliminarlo.

### 3. ¿"Propuesta matcheada/aceptada" es facturable sin fricción?

No como está definido. "Aceptada" ocurre fuera de la plataforma (conversación de WA → pedido telefónico → entrega); no es verificable sin datos de facturación que Gondola no tiene. "Matcheada" es medible pero el matching lo controla el propio algoritmo de Gondola — facturar sobre un evento que vos mismo generás es un conflicto de interés que un cliente va a impugnar (incentivo a sobre-matchear).

Lo operativamente medible hoy: **"interés declarado / contacto desbloqueado"** — la dietética toca "me interesa" en WA y la marca recibe el contacto + contexto. Es el modelo clásico de lead fee, y el tracking `contact_events` ya está en prod. No prometer nunca "pago por venta concretada".

### 4. ¿Secuencia más chica que el MVP del brief?

Sí, dos escalones más abajo:

1. **Esta semana, cero código**: llamar/escribir por WA a los 8 opt-ins. Dos preguntas: "¿qué categoría querés incorporar?" y "¿qué te pide tu cliente que no conseguís?". Curar a mano 1 propuesta por dietética desde el portfolio de Kaizen (vendiéndoselo a Kaizen como demand-gen gratis). Medir: respuesta → reunión → pedido.
2. **Ojo con la lectura del 1,5%**: se midió con mensaje genérico, por email, desde la base de una marca en disolución. No prueba que la oferta V3 no funcione; prueba que ese mensaje por ese canal no funciona. Antes de concluir, probar reclutamiento con hook concreto — y el hook más fuerte ya está construido: el **informe "voz de tu cliente"** (reviews de Maps del propio local), que hoy solo ve la marca compradora. "Esto es lo que tus clientes dicen que buscan y no encuentran en TU local" es personalizado, gratis y demuestra el valor de la red en el primer mensaje. La V1 se descartó por la promesa de consignación, no por el informe — recuperar esa pieza.

### 5. Riesgos de adopción/UX no contemplados

- **El mute de WhatsApp es muerte con un tap.** La promesa anti-ruido es frágil: UNA propuesta mala y Gondola queda recategorizado como el spam del que decía diferenciarse. El cap de frecuencia inicial debe ser brutal: 1-2 propuestas por MES, no "N por semana".
- **La preferencia declarada se pudre.** Lo que la dietética marcó en julio no es lo que busca en octubre (estacionalidad, moda de ingredientes). Cada notificación debe doblar como refresh de preferencia ("¿seguís buscando X?").
- **Circularidad de "verificada"**: el estatus no vale nada para la dietética hasta que existan condiciones diferenciales reales, y las marcas no ofrecen condiciones diferenciales hasta que haya dietéticas verificadas. Otro argumento para arrancar con Kaizen como oferta semilla.
- **Expectativa del lado marca**: con 8-50 dietéticas, la marca que publica una propuesta no recibe nada y churnea. No abrir el lado oferente a marcas frías hasta tener masa.

### 6. Riesgos legales/compliance

- **Plataforma, no parte**: T&C explícitos de que Gondola matchea y las condiciones comerciales son entre marca y comercio. No meterse en el medio del pago ni retener fondos — eso mantiene la exposición baja.
- **Datos personales (Ley 25.326)**: verificar que el consentimiento de `/sumate` cubra "recibir ofertas comerciales de terceros a través de Gondola". Si el texto actual no lo dice, agregarlo antes de rutear la primera propuesta.
- **Claims ANMAT**: si las propuestas incluyen claims de suplementos y Gondola las republica/rutea, comparte exposición. Regla mínima de moderación (no claims terapéuticos).
- **La inconsistencia verificado/facturación (incidente SIP, 17-jul)**: correcto lo del brief, y más — hoy es deuda interna, con "verificada" como promesa pública pasa a ser potencial misrepresentación hacia clientes pagos. Y ya hay un cliente al que se le comunicó algo que no es cierto. Arreglarla ya, independientemente de esta iniciativa.

### 7. Puntos ciegos del brief

1. **Overlap con el spin-off Greenco** (datos de canal: pedidos WA + sell-out, con Lionel Sauro como socio ancla). Son dos jugadas paralelas de red sobre LAS MISMAS dietéticas y el brief no lo menciona. Antes de invertir en cualquiera de las dos, decidir si son la misma cosa, complementarias o competencia interna por atención.
2. **El lado escaso es la oferta, no la demanda** (desarrollado en el veredicto).
3. **Métrica de éxito mal definida**: el brief propone comparar contra el 1,5% de opt-in. La métrica del MVP manual debe ser **tasa de respuesta/acción sobre propuestas curadas** (¿contestó? ¿se reunió? ¿pidió?), no reclutamiento. Son funnels distintos.
4. **El activo más diferenciado está sin usar como hook** (informe voz-del-cliente, ver pregunta 4).
5. **Qué es esto realmente**: una versión sistematizada de lo que hace el preventista de una distribuidora. El wedge defendible no es "acceso" ni "curación" — es el **dato de demanda** (qué piden los consumidores finales, agregado por zona/categoría). Ese dato, dicho sea de paso, es exactamente lo que el spin-off Greenco quiere vender. Otra razón para unificar las dos jugadas.

### 8. Secuencia recomendada

1. **Ya**: arreglar la inconsistencia verificado/facturación.
2. **Semana 1**: test manual con los 8 opt-ins + portfolio Kaizen (pregunta 4). Métrica: respuesta ≥30% y ≥1 pedido.
3. **Semana 1-2 en paralelo**: agregar 2-3 campos de preferencia a `/sumate`; probar reclutamiento con hook de informe personalizado (por WA cuando la WABA esté aprobada; mientras, email pero con el informe adjunto, no promesa vaga).
4. **Decisión Greenco**: definir si la red opt-in y el spin-off de datos son la misma iniciativa antes de escalar cualquiera.
5. **Solo si 2 y 3 validan**: construir lado oferente sobre esqueleto CRM + flujo WA para dietéticas. Nunca la app-para-dietéticas del brief.
6. **Mientras tanto, el negocio real**: vender CRM a más distribuidoras. Cada distribuidora cliente trae su cartera de dietéticas — la red se siembra desde el lado que ya paga, no desde reclutamiento frío.
