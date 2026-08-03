---
date: 2026-08-01
type: informe
tags: [gondola, whatsapp, waba, smart-foods, infra]
status: ejecutado
---

# Migración WABA → exclusivo Góndola (1/8/2026)

Decisión CEO: el WABA `1399636844706704` (phone `1057793384074433`, +54 9 11 2527-0390)
pasa a ser **exclusivo de Góndola**. Smart Foods queda SIN canal WhatsApp.

## Decisiones tomadas por Andrés
- Login OTP del dashboard SmartBrain SF: **muere** (no usa más ese dashboard; Flor tampoco tiene acceso).
- Notificaciones operativas (aprobación posts 11:30, alertas, briefing lunes): **apagadas**.
- Flows Shopify SF (pedido, envío, carrito, NPS, reviews): **apagados**.
- Clientes SF que escriban al número: **silencio** (Góndola ignora números ajenos).

## Cambios ejecutados (VPS 76.13.228.77)
1. **Inbound**: nginx `openclaw-webhook` location `/webhook/whatsapp-cloud` repunteada
   `18791 (journey-proxy)` → `127.0.0.1:8200/api/wa/webhook` (Góndola). Meta NO se tocó
   (misma URL pública, misma app, misma firma). Challenge verificado OK con `LM_WA_VERIFY_TOKEN`.
2. **Góndola**: `LM_WA_WABA_RECRUIT=1` en `/opt/lead-machine/.env` (sin el flag, el webhook
   ackea pero descarta) + restart `lead-machine`. Firma X-Hub-Signature-256 obligatoria (fail-closed).
3. **Crons SF**: 29 crons emisores de WA comentados con marcador `#WABA-OFF#` (shopify_flows,
   abandoned_cart, nps, review_request, sequences, scheduled_msgs, journeys, wa_daily_*,
   handoff, autoreplies, cascade, pillar drip/reminders, ceo_brief, brief_operativo,
   smartbot_health_monitor, kb_autopopulate, etc.).
4. **Corte estructural**: `WA_ACCESS_TOKEN=` (vacío) en `/etc/smartbrain/.env` → ningún código
   SF puede emitir por el número aunque algo quede vivo. Restart `smartbrain-api`.
5. **journey-proxy**: stopped + disabled (era el receptor/bot WA de SF).

Intactos: KR (WABA propio en su VPS), wa-baileys/wa-group-worker (WA personal de Andrés,
no WABA), smartwap (sin credenciales WA), IG publishing, email, Góndola outreach
(campaign_b2b_seed / brands_seed / brands_sequence siguen igual, template `gondola_outreach`).

## Rollback (si hiciera falta)
```
# nginx:    cp /root/nginx-openclaw-webhook.bak.waba.20260801_2045 /etc/nginx/sites-enabled/openclaw-webhook && systemctl reload nginx
# crontab:  crontab /root/crontab.bak.waba.20260801_2045
# SF env:   cp /etc/smartbrain/.env.bak.waba.20260801_2045 /etc/smartbrain/.env && systemctl restart smartbrain-api
# gondola:  cp /opt/lead-machine/.env.bak.waba.20260801_2045 /opt/lead-machine/.env && systemctl restart lead-machine
# bot:      systemctl enable --now journey-proxy
```

## Pendiente de verificación
- Test real: mandar "hola" al +54 9 11 2527-0390 y confirmar que aparece en el log de
  `lead-machine` (`journalctl -u lead-machine | grep wa`). El challenge ya validó, falta ver
  un POST real procesado.
- Quality rating del número en Meta: el historial de SF (bot + campañas) queda; vigilar que
  el outreach de Góndola no lo degrade.
- Sacar el número de WhatsApp de la web de Shopify / bio de IG de SF (sigue publicado).
