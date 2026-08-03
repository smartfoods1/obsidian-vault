---
date: 2026-07-03
type: architecture-decision
tags: [smart-foods, philo-cafe, consignacion, b2b, sistema]
status: en-produccion
---

> **UPDATE jul 3 2026 (mismo día)**: construido y deployado. URL: `https://srv1319033.hstgr.cloud/consigna/`.
> Código local `~/consigna-philo` (git) · VPS `/opt/consigna` · systemd `consigna` · datos `/var/lib/consigna/` · backup cron 03:15.
> Formato de Philo validado con 12 archivos reales (1 hoja por local, `Nombre|Sku|fechas ISO`, códigos estables) — el parser se escribió contra esos archivos y el E2E corre con ellos (38 checks).
> Cambio de requerimiento vs diseño original: login ÚNICO compartido para Philo (rol retailer) que elige local; la accountability va en la alerta (nombre obligatorio + hora + detalle). Sin OTP para gerentes.
> Los 4 archivos de junio quedaron subidos en preview. Pendiente: stock inicial, confirmar archivos, WA_ALERT_TEMPLATE, credenciales a Philo, DNS consigna.smartfoods.ar (opcional).

# Sistema de consignación Smart Foods × Philo Cafe — Decisión de arquitectura

## Contexto

Smart Foods deja mercadería en consignación en la cadena Philo Cafe. Se necesita: stock por local, remitos de entrada, procesamiento de archivos de ventas del retailer (descuento automático de stock), portal read-only para gerentes de local con reporte de diferencias.

Se evaluaron 3 arquitecturas con un panel multi-agente (jul 2026): módulo dentro de SmartBrain, app standalone mínima, y el plan original (Docker + PostgreSQL + Next.js).

## Decisión: app standalone mínima ("Consigna")

**Stack**: FastAPI + SQLite (WAL) con DB propia + SSR Jinja2/htmx/Tailwind (sin build step) + systemd + nginx en subdominio propio (`consigna.smartfoods.ar`). Sin Docker, sin Postgres, sin Next.js.

**Razón decisiva**: los gerentes de Philo son empleados de OTRA empresa. El boundary de seguridad se resuelve con física (proceso separado en 127.0.0.1:8090, DB separada, usuario UNIX dedicado no-root con hardening systemd, secrets separados en `/etc/consigna/.env`, dominio separado) y no con disciplina de código dentro del monolito SmartBrain. Además: los deploys frecuentes de SmartBrain no deben rebotar el portal de un cliente externo, y con la disolución societaria en curso conviene que este activo viva como pieza independiente.

**Por qué no el plan original**: Postgres + Docker + Next.js es un segundo régimen operativo completo (~400-600MB RAM extra, backups pg_dump no dominados, imágenes que nadie rebuildea) para un problema de 5-30 locales, 7 SKUs y 2 archivos por mes. La mitad del plan sí sobrevive: app separada, FastAPI, subdominio TLS, motor transaccional todo-o-nada.

## Núcleo del diseño

- **Ledger append-only** (`movimientos`): inmutable con triggers SQLite `BEFORE UPDATE/DELETE RAISE(ABORT)`. Stock = `SUM(cantidad)` por (local, producto) — derivado, nunca cacheado en tabla mutable.
- **Fecha efectiva vs fecha de registro** en cada movimiento (el archivo llega días después del período).
- **Idempotencia en 3 capas**: sha256 UNIQUE del archivo + UNIQUE parcial (retailer, período) en estado aplicado + claim atómico por rowcount (mismo patrón anti-doble-dispatch del WA dispatcher).
- **Motor de ventas en 2 fases**: parse a staging con validación fila por fila → preview obligatorio (stock resultante, negativos en rojo, códigos sin mapear con form inline) → confirm en UNA transacción `BEGIN IMMEDIATE`, todo-o-nada.
- **Mapeo de códigos** Philo→SKU SF (`sku_map` con `factor_unidades`). Códigos huérfanos bloquean el batch (nunca aplicar parcial). Layout de columnas configurable en DB por retailer.
- **Unidad mínima vendible**: todo el stock en unidades (barrita, no display x12); conversión en la UI de remitos.
- **Precios con vigencia histórica** (`precios_consignacion` con vigente_desde/hasta): la venta se valúa al precio de su fecha; la liquidación snapshotea el precio en el renglón.
- **Liquidaciones**: entidad de cierre por período con renglones congelados. Período cerrado = inmutable; correcciones = ajuste retroactivo hacia adelante en el período corriente (matchea nota crédito/débito).
- **Stock negativo**: no bloquea (la venta es real y se factura) pero auto-crea discrepancia + alerta WA; no se cierra el período con negativos sin resolver.
- **Recepción conforme del remito**: el gerente confirma cantidades recibidas; el stock se acredita por lo confirmado.
- **Gerentes**: login OTP por WhatsApp (patrón copiado de SmartBrain, secrets propios), scoping de local SOLO desde la sesión (el parámetro no existe), rate limit al único write (reportar diferencia). Sin precios visibles para el rol gerente.
- **Multi-retailer barato**: `retailer_id` en todas las tablas + config por retailer en DB. No construir multi-DB ni onboarding hoy.
- **Ops**: `/opt/consigna` + `/var/lib/consigna/` (db + uploads originales como evidencia), backup diario `sqlite3 .backup` + rclone off-VPS semanal + restore probado una vez, tests de boundary 403 en cada deploy, alertas WA por plantilla APPROVED (quiebre stock, período sin archivo, batch trabado).

## Bloqueantes antes de codear

1. **2-3 archivos de ventas REALES de Philo** — la incógnita dominante; el parser se escribe contra el archivo real.
2. Acordar con Philo: quién paga faltantes de conteo, cadencia de reportes, unidad que representa cada código de su POS, precio a fecha de venta vs precio al cierre.
3. DNS `consigna.smartfoods.ar` → VPS.

## Estimación

40-60 h efectivas, 2-3 semanas calendario. Fases: esquema+ledger → motor de archivos → auth+portal gerente → UI admin → liquidación → ops/runbook → prueba end-to-end con archivos reales.
