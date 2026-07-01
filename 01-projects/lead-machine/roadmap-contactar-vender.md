---
date: 2026-06-21
type: roadmap
tags: [lead-machine, saas, b2b, producto, ventas, roadmap]
status: activo
derivado_de: handoff.md
---

# Lead Machine — Roadmap contactar→vender

> Salida de un análisis multi-agente (19 agentes: 4 personas reales + 7 dimensiones + verificación adversarial de cada gap contra el harness + síntesis). Jun 21 2026.
> **🟢 Estado (jun 21): COMPLETO. Modelo B decidido + P0, P1 y P2 los tres DEPLOYADOS, verificados en prod y commiteados a git (`main`, commit c83e4d4).** Detalle en `project_lead_machine.md` v12 (P0) + v13 (P1) + v14 (P2). Pendiente fuera de roadmap: rotar creds MP/Google, validar webhook MP con pago real.
>
> **Lecciones (no repetir):**
> - **WhatsApp:** Google Places NO trae el prefijo "15" (móvil≡fijo, `011 XXXX-XXXX`) → `_infer_whatsapp` normaliza a +549 SIEMPRE y ofrece el botón (atenuado si no hay señal real), nunca lo apaga.
> - **Billing/cuota:** cobrar solo leads nuevos exige enriquecer solo leads nuevos (`_split_candidates`), o re-buscar una zona guardada gasta Gemini/Places gratis e ilimitado.
> - **Timezone:** VPS en UTC, el user fija fechas en hora AR → `today` en ART (`gmtime(now-3h)`), snooze del front con componentes locales (no `toISOString()`); `new_7d`/`cutoff7` en UTC (= base de created_at).

## Diagnóstico en una línea

Lead Machine resuelve de diez **encontrar + calificar + organizar**, y se corta exactamente donde se hace la plata mayorista: **contactar con un mensaje que cierre, seguir a los que no contestan, y saber si cerraste.** Las 4 personas (dueño de marca chica, comercial de calle, sales manager, churn/KR) coincidieron: "gran buscador de listas, no máquina de ventas" → la usan una vez por zona y no vuelven. Un producto que se usa cada tanto no sostiene un mensual.

## El fork de negocio (decisión de Andrés, previa al código)

El problema de fondo no lo arregla ninguna feature: **se cobra por VOLUMEN de leads (packs one-off), pero el mercado quiere pagar por RESULTADO de venta.** Hay que elegir:

- **(A) Negocio transaccional de listas** — seguir vendiendo packs. Simple, techo bajo, churn estructural (KR sacó 30 y no volvió).
- **(B) CRM de venta mayorista de récord** — el mensual ES el producto, los packs son la rampa. El valor es "tu pipeline vive adentro y te dice a quién perseguir hoy". Única forma de justificar recurrencia.

El roadmap habilita (B) sin romper (A). Si no se va a (B), el P1 es plata tirada. **Recomendación: apuntar a (B).**

## Qué construir primero

**El mensaje que vende + el seguimiento fechado**, como una atómica deployable:

1. `wholesale_offer` por marca (precio mayor, mínimo, margen para el local, muestra, condiciones) en **una columna de texto libre** (no sub-schema), inyectada al prompt del icebreaker pidiéndole a Gemini cerrar **con números pero en una línea**. Convierte "creo que encajamos" en "te dejo 45% de margen y arrancás sin mínimo". S de esfuerzo, impacto 5. La bisagra.
2. Migración aditiva compartida sobre `saved_leads`: `outcome`, `last_contacted_at`, `next_action_at` (todas `TEXT DEFAULT ''`, tolerantes a `OperationalError`).
3. El botón de WhatsApp registra el toque (`last_contacted_at` + sube a `contactado` solo si estaba en `nuevo/visitar`).

## Roadmap

### P0 — De buscador a máquina de cierre (1 sprint)
Una migración, un PATCH extendido, sin tocar el camino caliente de `/api/leads`.
- Oferta mayorista inyectada al icebreaker.
- Email + Instagram en el *mismo* prompt de enrich (costo marginal cero) + `mailto:` espejo del `wa.me`.
- WhatsApp honesto: clasificar móvil vs fijo, no renderizar botón verde a chat muerto, matar el fallback a teléfono crudo en `waLink`.
- Estados de OUTCOME acotados a 5 (`respondió/interesado/cotizado/ganado/perdido`), eje separado de la actividad.
- Demo pre-login `/api/detect-demo`: mostrar el "ajá" sin cuenta ni créditos (reusa bucket `detect`).

### P1 — A quién persigo HOY (1 sprint, retención = lo que paga el mensual)
- `next_action_at` + orden/facet "vencidos primero" (calculado on-read en Python, sin cron) + atajos +3d/+1sem.
- `sort='accion'`: cola de próxima mejor acción (fit + estado + antigüedad del toque).
- Editar el icebreaker antes de mandarlo, persistido en columna dedicada `message_override` (NO en `data`).
- No cobrar leads que la marca ya tiene (queja literal de KR): cobrar solo `place_key` nuevos, dentro del lock existente.
- Badge `new_7d` reusando `created_at` (sin migración) + paywall con copy por resultado.

### P2 — Cierre del loop (oportunista, no bloquea)
- `deal_value` + mini-resumen "Ganado $X · En pipeline $Y". Nada por-rep, nada gráficos.
- Generador del segundo mensaje / toque N bajo demanda (1 lead/llamada).
- Arreglar el copy mentiroso del cluster ("asigná un vendedor" cuando no hay vendedores).

## Qué NO construir (anti gold-plating)

- **Multi-usuario / roles / login por rep** — L, toca el corazón de la auth (`sign(brand_id)`) en una app viva que ya corrompió la DB 2 veces. Buyer real (KR, Plante) es 1-3 personas sin sales org.
- **Cron de re-corrida automática de búsquedas** — mete infra operativa nueva y re-corre Places+Gemini gastando créditos sin botón → choca con el lock anti-doble-gasto.
- **Optimizador de "Mi ruta de hoy"** — máxima superficie de front por el menor impacto en cerrar.
- **Dashboard de ROI por rep/zona, multiplicadores inventados en el paywall, tours con librería** — gold-plating.

## Dos minas técnicas para implementar P0

1. El loop de `ALTER` de `app.py:358` cubre **solo `brands`**. Las columnas nuevas de `saved_leads` necesitan su **propio** loop `ALTER`, o no se crean en la DB de prod (existe con `CREATE TABLE IF NOT EXISTS`) y el PATCH falla en silencio.
2. **Nunca** persistir un campo editable (icebreaker editado) dentro de la columna `data`: el UPDATE del UPSERT en `app.py:614` la pisa entera en cada re-búsqueda de zona. Columna dedicada, como `status`/`notes`.

Y siempre: `./run-tests.sh` → `./deploy.sh`, nunca a mano.

## Riesgo principal

El roadmap, perfecto, deja igual al usuario comprando "una tanda de lista" si no se ata la recurrencia (P1) a una suscripción por **actividad de venta**, no por volumen. Sin eso, seguís vendiendo listas, no software.
