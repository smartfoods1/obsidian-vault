---
date: 2026-05-31
type: technical-spec
tags: [salto-cuantico, korean-root, whatsapp, meta-templates]
status: ready-for-meta-submission
---

# Salto Cuántico — Templates WhatsApp para Meta Business Manager

Templates listos para cargar en Meta Business Manager (Korean Root WABA). Los 4 listados acá no dependen de assets pendientes (M1 espera meditación grabada, M3 espera video modo de uso).

**Idioma**: español (Argentina) → código `es_AR`
**Categoría**: MARKETING (los 6 son post-venta promocional)
**WABA**: la registrada en el bot KR actual
**Tiempo estimado de aprobación**: 24-48 hs por template

---

## Conventions

- `{{nombre}}` = `{{1}}`, `{{2}}`, etc. en Meta — los voy listando en orden
- "Bienvenida/o" se inyecta como variable (no escribir variantes hardcodeadas)
- "cuántica/o" igual
- Cierre estándar: `— Viqui, KR` (no variable)

---

## 1. `sc_m2_pre_entrega` — 1 día antes de recibir

**Categoría**: MARKETING
**Header**: ninguno
**Botones**: 1 botón URL → al portal

### Body

```
{{1}}, toda transformación primero es silenciosa, sutil, hasta que un día aparece algo que podés nombrar, ver, sentir...

Por eso creamos *DESAFÍO SALTO CUÁNTICO*, un programa para ayudarte a que veas los movimientos que están sucediendo en tu vida.

Me encantaría que lo completes con honestidad y presencia.

Luego de tomar {{2}} por un tiempo, te voy a invitar a volverlo a responder para que tengas una referencia de tus cambios en cada aspecto de tu vida.

— Viqui, KR
```

### Variables
- `{{1}}` = `name_first` (ej. "Mariana")
- `{{2}}` = `product_phrase` (ej. "Limonada Cuántica" o "Limonada Cuántica y Shakti Booster")

### Botón URL
- **Tipo**: URL dinámica
- **Texto del botón**: `Empezar el quiz`
- **URL base**: `https://103-199-187-246.nip.io/salto-cuantico/portal/`
- **Variable URL**: `{{1}}` = slug del cliente (ej. `victoria-m-9c5pck`)

---

## 2. `sc_m4_opinion` — 11 días después de recibir

**Categoría**: MARKETING
**Header**: ninguno
**Botones**: 1 botón URL → reviews Google

### Body

```
Hola {{1}}, ya pasó más de una semana desde que incluiste {{2}} en tu vida.

Dale tiempo y espacio a tu cuerpo. Los hábitos son la forma que tenés de programar y elegir tu vida, tu energía y tu destino.

Lo estás haciendo bien.

Me encantaría leer tu opinión. Cuando puedas, dejame unas líneas contándome cómo te estás sintiendo:

— Viqui, KR
```

### Variables
- `{{1}}` = `name_first`
- `{{2}}` = `product_phrase`

### Botón URL
- **Tipo**: URL estática
- **Texto**: `Dejar mi opinión`
- **URL**: `https://g.page/r/<...>/review` (Andrés/Viqui pasar la URL exacta del perfil Google de KR)

---

## 3. `sc_m5_recalibracion` — 22 días después de recibir

**Categoría**: MARKETING
**Header**: ninguno
**Botones**: 1 botón URL → portal (quiz Q2)

### Body

```
{{1}}, ¿sabías que el cerebro tarda 21 días en crear un nuevo surco neuronal y adoptar un nuevo hábito?

Si tomaste {{2}} hasta hoy, *felicitate*: transformaste una acción en parte de tu identidad. Tu cuerpo ya se acostumbró a funcionar desde un nuevo nivel de bienestar.

Y como estás en pleno SALTO CUÁNTICO, te dejo tu segundo test de evolución para que puedas comparar tus cambios reales desde el día 1.

Tu {{2}} se debe estar por terminar. Para que lo puedas continuar sin interrupciones, te dejo un código de descuento exclusivo:

🎁 *{{3}}* — válido 7 días

— Viqui, KR
```

### Variables
- `{{1}}` = `name_first`
- `{{2}}` = `product_phrase`
- `{{3}}` = `coupon_code` (ej. `SC-VICTORIA-M5-9D33VD`)

### Botón URL
- **Tipo**: URL dinámica
- **Texto del botón**: `Hacer el segundo test`
- **URL base**: `https://103-199-187-246.nip.io/salto-cuantico/portal/`
- **Variable URL**: `{{1}}` = slug del cliente

---

## 4. `sc_m6_un_mes` — 30 días desde la compra

**Categoría**: MARKETING
**Header**: ninguno
**Botones**: ninguno (es un mensaje de cierre, código en el body)

### Body

```
{{1}}, oficialmente cumpliste un mes eligiéndote, y eso no es poca cosa.

Felicitate. Honrate. Mirá para atrás un segundo: decidiste invertir en vos y reprogramaste tus células, creaste un hábito y una realidad distinta.

La constancia es el puente entre tus deseos y una nueva realidad.

Si todavía no repusiste tu aliado de bienestar, te dejo otro cupón para que no cortes el proceso. Lo ideal sería que sigas al menos 3 meses más:

🎁 *{{2}}* — válido 7 días

— Viqui, KR
```

### Variables
- `{{1}}` = `name_first`
- `{{2}}` = `coupon_code` (ej. `SC-VICTORIA-M6-K8H2QF`)

---

## Templates pendientes de asset

### 5. `sc_m1_bienvenida` — bloqueado por **meditación M1**

Esperando que Viqui grabe y suba la meditación "reprogramar células". Cuando esté:
- Si la subimos a YouTube → el template puede ser solo texto + URL en el body
- Si tenemos el archivo mp3/ogg < 16MB → podemos usar header AUDIO en el template

### 6. `sc_m3_recepcion` — bloqueado por **video modo de uso**

Esperando video genérico de Viqui (60-90s, MP4 vertical, ≤16MB) explicando los 3 productos. Va como header VIDEO del template.

---

## Cómo cargar en Meta Business Manager

1. Entrar a Meta Business Suite → WhatsApp Manager → Plantillas
2. Click "Crear plantilla"
3. Categoría: **Marketing** (no Utility — son promocionales)
4. Idioma: **Spanish (ARG)** — `es_AR`
5. Nombre: usar exactamente el del header de cada sección arriba (snake_case)
6. Copiar el body
7. Agregar el botón URL si corresponde con la URL base y la variable dinámica
8. Enviar para revisión

Una vez aprobado por Meta, marcar el item correspondiente en el checklist Salto Cuántico admin como OK y cambiar `dispatcher_mode` de `dry_run` a `live` desde el panel.

---

## Validación pre-envío

El backend ya está generando estos payloads exactos en modo dry-run. Para verificar lo que va a salir, correr:

```bash
ssh root@103.199.187.246 "/opt/journey-venv/bin/python3 /tmp/sc_template_preview.py"
```

Eso muestra el JSON exacto que el dispatcher va a postear a Meta para cada template, así Viqui o vos pueden confirmar el copy palabra por palabra antes de cargarlos en el Business Manager.
