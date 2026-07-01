---
date: 2026-05-31
type: runbook
tags: [salto-cuantico, korean-root, ops]
status: live
---

# Salto Cuántico — Runbook operacional

Doc de referencia para resolver issues comunes en producción sin tener que reverse-engineerear el sistema. Mantener actualizado cuando aparezcan casos nuevos.

**Sistema vive en**: VPS Korean Root `root@103.199.187.246`
**DB principal**: `/root/.openclaw/workspace/dashboard/ops_korean-root.db`
**API**: `http://127.0.0.1:8080` (proxy nginx `https://103-199-187-246.nip.io`)
**Cron**: `*/5 * * * * /root/.openclaw/workspace/scripts/cron_salto_cuantico_dispatch.py`
**Admin UI**: `https://103-199-187-246.nip.io/salto-cuantico`

---

## Escenario 1: Cliente reporta "no recibí mi mensaje"

**Síntoma**: alguien escribe al bot diciendo que no recibió el M3 (al recibir el producto), o el M1.

### Investigación

1. Entrar al admin `/salto-cuantico` → tab **Órdenes** → filtrar por phone
2. Click en el order_id → ver tab **events_log**
3. Buscar el event `queue.sent_dryrun` o `queue.sent` con `code=m3`
4. Si está → ver `wa_message_id`. Buscar evento `wa.status.failed` para esa wa_id

### Acciones

- **Si `wa.status.failed` con error 131026 (Receiver incapable)**: el número no tiene WA. Marcar manualmente al cliente o pedirle número alternativo.
- **Si dispatcher en modo dry_run**: no se envió por diseño. Cambiar `dispatcher_mode` a `live` desde admin solo después de templates aprobados Meta.
- **Si nunca se procesó (no hay event)**: chequear que `scheduled_at` esté en el pasado. Si está, ver health → `last_tick_age_min`. Si > 30 min, el cron está caído.

---

## Escenario 2: Cron dispatcher caído

**Síntoma**: header del admin muestra "Último tick" rojo, queue acumulada, `due_now` alto.

### Investigación

```bash
ssh root@103.199.187.246 "tail -50 /var/log/smartbrain/cron_salto_cuantico_dispatch.log"
ssh root@103.199.187.246 "crontab -l | grep salto_cuantico"
```

### Acciones

1. **Fix rápido**: ejecutar manualmente desde el admin → header → botón "tick"
2. **Si crontab no está**: re-registrar:
   ```bash
   ssh root@103.199.187.246 "bash /tmp/install_crontab.sh"
   ```
3. **Si el script da error**: revisar permisos `chmod +x` y que `/opt/journey-venv/bin/python3` exista.

---

## Escenario 3: TN coupons API caída → fallback masivo

**Síntoma**: header health muestra "X cupones con fallback global". Clientes reciben `SALTO15` en vez de su código único.

### Investigación

1. Admin → tab **Cupones** → filtrar status `fallback_global`
2. Mirar timestamp — si es reciente y muchos juntos, TN tuvo un downtime.

### Acciones

- **Cleanup post-incidente**: para cada cupón fallback, re-issue manual con la URL admin:
  ```
  POST /api/salto-cuantico/admin/coupons/issue-manual
  Body: {user_id, applies_to, percent, valid_days}
  ```
- **Notificar al cliente**: WA manual a Viqui con el código nuevo.
- Si TN sigue caída por > 30 min: pausar todo con toggle en admin hasta que vuelva.

---

## Escenario 4: Cliente quiere dejar el viaje pero no escribió "BAJA"

**Síntoma**: Viqui recibe mensaje "ya no quiero" en otro canal.

### Acciones

1. Admin → tab **Bajas** → confirmar que NO está ya unsubscribed.
2. Si no está, simular el unsub desde el endpoint admin:
   ```bash
   curl -X POST .../api/salto-cuantico/admin/wa-inbound/simulate \
     -H "Authorization: Bearer $JWT" \
     -d '{"from_phone":"549XXXXXXXXX","user_text":"BAJA"}'
   ```
3. Verificar que pasó a `unsubscribed` en tab Bajas.

---

## Escenario 5: Mensaje fallido masivo (template Meta rechazado)

**Síntoma**: alerta WA en cel de Viqui: "X mensajes fallidos en último tick". Tab Cola → status `failed`.

### Investigación

1. Mirar el error en la columna `error` de la cola → buscar mensaje de Meta tipo `template not found` o `template not approved`.
2. Si Meta rechazó el template: hay que recrearlo en Business Manager.

### Acciones

1. Pausar el dispatcher con toggle en admin (evitar más fallos)
2. Ir a Meta Business Manager → revisar status del template
3. Una vez aprobado, retry manual desde admin tab Cola → botón ↻

---

## Escenario 6: Orden duplicada / mensajes duplicados

**Síntoma**: cliente reporta haber recibido el M1 dos veces.

### Diagnóstico

Esto NO debería pasar — el sistema dedupea por `tn_order_id` en `salto_cuantico_orders` y por `(order_id, message_code)` en `salto_cuantico_message_queue` (UNIQUE constraint).

Si pasa:
1. Verificar `tn_webhook_events` — debería haber dedup ahí
2. Ver `salto_cuantico_orders` por ese phone — buscar 2 rows con distinto `tn_order_id`. Si son 2 órdenes distintas en TN, es esperado.

