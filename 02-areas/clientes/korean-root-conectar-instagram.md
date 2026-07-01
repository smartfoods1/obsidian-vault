---
date: 2026-06-16
type: playbook
tags: [korean-root, instagram, smartbrain, contenido, meta]
status: activo
---

# Korean Root — Conectar Instagram para publicación automática

> Objetivo: que SmartBrain publique solo los posts aprobados/agendados de KR en **@koreanroot**.
> Estado: todo el sistema de contenido está listo; **lo único que falta es esto**. Hoy el token está vacío y el banner de la sección Contenido muestra 🔴 "Instagram no conectado".

## Qué se necesita (lo hace alguien con acceso al Business Manager de KR)

1. **@koreanroot debe ser cuenta Profesional/Business** (no personal).
   - App Instagram → Configuración → Cuenta → "Cambiar a cuenta profesional".

2. **Vincularla a una Página de Facebook** de Korean Root.
   - Desde la Página FB → Configuración → "Cuentas vinculadas" → Instagram. O desde IG → Configuración → "Compartir en otras apps".

3. **Página + cuenta IG en el mismo Meta Business Manager.**
   - business.facebook.com → Configuración del negocio → que la Página y la cuenta de Instagram estén agregadas al mismo Business.
   - Puede usarse la **misma App de Meta** que ya usan para el bot de WhatsApp, si se le habilitan los productos de Instagram (Instagram Graph API).

4. **Generar un token de acceso de larga duración** con estos permisos:
   - `instagram_basic`, `instagram_content_publish`, `pages_show_list`, `pages_read_engagement` (y `business_management`).
   - Camino rápido: Graph API Explorer (developers.facebook.com/tools/explorer) → elegir la App → "Get Token" con esos permisos → luego intercambiarlo por uno de 60 días (long-lived).

5. **Obtener el IG User ID** (el de la cuenta business):
   - En Graph API Explorer: `GET /me/accounts` → tomar el `id` de la Página → `GET /{page-id}?fields=instagram_business_account` → ese `instagram_business_account.id` es el **IG_USER_ID**.

6. **Pasarle a Andrés**: el **token** + el **IG_USER_ID**.

## Qué hace Andrés (yo) con eso

- Cargo en `/etc/smartbrain/.env` del VPS de KR (`103.199.187.246`):
  - `IG_ACCESS_TOKEN=` (o `IG_PAGE_ACCESS_TOKEN=`) el token
  - `IG_USER_ID=` el id
- Reinicio `smartbrain-api`. (El cron de publicación ya está agendado: corre cada hora 10–21 ART.)

## Cómo verificar que quedó conectado

- Entrar a SmartBrain KR → **Contenido**. El banner de arriba debe pasar a 🟢 **"Instagram conectado: @koreanroot"** con seguidores y agendados pendientes.
- El endpoint `GET /api/content/ig-status` devuelve `connected: true`.
- Probar un post aprobado con "Publicar ahora" o esperar el cron.

## Notas

- Los tokens de IG duran ~60 días (long-lived); hay que renovarlos antes de que expiren.
- Sin esto, todo lo demás funciona (generar contenido, plantillas, subir reels/stories, agendar) — solo la publicación efectiva a IG queda en espera.
