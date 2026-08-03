---
date: 2026-07-17
type: analisis
tags: [gondola, lead-machine, kaizen, ventas, dfy, icp, advisor]
status: activo
derivado_de: kaizen-primer-cliente-2026-07-16
---

# Kaizen — Lectura post-reunión (call 17/07) + insights de producto y escalamiento

Análisis de la grabación real (transcript limpio en `~/Downloads/kaizen-17jul-transcript/`). Companion de [[kaizen-primer-cliente-2026-07-16|la prep note]]. No repite lo ya decidido (fit, precios, modelo cazador, P0). Se enfoca en: qué cambió la call, insights de app, e ICP para escalar.

---

## 1. El reencuadre grande: no es upsell de crecimiento, es tabla de salvación

La prep leyó el DFY como "abrirles bocas nuevas sin frenar la operación". La call revela algo más urgente y más personal:

> *"mi madre es la que se encargaba de eso y tuvo una caída hace como un mes… tienen que hacerse una cirugía. Está complicada y la verdad que mucho tiempo no tenemos."*

**Margarita ES el motor de ventas de campo** (4 años y medio visitando clientes, ella misma lo dice: *"la que ha estado aquí en venta directamente cara a cara he sido yo"*). Está lesionada y va a cirugía. El canal mayorista de Kaizen se quedó, literalmente, sin fuerza de ventas.

Consecuencias:
- La demanda del DFY no es "queremos crecer", es **continuidad de negocio con miedo**. Willingness-to-pay mucho más alta.
- **Pero está atada a una condición temporal.** Cuando Margarita se recupere, ¿siguen? El piloto tiene que probar ROI *standalone* (cuentas nuevas abiertas), no "reemplazo de Margarita", para sobrevivir su vuelta.
- Ya te de-riskearon la alternativa "contratar vendedor": *"intentamos buscar vendedores pero no nos generaban la confianza"*. Su objeción a contratar es **confianza, no plata**. Y a vos te tienen confianza (el hijo te buscó, Margarita quiere "nutrirse" de tu experiencia). **Tu credibilidad personal es el producto.** Eso vende el DFY — y también es su techo (ver §5).

## 2. La web pública miente sobre el tamaño del cliente

Tu prep (mañana) describió Kaizen desde su web: *"reventa pura, dietética online chica, reabrió hace poco, sin sección mayorista visible"*. La call muestra otra cosa:

- Distribuidora hace **4,5 años**, **~200 dietéticas** cliente, fuerte en Capital (Belgrano/Palermo/Recoleta/Puerto Madero/Microcentro) + Zona Norte.
- Venden también por Mercado Libre + Tienda Nube, usan **Dux** (ERP con módulos de compra/tesorería/venta/stock).
- Operación de campo real con rutas. Coworkings de alto volumen. El hijo viene de **Mass Brownie** (fábrica, 10 años).

**Insight de calificación para escalar:** la vidriera B2C de una distribuidora es un pésimo proxy de su tamaño real. No descartes prospectos por web chica. El hijo se auto-calificó porque **el mail le pegó**, no por la web. (→ §4)

## 3. Insights de APP (ordenados por leverage)

1. **Excluir clientes existentes de la búsqueda** — fricción #1, prometida "hoy". Verbatim de Nelson: *"¿cómo hacemos para no gastar un lead en un cliente que ya es nuestro?"*. **Debe deduplicar por dirección, no por nombre**: *"tenemos un Bon Natural que tiene cinco sucursales y le vendemos a todas"*. (En construcción.)

2. **El ícono de WhatsApp rojo/verde: es UX confusa Y un riesgo de integridad.** Nelson preguntó dos veces qué significa el rojo; tu respuesta fue difusa (*"puede que funcione, puede que no"*). Dos problemas:
   - **UX:** el significado no es evidente. Falta leyenda/tooltip.
   - **Economía + garantía:** tu promesa es "solo pagás los que tienen WhatsApp". Pero "tiene un campo de WhatsApp" ≠ "el WhatsApp funciona". Si un lead **rojo** descuenta crédito y el número está muerto, pagaron por un lead muerto → contradice tu propia garantía. **Es exactamente lo que Nelson está rodeando con la pregunta.** Recomendación: que el crédito se consuma solo en **verde (verificado activo)**, o que el rojo sea gratis hasta verificar. Si lo descubren ellos, te cuesta la confianza que es TODO tu producto. (El mapeo de código está verificando la lógica real.)

