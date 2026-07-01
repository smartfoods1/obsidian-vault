---
date: 2026-06-21
type: project
tags: [del-problema-al-sistema, cohorte, educacion, lanzamiento, specialandres]
status: en-progreso
---

# Del Problema al Sistema

Programa educativo de Andrés (`@specialandres`): enseñar a dueños de negocio no técnicos a construir, con IA + Claude Code + servidor propio, sistemas que resuelven problemas reales. Primer lanzamiento: **Cohorte Fundadora**.

## La idea en una línea

> Tenés el problema. Te falta el sistema. El método para que un dueño de negocio —sin ser programador— transforme los problemas que le comen tiempo y plata en sistemas de IA que trabajan solos.

- **Método (activo atemporal):** "Del Problema al Sistema" — sirve para cualquier problema.
- **Promesa de la cohorte 1 (gancho de venta):** construí tu empleado de ventas en WhatsApp en 5 semanas.
- **Posicionamiento:** no es "aprendé Claude Code" (commodity). Es un operador real que construyó los sistemas que operan su empresa sin escribir código y los implementó en otras marcas.

## El método — 5 etapas

`Detectar → Traducir → Conectar → Construir → Lanzar`. Una etapa por semana. Detalle completo y guion clase por clase en [[curriculum-y-guiones|Currículum y guiones]]. La app de referencia que se construye en vivo (y los alumnos replican) está en [[app-caso-testigo|App del caso testigo]].

## La oferta — Cohorte Fundadora

- **8 cupos** (elegidos a mano vía aplicación, no checkout directo).
- **Precio fundador: USD 450** (después USD 1.000+).
- **Pago total adelantado** (descartada la seña: no valida el pago completo y parte la cobranza). Quien necesita, 2 cuotas 50/50 a mano.
- **Garantía de resultado:** te vas con el sistema andando o 1:1 hasta lograrlo (condicionada a cumplir las entregas).
- **Sin riesgo:** devolución total y sin preguntas en la primera semana. Coherente con la confianza en el producto: el que confía devuelve, no pide seña.
- **Fechas:** arranca viernes 17/7. 5 viernes: 17 y 24 de julio; 31; 7 y 14 de agosto. 10:00 hs (Arg), 90 min.

### Por qué cohorte fundadora
El objetivo NO es maximizar ingreso: es **validar demanda con plata real** y **parir los primeros casos/testimonios**. El precio bajo es el peaje por esos casos.

### Umbral de validación
Si al ~10/7 hay **6 pagos confirmados**, la cohorte va con todo. Si hay 2, ajustar problema-gancho o canal antes del 17.

## Infraestructura (en vivo)

- **Landing:** https://srv1319033.hstgr.cloud/dps/
- **Panel CRM (mini-CRM):** https://srv1319033.hstgr.cloud/dps-api/admin (Basic Auth)
- Stack: FastAPI + SQLite en VPS (`/opt/dps`), nginx subpath, systemd `dps.service`. Aislado de SmartBrain.
- Pipeline CRM: `nuevo → contactado → aprobado → pagó → inscripto` (o descartado), con notas + link a WhatsApp + export CSV.
- **Credenciales admin:** en `/opt/dps/.env` del VPS (NO se guardan acá). Código local en `~/dps-landing/` con README.
- Pendiente: dominio propio (la URL de Hostinger convierte peor para venta) — apuntar DNS al VPS 76.13.228.77 cuando esté.

## Kit de marketing

3 posts + stories + flyer, copy e imágenes, en [[kit-lanzamiento|Kit de lanzamiento]]. Mismo lenguaje visual que la landing (papel, tinta, verde, serif editorial).

## Estado y próximos pasos

- [x] Posicionamiento, método, nombre, oferta definidos.
- [x] Landing + formulario de aplicación + mini-CRM desplegados y verificados.
- [x] Kit de marketing (3 posts + stories + flyer).
- [x] Currículum + guion clase por clase.
- [ ] Definir dominio propio.
- [ ] Poner link en la bio de `@specialandres` y abrir inscripción.
- [x] Diseñar en detalle la app del caso testigo → [[app-caso-testigo|App del caso testigo]].
- [ ] Capturar prueba social de la cohorte 1 (antes/después).

## Decisiones clave (para no re-litigar)

- Educación = top del funnel; servicios (Content Hub / Growth B2B) = abajo. No dispersarse.
- Vender el resultado, no la herramienta. El mindset es el valor; "lo último de IA" no se vende y caduca.
- "Sin ser programador" sí; "sin tocar código" no (genera reembolsos). Andrés construyó todo sin escribir código.
- Alumnos practican en canal de baja fricción; WhatsApp oficial (WABA) es upsell de setup.
