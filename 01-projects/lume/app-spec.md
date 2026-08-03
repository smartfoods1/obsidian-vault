---
date: 2026-07-22
type: spec
tags: [lume, app, mvp, wearables, fotobiomodulacion]
status: en-desarrollo
implementacion: "~/lume-app (Expo SDK 57) — MVP v0.1 construido jul 22"
derivado_de: "[[01-projects/lume/index]]"
---

# Lumé App — Spec MVP + Backlog v2

Companion app del panel Lumé. Dos trabajos: **educar** al usuario para que use bien el panel, y **mostrarle el impacto** en su cuerpo combinando registro de sesiones con datos de su wearable.

---

## Principios de producto

1. **Educar > medir.** El diferencial de Lumé es "la calidad de la luz es el tratamiento". La app enseña a dosificar bien; los datos son el refuerzo, no la promesa central.
2. **Los quick wins van al frente.** Dolor, energía y piel se perciben en semanas; HRV y sueño se mueven lento y con ruido. La UI prioriza lo perceptible para no frustrar.
3. **Framing wellness, nunca terapéutico** (ANMAT 4059/2025). "Registrá tus sesiones y conocé tu cuerpo" — jamás "tratá tu dolor" ni nombres de enfermedades. Mismo criterio que la landing.
4. **Fricción mínima**: check-in diario ≤ 10 segundos, sesión se registra con 2 taps (el timer lo hace solo).
5. **El moat es la dosis.** Conocemos la irradiancia exacta del panel → podemos calcular J/cm² reales, el lenguaje de toda la literatura de fotobiomodulación. Ninguna app genérica de wellness puede.

---

## Alcance MVP

### F1 — Sesiones con timer guiado y dosis real
- Registro: fecha/hora, duración, **distancia al panel**, zona del cuerpo, modo (roja 630/660 · NIR 850 · ambas).
- **Timer integrado con guía**: el usuario elige objetivo + zona → la app dicta distancia y tiempo ("30 cm, 12 minutos") y arranca cuenta regresiva con aviso al terminar.
- Cálculo automático de **dosis en J/cm²** por sesión (ver modelo abajo).
- Registro manual retroactivo (sesión sin la app abierta).
- Historial: dosis acumulada semanal, racha de adherencia, calendario de sesiones.

### F2 — Check-in subjetivo diario (≤10 s)
- **Energía al despertar** (1–10)
- **Dolor/molestia localizada** (1–10 + zona del cuerpo en silueta tocable) — opcional, solo si el usuario activó "seguimiento de zona"
- **Ánimo** (emoji 5 niveles)
- Push a la mañana; se responde desde la notificación sin abrir la app.

### F3 — Sync de wearables (HealthKit + Health Connect)
Solo lectura, vía Apple HealthKit (iOS) y Google Health Connect (Android). Eso cubre Apple Watch, Garmin, Samsung, Polar, Amazfit, Xiaomi y la mayoría de las balanzas sin integrar dispositivo por dispositivo.

Métricas MVP:
- **HRV** (rMSSD)
- **Sueño**: duración, fases (profundo/REM), latencia, eficiencia
- **FC en reposo**
- **Ejercicio/entrenamientos** — solo como variable de control (contexto de por qué se movió el HRV), no se muestra como métrica propia.

La app funciona 100% sin wearable: sesiones + check-ins subjetivos ya cierran el loop.

### F4 — Baseline y comparación con/sin sesión
- Al onboardear: la app pide **7–14 días de baseline** antes o durante las primeras sesiones (si hay historial en HealthKit, lo importa retroactivamente y el baseline es instantáneo).
- Insight central: **días con sesión vs. días sin sesión** — "las mañanas después de una sesión nocturna, tu latencia de sueño promedió 6 min menos".
- Umbral de honestidad: si no hay diferencia estadísticamente decente, la app lo dice ("todavía no hay señal clara — seguí 2 semanas más") en vez de inventar correlaciones. La confianza es la marca.

### F5 — Educación
- **Protocolos por objetivo** (recuperación muscular, piel, energía/mañana, relajación/noche): cada uno define zona, distancia, tiempo, frecuencia semanal y qué esperar en qué plazo. Alimentan el timer de F1.
- **Píldoras educativas** cortas (por qué 660 vs 850, qué es una dosis, por qué más tiempo no es mejor — curva bifásica). Lenguaje ANMAT-safe, misma base de evidencia verificada que la landing (`scratchpad/brief.json`).

---

## Modelo de dosis

`Dosis (J/cm²) = irradiancia (W/cm²) × segundos`

Con el dato medido del panel — **40 mW/cm² a 30 cm** (0,04 W/cm²):

| Duración a 30 cm | Dosis |
|---|---|
| 5 min | 12 J/cm² |
| 10 min | 24 J/cm² |
| 20 min | 48 J/cm² |

Rangos de referencia en literatura: superficial/piel ~3–15 J/cm², tejido profundo (músculo/articulación, NIR) ~20–60 J/cm². Los protocolos de F5 se calibran dentro de esos rangos.

⚠️ **Bloqueante de hardware**: hoy solo tenemos irradiancia medida a 30 cm. Hay que **medir a 10 / 15 / 20 / 45 cm** con solar power meter y cargar la tabla real (con haz de 20° la caída no es inversa cuadrada pura — no extrapolar, medir). Sin esa tabla, el MVP fuerza distancia fija de 30 cm en el timer.

---

## Modelo de datos mínimo

