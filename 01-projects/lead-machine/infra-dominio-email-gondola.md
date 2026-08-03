---
date: 2026-07-04
type: infra
tags: [gondola, dominio, email, cloudflare, resend, dns, lead-machine]
status: operativo
derivado_de: playbook-email-dominio-cloudflare-resend
---

# Gondola.ar — dominio + email (infra, jul 4 2026)

Setup completo de dominio y email para **Góndola** (la app lead-machine, `~/lead-machine/`, VPS `76.13.228.77`). Patrón general en [[playbook-email-dominio-cloudflare-resend|Playbook: Email de dominio (Cloudflare + Resend)]].

## Dónde vive cada capa (aclaración importante — NO es Donweb)

| Capa | Dónde |
|---|---|
| **Registro** `gondola.ar` | **NIC.ar** (`.ar`, se renueva con Clave Fiscal AFIP) |
| **DNS** | **Cloudflare** — account `b588a7eb1d99a0441521da8f2e3dc068` ("Andy@smartfoods.ar's Account") |
| **Hosting app** | VPS Hostinger `76.13.228.77`, nginx vhost `sites-available/gondola` → `127.0.0.1:8200` (uvicorn `app:app`) |

> Otros dominios de Andrés (mismo relevamiento): `ceocode.com` en **GoDaddy**, `ceocode.dev` Cloudflare (sin usar), `smartfoods.ar` NIC.ar + DNS apuntando a **Shopify** (23.227.38.65).

## Sitio
- `gondola.ar` y `www.gondola.ar` → A → `76.13.228.77`, proxied 🟠 por Cloudflare.
- **gondola.ar SIRVE la app Góndola** (no solo el dashboard SmartBrain, que está en `gondola.76.13.228.77.nip.io`).

## Email — RECEPCIÓN (Cloudflare Email Routing) ✅
- Catch-all `*@gondola.ar` → reenvía a **specialandres@gmail.com** (destino `Verified`).
- Root: 3× MX `routeN.mx.cloudflare.net` + SPF `_spf.mx.cloudflare.net` + DKIM `cf2024-1._domainkey`.
- Se activó lockeando los DNS records en Settings (la UI nueva esconde el enable).

## Email — ENVÍO (Resend) ✅
- Workspace Resend: **`smartcoffee.ar`** (login `smartcoffee.ar@gmail.com`), región **sa-east-1 (São Paulo)**. Dominio `gondola.ar` `Verified`.
- Records en subdominio `send.gondola.ar` (MX `feedback-smtp.sa-east-1.amazonses.com` + SPF `amazonses.com`) + DKIM `resend._domainkey`. Cargados por el "Auto configure" de Resend. **No chocan** con la recepción (envío en `send.`, recepción en root).
- **El código de envío YA estaba** en `app.py` (`send_email()` vía Resend, welcome al registrarse, unsubscribe, admin blast). `RESEND_API_KEY` (`re_…`) + `EMAIL_FROM="Góndola <hola@gondola.ar>"` ya estaban en `/opt/lead-machine/.env`. Faltaba SOLO verificar el dominio en Resend.
- **Test end-to-end: `POST api.resend.com/emails` → HTTP 200**, y **el mail llegó a la bandeja** (confirmado por Andrés). Envío 100% operativo.

## Anti-spoofing ✅
- `_dmarc` TXT → `v=DMARC1; p=quarantine; rua=mailto:dmarc@gondola.ar; adkim=r; aspf=r`.
- A futuro: subir a `p=reject` cuando se confirme deliverability estable.

## Cambio de código (deployado + commiteado)
- `app.py:632` — se desacopló `EMAIL_BASE_URL` de `PUBLIC_BASE_URL` para que los links de los emails salgan con `https://gondola.ar` **sin romper** el redirect de Google OAuth ni MercadoPago (que siguen con `PUBLIC_BASE_URL` = `leadmachine…nip.io`). Se seteó `EMAIL_BASE_URL=https://gondola.ar` en el `.env` del VPS.
- Deployado con `./deploy.sh` (7/7 OK). Commit `e91de2d` en `main`.

## Pendientes / a futuro (no urgentes)
- **Workspace Resend**: hoy `gondola.ar` vive bajo el workspace `smartcoffee.ar`. Si se quiere separar facturación/límites por marca, migrar a un workspace Góndola propio.
- **Deliverability**: primer envío masivo real → monitorear Resend → Logs para confirmar `delivered` (IPs nuevas arrancan con reputación baja).
- **DMARC** → `p=reject` una vez estable.
- Migrar el login del dashboard de `gondola.76.13.228.77.nip.io` a `app.gondola.ar` (solo agregar A→VPS + certbot).
