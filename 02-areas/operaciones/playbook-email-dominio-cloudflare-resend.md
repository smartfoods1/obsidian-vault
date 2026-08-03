---
date: 2026-07-04
type: playbook
tags: [email, dns, cloudflare, resend, dmarc, deliverability, infra]
status: activo
---

# Playbook — Email de un dominio: recepción (Cloudflare Routing) + envío (Resend) + anti-spoofing

Patrón reusable para dejar un dominio con **email completo** sin contratar Google Workspace. Aplicado por primera vez en `gondola.ar` (jul 2026). Sirve para cualquier marca/tenant nuevo.

## Arquitectura (la clave: recepción y envío NO se pisan)

- **Recepción** → **Cloudflare Email Routing**. MX + SPF + DKIM en el **root** del dominio. Reenvía `*@dominio` a una casilla real (ej. un Gmail). Gratis.
- **Envío** → **Resend**. Sus records van en el subdominio **`send.dominio`** (MX de bounces + SPF de Amazon SES) + DKIM en `resend._domainkey`. Como el MX de envío está en `send.` y el de recepción en el root, **coexisten sin conflicto**.
- **DMARC** → un solo TXT en `_dmarc`, cubre a ambos.

## Pasos

### 1. Recepción — Cloudflare Email Routing
1. Cloudflare → dominio → **Email** → Email Routing.
2. Agregar **Destination Address** (la casilla real). Queda `Pending`: Cloudflare manda un mail de verificación a ESA casilla → hay que abrirlo y hacer clic. Sin eso, NO entrega.
3. Editar la regla **Catch-all** → acción **Send to an email** → destino → activar el toggle (`Active`).
4. **GOTCHA UI NUEVA (Email Service):** el botón de "enable" está escondido. Se activa yendo a **Settings → DNS records → botón `Lock`** (lockea/escribe los MX+SPF+DKIM en la zona). No hay toggle obvio de "activar routing". Tras lockear, Status pasa a `Enabled` y aparecen los records en la zona.
5. Verificar en la zona DNS que aparecieron los 3 MX `routeN.mx.cloudflare.net` + SPF `_spf.mx.cloudflare.net` + DKIM `cf2024-1._domainkey`.

### 2. Envío — Resend
1. Resend → **Domains** → Add domain (o ya existe). Elegir región.
2. Resend detecta el provider (Cloudflare) y ofrece **"Auto configure"** → escribe los 3 records directo en Cloudflare vía API. (Alternativa: cargarlos a mano — el DKIM es largo, cuidado con el truncado visual; leer el valor exacto del DOM.)
3. Records que agrega: `send` MX → `feedback-smtp.<region>.amazonses.com` (prio 10) · `send` TXT → `v=spf1 include:amazonses.com ~all` · `resend._domainkey` TXT → DKIM.
4. Click **"Verify DNS Records"**. Cloudflare es autoritativo → verifica en segundos/minutos. Domain pasa a `Verified`.

### 3. DMARC (anti-spoofing)
- TXT `_dmarc` → `v=DMARC1; p=quarantine; rua=mailto:dmarc@dominio; adkim=r; aspf=r`
- **Un solo** record `_dmarc` (si Resend sugiere uno con `p=none`, no duplicar — usar el propio).
- `p=quarantine` con alineación relajada es seguro: el mail de Resend pasa SPF+DKIM alineados. Subir a `p=reject` recién cuando se confirme deliverability unos días.
- El `rua` (reportes) puede caer en el mismo Gmail vía el catch-all si se usa `dmarc@dominio`.

### 4. Test end-to-end
```bash
# Leer la key desde donde viva (NUNCA imprimirla). from NO es secreto.
curl -s -w "\nHTTP %{http_code}\n" -X POST https://api.resend.com/emails \
  -H "Authorization: Bearer $RESEND_API_KEY" -H "Content-Type: application/json" \
  -d '{"from":"Marca <hola@dominio>","to":["tucasilla@gmail.com"],"subject":"test","html":"<p>test</p>"}'
```
`HTTP 200` + id = aceptado. Confirmar que **llega a la bandeja** (no solo `sent`). IPs nuevas pueden arrancar con reputación baja → mirar Resend → **Logs** para ver `delivered`.

## Gotchas aprendidos
- El `source .env` de bash **rompe** si `EMAIL_FROM` tiene `<>` (`Marca <hola@dominio>`) → los `<>` son redirección de shell. Para leer la key en scripts usar `grep '^KEY=' .env | cut -d= -f2-`, no `source`. (Las apps con loader propio de .env no tienen este problema.)
- Si la app usa `PUBLIC_BASE_URL` también para **OAuth redirect_uri** o **webhooks de pago**, NO reusarlo para los links de emails: desacoplar un `EMAIL_BASE_URL` propio. Cambiar `PUBLIC_BASE_URL` a ciegas rompe el login con Google.
- El dashboard de Cloudflare a veces se cuelga cargando (cosa de ellos) — reintentar, no es el setup.

## Dónde queda registrado quién administra qué
No confundir capas: **registro** (dónde se renueva el dominio) ≠ **DNS** (nameservers) ≠ **hosting** (dónde corre la app). Un dominio `.ar` se registra en **NIC.ar** (Clave Fiscal AFIP), el DNS puede estar en Cloudflare, y la app en el VPS. Ver la nota de proyecto de cada marca para los IDs concretos.
