---
date: 2026-07-22
type: project
tags: [lume, luz-roja, hardware, app]
status: activo
---

# Lumé — Panel de luz roja + NIR

Producto nuevo (jul 2026), aparte de Smart Foods / Smart Coffee: panel de **luz roja + infrarrojo cercano** ensamblado en Argentina con componentes importados premium. Concepto: "la calidad de la luz es el tratamiento; todo lo demás es marketing".

## Specs del panel
630 + 660 + 850nm · 40W · 16 LEDs · **40 mW/cm² a 30cm** · haz 20° · 33×11×6cm · 950g · >100.000h · garantía 1 año · carcasa impresa 3D · 220V.

## Precio
Preventa USD 222 / ARS 333.000 · Lista USD 300 / ARS 450.000.

## Entregables
- **Landing** (jul 21): LIVE en https://srv1319033.hstgr.cloud/lume/ (VPS SF, `/var/www/lume/`)
- **App companion**: [[01-projects/lume/app-spec|Spec MVP + backlog v2]] (jul 22)
- **App MVP construido** (jul 22): repo `~/lume-app` (Expo SDK 57 + expo-router, TypeScript, commit `bddd631`). Las 5 features del MVP implementadas y verificadas en web; correr con `npx expo start` (Expo Go) o `--web`. Spec-kit en `specs/001-mvp/`.

## Pendientes generales
- Verificar marca "Lumé" en INPI + dominio
- Foto de producto premium / lifestyle
- Deploy a dominio real
- Captura de leads (form o seña MercadoPago) además del WhatsApp
- **Medir irradiancia a 10/15/20/45cm** (hoy solo tenemos el dato a 30cm) — necesario para la tabla de dosis de la app