3. **"Nos vamos a quedar cortos de leads" es un momento de producto, no solo un upsell.** *"esos 200 me parece que se nos van a quedar corto, hay que planificar más leads."* Hacé el top-up sin fricción y visible el nudge de "te estás quedando corto". Y ojo al patrón estratégico: una distribuidora **recompra leads todos los meses** (a diferencia de una marca que prospecta una vez). Eso es recurrencia. (→ §4)

4. **Doblá la apuesta en Gondola-como-CRM; matá el export a Dux.** Usan Dux pero **no como CRM**, y no tienen CRM (*"no tengo tanta experiencia con CRM"*). Ofreciste adaptar un export al formato de su CRM — dirección equivocada: laburo de integración a medida para algo que no usan. La call muestra que **aman el seguimiento nativo** (*"el seguimiento nos gusta mucho… no es tan prolijo como esto"*). El pipeline propio de Gondola ES su CRM comercial: más barato de construir, más pegajoso (lock-in), y es lo que quieren. Descartá el export a Dux.

5. **Onboarding: pedí el perfil mayorista explícito, no lo infieras de la web B2C.** La inferencia de ICP lee la tienda del cliente; la de Kaizen (B2C) los hace ver chicos y ensucia los icebreakers de WhatsApp. El onboarding debería preguntar directo: marcas que llevan, márgenes, zonas, rubros target. Mejora el fit-score y los mensajes.

6. **Percepción de confiabilidad.** En la call hubo varios "ahora no anda": el "da cero" de ayer (billing Gemini, ya resuelto), *"estaba actualizándose y no estaba activo"*, el "generar informe" con error. Todo explicable, pero para un cliente pago de referencia, **estabilidad > features**. Mandá un WA proactivo: "el error de ayer ya está arreglado, probá de nuevo". Y ojo: el deploy de esta feature (+ el P0 de seguridad pendiente) **invalida sesiones → Kaizen re-loguea**. Avisales.

## 4. ICP para escalar: el mejor cliente de Gondola es una DISTRIBUIDORA, no una marca

La call es evidencia fuerte de que las distribuidoras del canal salud le ganan a las marcas individuales como ICP:

| Dimensión | Marca individual | Distribuidora (Kaizen) |
|---|---|---|
| Demanda de leads | Prospecta su canal una vez | **Prospecta siempre** (*"todos los meses estamos buscando"*) → recompra |
| Presupuesto | A menudo sin caja | Ya paga ads ML + Meta, mentalidad ROI (*"si el presupuesto da, avanzar"*) |
| Rubros / uso | 1 tipo de PDV | Dietéticas + coworkings + gimnasios + farmacias → más uso de la app |
| Comprador de DFY | Rara vez tiene fuerza de campo | **La tiene y es cara/frágil** → el DFY existe para esto |

**Señales de prospecto "tipo Kaizen":** vende mayorista al canal dietética/salud · portafolio multimarca (reventa), suma marcas seguido · presente en ML + Tienda Nube/Shopify (ecommerce-native = cómodo con herramientas, con budget) · establecido 2+ años, chico, dueño-operado, sin tiempo · dependiente de ventas de campo (rutas/visitas).

**Anti-señal:** NO califiques por el tamaño de la vidriera B2C (miente, §2).

**Cómo encontrarlas (canales que YA funcionaron):**
- **El mail frío funcionó.** El hijo: *"cuando me mandaste el mail me identifiqué totalmente porque es lo que yo hago también"*. El mensaje espejaba su dolor diario exacto (Google + WhatsApp + armar rutas). **Ese message-market fit es el activo** — sistematizalo: lista de distribuidoras del canal + mismo mail espejo.
- **Fuente de la lista:** Gondola misma puede buscar rubro "distribuidora suplementos / mayorista dietética". Las marcas que las distribuidoras revenden (Natural Nutrition, Muscle Pro, Natier, ENA, Wake Up, Vitalgy, Lappiel…) publican su red de distribuidores / "dónde comprar" → scrapealas. Grupos de WhatsApp del sector (mencionaron uno). Ferias de suplementos.
- **Referido intra-sector:** Kaizen contenta conoce otras distribuidoras. Y tu servicio de curación de marcas te conecta con marcas que conocen sus distribuidoras. Cross-pollinizá.