---

## Escenario 7: Reactivar dispatcher después de pausa

```sql
-- desde admin UI: toggle PAUSADO → ACTIVO
-- o vía SQL:
UPDATE salto_cuantico_settings SET value='false' WHERE key='journey_paused';
```

El próximo tick (cada 5 min) recoge los mensajes acumulados que aún están dentro de ventana (24h del scheduled_at).

---

## Escenario 8: Switch dry_run → live

**Pre-checks obligatorios**:
- [ ] Los 6 templates Meta aprobados (admin → Setup → categoría Templates)
- [ ] Meditación M1 grabada y URL en `salto_cuantico_assets`
- [ ] Video M3 grabado y `media_id_wa` en `salto_cuantico_assets`
- [ ] Test con 1 cliente real (forzar 1 mensaje desde admin, ver que llegue al cel)

```sql
UPDATE salto_cuantico_settings SET value='live' WHERE key='dispatcher_mode';
```

Esperá 10 min monitoreando health en admin. Si todo verde, queda live.

---

## Escenario 9: Borrar un cliente por GDPR

```sql
-- Soft delete
UPDATE salto_cuantico_users SET deleted_at=datetime('now'), journey_status='unsubscribed'
 WHERE phone='549XXXXXXXXX';

UPDATE salto_cuantico_message_queue SET status='cancelled'
 WHERE user_id=(SELECT id FROM salto_cuantico_users WHERE phone='549XXXXXXXXX');
```

Para hard delete (raro):
```sql
DELETE FROM salto_cuantico_events_log WHERE user_id=?;
DELETE FROM salto_cuantico_message_queue WHERE user_id=?;
DELETE FROM salto_cuantico_coupons WHERE user_id=?;
DELETE FROM salto_cuantico_responses WHERE enrollment_id IN
  (SELECT id FROM salto_cuantico_enrollments WHERE user_id=?);
DELETE FROM salto_cuantico_checkins WHERE enrollment_id IN
  (SELECT id FROM salto_cuantico_enrollments WHERE user_id=?);
DELETE FROM salto_cuantico_enrollments WHERE user_id=?;
DELETE FROM salto_cuantico_rewards WHERE user_id=?;
DELETE FROM salto_cuantico_users WHERE id=?;
```

---

## Tablas DB reference

| Tabla | Propósito |
|---|---|
| `salto_cuantico_users` | clientes del programa |
| `salto_cuantico_journeys` | 3 programas (Limonada/Shakti/Solar) |
| `salto_cuantico_enrollments` | user × journey |
| `salto_cuantico_quizzes` | 9 cuestionarios (3 por journey) |
| `salto_cuantico_responses` | respuestas a quizzes |
| `salto_cuantico_checkins` | check-ins semanales |
| `salto_cuantico_content` | "Para vos" — recetas/articles/audios |
| `salto_cuantico_rewards` | historial de puntos (positivos: ganados; negativos: canjeados) |
| `salto_cuantico_orders` | órdenes TN ingeridas |
| `salto_cuantico_message_queue` | queue del dispatcher |
| `salto_cuantico_coupons` | cupones generados (con tn_coupon_id) |
| `salto_cuantico_assets` | URLs/media_ids de meditaciones/videos |
| `salto_cuantico_settings` | toda la config editable |
| `salto_cuantico_blackout_dates` | rangos sin envío |
| `salto_cuantico_events_log` | audit log append-only |
| `salto_cuantico_setup_checklist` | la vista /setup del admin |
| `tn_webhook_events` | dedup webhooks TN |

---

## Endpoints útiles

```
GET  /api/salto-cuantico/admin/health             # snapshot health
GET  /api/salto-cuantico/admin/dispatcher/status  # último tick + settings
POST /api/salto-cuantico/admin/dispatcher/tick    # forzar tick
GET  /api/salto-cuantico/admin/funnel             # contadores por mensaje
GET  /api/salto-cuantico/admin/queue?status_filter=failed
POST /api/salto-cuantico/admin/queue/{id}/retry
GET  /api/salto-cuantico/admin/orders
GET  /api/salto-cuantico/admin/unsubscribes
POST /api/salto-cuantico/admin/users/{id}/resubscribe
GET  /api/salto-cuantico/admin/coupons
POST /api/salto-cuantico/admin/coupons/issue-manual
GET  /api/salto-cuantico/admin/blackouts
POST /api/salto-cuantico/admin/blackouts
```

---

## Credenciales / dependencias externas

- **TN**: `TIENDANUBE_ACCESS_TOKEN` y `TIENDANUBE_STORE_ID` en `/etc/smartbrain/.env`
- **WA Cloud**: `WA_ACCESS_TOKEN`, `WA_PHONE_NUMBER_ID` (mismo .env)
- **OpenRouter** (gender inference): `OPENROUTER_API_KEY`
- **Alert target**: setting `alert_target_phone` (default: chip Viqui `5493426516417`)

---

## Backups

Antes de cualquier intervención mayor, snapshot DB:
```bash
ssh root@103.199.187.246 "cp /root/.openclaw/workspace/dashboard/ops_korean-root.db \
  /root/.openclaw/workspace/dashboard/ops_korean-root.db.bak-$(date +%Y%m%d-%H%M%S)"
```

Hay snapshots automáticos por fase desde el build (`ops_korean-root.db.bak-fase0-*`).