- `users` — perfil, objetivo principal, panel vinculado (serial), consentimiento datos salud
- `sessions` — ts, duración, distancia, zona, modo, dosis_jcm2, fuente (timer/manual)
- `checkins` — fecha, energía, dolor (zona+score), ánimo
- `health_samples` — tipo (hrv/sleep_*/rhr/workout), valor, ts, fuente (healthkit/healthconnect)
- `baselines` — métrica, ventana, media, desvío

Datos de salud = dato sensible: cifrado en reposo, borrado total a pedido, y el consentimiento del onboarding lo dice sin letra chica.

---

## Stack recomendado

- **App**: React Native + Expo (un codebase, librerías maduras para HealthKit y Health Connect). Offline-first: SQLite local, sync a backend cuando hay red.
- **Backend**: FastAPI + SQLite/Postgres en VPS (mismo stack SmartBrain — reuso de patrones, no de código; Lumé es producto separado).
- **Sin LLM en el MVP.** Los insights de F4 son estadística simple (medias, desvíos, diferencia de grupos). Gemini Flash queda para v2 si hay capa de coach.
- Al arrancar desarrollo: repo propio `~/lume-app` con `specify init . --integration claude` (flujo spec-kit; este doc es el insumo de `/speckit.specify`).

---

## Métricas de éxito del MVP

- **Activación**: % de compradores que registran ≥1 sesión en la primera semana
- **Hábito**: sesiones/semana promedio (target: ≥3 — es donde la literatura muestra efecto)
- **Retención D30/D60** de la app
- **% con wearable conectado** (valida cuánto invertir en F3/F4 en v2)
- Check-ins/semana (valida el formato ≤10 s)

---

## Backlog v2 (documentado — qué y por qué quedó afuera)

| # | Feature | Por qué es v2 y no MVP |
|---|---|---|
| 1 | **Fotos de piel guiadas** (progreso con cámara frontal, misma luz/distancia/encuadre, comparador antes/después) | El outcome más validado de la luz roja y el más compartible, pero la UX de captura consistente (alineación de cara, control de luz ambiente) es un proyecto en sí mismo. Hacerlo mal genera comparaciones engañosas. |
| 2 | **Experimentos guiados N-of-1** (protocolo A/B de 4 semanas: ej. sesión mañana vs. noche, con medición antes/después) | Necesita el baseline de F4 maduro y usuarios con hábito formado. Es EL feature de retención de largo plazo. |
| 3 | **Motor de correlaciones con confounders** (entrenamiento, ciclo menstrual, alcohol, viajes) | Sin volumen de datos reales, sobreajusta y miente. Primero acumular meses de datos de usuarios reales. |
| 4 | **Métricas secundarias de wearable**: temperatura de muñeca, SpO2 nocturno, frecuencia respiratoria | Señal más débil y menos universal entre dispositivos; suman ruido a la UI del MVP. |
| 5 | **APIs nativas Whoop / Oura** (recovery score, readiness) | HealthKit/Health Connect ya trae las métricas crudas; los scores propietarios requieren integración y aprobación por vendor. Decidir según "% con wearable" del MVP. |
| 6 | **Ciclo menstrual como variable de control** | Depende del motor de #3; sin él, mostrarlo es cosmético. |
| 7 | **Coach adaptativo / recordatorios inteligentes** (ajusta protocolo según datos; posible capa Gemini) | Requiere F4 + #3 funcionando. En MVP los recordatorios son fijos por protocolo. |
| 8 | **Reporte PDF exportable** (para llevar a médico/entrenador) | Nice-to-have de credibilidad; cero urgencia. |
| 9 | **Multi-usuario por panel** (hogar comparte panel, cada uno su perfil) | Complejidad de cuentas; validar primero si pasa en la vida real. |
| 10 | **Comunidad / retos** (reto 30 días, rachas compartidas) | Palanca de retención social, pero sin masa crítica de usuarios es una plaza vacía. |
| 11 | **Cross-sell ecosistema** (ej. stack "energía": sesión matinal + Brain Boost) | Primero la app tiene que ganarse la confianza como herramienta, no como catálogo. |

---

## Riesgos y decisiones abiertas

- **Riesgo #1 — prometer biometría**: si el marketing de la app promete "mirá cómo mejora tu HRV", la mayoría verá una línea plana 1 mes. Mensaje de lanzamiento centrado en protocolo + adherencia + percepción subjetiva.
- **Tabla de irradiancia**: bloqueante de hardware (ver Modelo de dosis). Dueño: Andrés, requiere solar power meter.
- **iOS vs Android primero**: si la preventa muestra mayoría iPhone, se puede shippear iOS-only 1 mes antes. Decidir con datos de los compradores de preventa.
- **Nombre de la app en stores**: atado a la verificación de marca Lumé en INPI (pendiente en [[01-projects/lume/index]]).

## Estado de implementación (jul 22, 2026)

MVP v0.1 **construido** en `~/lume-app` (Expo SDK 57 + expo-router + TypeScript, spec-kit inicializado, artefactos en `specs/001-mvp/`). Implementado y verificado en web: F1 sesiones con timer + dosis real (forzada a 30 cm hasta medir más distancias), F2 check-in ≤10s, F4 comparación honesta días con/sin sesión (sobre energía subjetiva), F5 protocolos + 8 píldoras educativas. F3 (wearables) quedó como interfaz stub en `src/health/` — requiere development build (EAS), no funciona en Expo Go.

**Próximos pasos**: probar en iPhone vía Expo Go (`npx expo start` + QR) · dev build EAS para HealthKit/Health Connect · medir irradiancia 10/15/20/45 cm (bloqueante hardware) · íconos/splash con branding real · decidir iOS vs Android first con datos de preventa.