**Reframe del wedge:** Gondola no es "herramienta de leads". Es **"el motor comercial tercerizado para distribuidoras del canal salud sin tiempo"**. La app es el tier de entrada (Pro), el DFY el tier alto (cazador). Mismo ICP, dos precios. Kaizen recorrió toda la escalera en una call. **Esa es la secuencia repetible: mail → Pro → (siente el dolor de labor) → DFY.**

El momento de conversión al DFY es predecible: compraron una **herramienta** para resolver un problema de **labor**. Una herramienta no resuelve labor, la reubica. Van a descubrir que siguen sin nadie que mande los 200 WhatsApps ni haga las visitas (Margarita out). Ese "click" = momento DFY. Dejalos sentir el dolor ~2 semanas y ahí seguís. No cerrar mañana (ya lo tenías).

## 5. Puntos ciegos (para confrontar)

1. **Foco.** En UNA call ofreciste: app Gondola, DFY equipo de ventas, curación/representación de marcas, laboratorio de tinturas de Entre Ríos, y conectar marcas con dietéticas. Kaizen es comprador tibio de TODO — es seductor, pero sentás el precedente "Andrés nos hace todo". Si te volvés su brand-sourcer + equipo de ventas + vendor de tool, **reconstruiste el laburo de operador que estás tratando de dejar, para la empresa de otro.** Mi recomendación: **el negocio es Gondola (tool) + DFY (servicio).** La curación de marcas es profundizador de relación / motor de referidos, no una línea paga todavía. No la dejes comerse el foco.

2. **La confianza no escala como el software.** Toda la venta descansa en que a VOS te tienen confianza (rechazaron vendedores anónimos). El "equipo" del DFY sos vos + Flor. A 4 marcas, el modelo cazador te necesita como cara confiable 4x simultáneas. Techo real. **La app escala; el DFY no** — precialo como servicio boutique escaso (pocos clientes, precio alto), no como producto a vender en volumen. Dejá que la escala la haga la app.

3. **Kaizen es cliente de referencia, no de margen — cuidá el impuesto de soporte.** Ya generaron ~4 pedidos de build en una call (exclusión, más leads, export CRM, claridad del ícono) y tienen línea directa con vos. Los primeros clientes son demandantes. **Regla: solo construí lo que generaliza a todas las distribuidoras** (exclusión: sí, todas la necesitan; export a Dux: no, one-off). 

4. **Estabilidad antes que features.** Primera impresión con varios "ahora no anda". Para el cliente pago de referencia, un deploy que rompa algo en su cuenta vale más que cualquier feature nueva. Bundleá el P0 + esta feature con cuidado y verificá su cuenta post-deploy.

---

## Acciones (yo / esta semana)
- [x] **HECHO 17/07:** sección "Cargar clientes" construida y DEPLOYADA a prod (tabla `brand_clients`, endpoints `/api/clients*`, UI en Buscar, matching laxo nombre+dirección, excluye del pool + Places + peek, 8 tests). Verificado en browser end-to-end y cuenta Kaizen intacta post-deploy (196 créditos).
- [x] **CONFIRMADO en código:** el WhatsApp rojo SÍ descuenta crédito (`_save_leads` cobra con que el campo `whatsapp` no esté vacío, sin mirar verde/rojo). → decisión de pricing PENDIENTE de Andrés: cobrar solo al validar verde, o dejar y absorber reclamo.
- [ ] WA a Kaizen: feature lista + re-login (deploy invalidó sesiones) + error de ayer arreglado. Borrador entregado a Andrés 17/07.
- [ ] Descartar formalmente el export a Dux; documentar Gondola-como-CRM como el camino.
- [ ] Sistematizar el mail-espejo para conseguir más distribuidoras (lista + secuencia).

Relacionado: [[kaizen-primer-cliente-2026-07-16]] · [[estrategia-freemium]] · [[brand-gondola]] · [[../growth-b2b-canal-dieteticas/index|Growth B2B canal dietéticas]]
