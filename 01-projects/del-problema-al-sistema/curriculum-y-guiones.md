---
date: 2026-06-21
type: project
tags: [del-problema-al-sistema, cohorte, curriculum, guion, educacion]
status: en-progreso
---

# Currículum y guion clase por clase — Del Problema al Sistema

Cohorte Fundadora · 5 encuentros en vivo · viernes 10:00 hs (Arg), 90 min.
Caso testigo: **empleado de ventas en WhatsApp**. Volver al [[index|índice del proyecto]].

## Principios que rigen todo el diseño

- **Construcción espejo:** Andrés muestra la etapa en el caso testigo, y en la misma clase cada alumno la replica en *su* problema. Si miran más de lo que teclean, la clase falló.
- **Cada clase termina con algo funcionando.** El entregable semanal es el checkpoint que blinda la garantía: si lo cumplieron, van bien; si no, se agarra ahí, no en la semana 5.
- **Blindar los bordes.** El cuello de botella del no-técnico no es el código, es el criterio de borde (setup, deploy, leer un error). Se resuelve con entornos preconfigurados, plantillas y un plan B en la nube.
- **El canal es intercambiable.** Los alumnos practican sobre un canal de cero fricción (Telegram / widget web). WhatsApp oficial (WABA) queda para producción y es upsell.
- **Mindset > herramienta.** Se enseña a pensar el problema, no a memorizar Claude Code. El harness es el cómo, no el qué.

## Estructura fija de cada encuentro (90 min)

| Bloque | Tiempo | Qué pasa |
|---|---|---|
| Arranque · mindset | ~15' | El concepto de la etapa y el cambio de cabeza que trae |
| Demo en vivo | ~30' | Andrés construye la etapa en el caso testigo, a la vista |
| Construcción espejo | ~35' | Cada uno lo hace en su negocio; Andrés acompaña |
| Cierre + checkpoint | ~10' | Qué dejan funcionando + tarea async para la próxima |

---

## Semana 0 — Pre-work (antes del viernes 17/7)

Asincrónico, con guía paso a paso + video. Objetivo: llegar a la clase 1 con el entorno andando, no peleándose con la terminal.

- Instalar Claude Code y dejar acceso al entorno/servidor listo (kit preconfigurado).
- Correr un "hola mundo" para verificar que todo funciona.
- Traer pensados 2-3 candidatos de problema del propio negocio.
- **Plan B:** entorno en la nube preconfigurado para quien no logre el setup local — nadie pierde la clase 1 por esto.

---

## Semana 1 — DETECTAR · viernes 17/7

**Objetivo:** que cada alumno elija y defina con precisión el problema que va a convertir en sistema.
**Shift:** casi nadie tiene un problema de IA; tiene un problema mal definido. Una tarea repetitiva basada en información es delegable a una máquina (operario → arquitecto).

**00:00–00:15 · Arranque / mindset**
- Bienvenida + mostrar el caso testigo YA andando: "esto es lo que vas a tener vos en 5 semanas".
- Operario vs arquitecto: no vinieron a aprender IA, vinieron a sacarse un problema de encima construyendo la máquina que lo hace.
- Criterio para elegir UN problema: repetitivo + basado en información + alto dolor/ROI + dentro de alcance.

**00:15–00:45 · Demo en vivo**
- Andrés piensa en voz alta cómo detectó "pierdo ventas porque no contesto a tiempo".
- Lo descompone: ¿qué tarea exacta? ¿qué info necesita? ¿qué decisión toma? ¿dónde empieza y termina el trabajo?
- Lo enuncia en una frase y lo escribe como mini-brief.

**00:45–01:20 · Construcción espejo**
- Cada alumno lista sus tareas repetitivas (plantilla).
- Filtran con una matriz dolor vs alcance y eligen UNA.
- La enuncian en una frase + definen el "trabajo" que hará.
- Andrés rota y ayuda a acotar.

**01:20–01:30 · Cierre + checkpoint**
- Ronda rápida: cada uno comparte su frase.
- **Checkpoint:** problema en una frase + trabajo definido + entorno verificado andando.
- **Tarea async:** refinar la frase + empezar a juntar el material de conocimiento (catálogo, FAQ, info del negocio).

**Fricciones a anticipar**
- Eligen algo demasiado grande → forzar a acotar a un caso de uso.
- Eligen algo que requiere juicio humano puro (no delegable) → reorientar.
- Entorno no quedó del pre-work → mandar al plan B en la nube.

---

## Semana 2 — TRADUCIR · viernes 24/7

**Objetivo:** convertir el problema en instrucciones que una IA ejecuta.
**Shift:** acá vive el corazón del método. La "ficha del empleado IA": qué sabe, qué decide y qué no toca.

**00:00–00:15 · Arranque / mindset**
- Cómo se le "explica" un trabajo a una máquina: conocimiento + decisiones + límites.
- Los tres pilares de la ficha: lo que sabe (KB), lo que decide (lógica), lo que NO hace (guardrails + cuándo deriva a un humano).

**00:15–00:45 · Demo en vivo**
- Andrés escribe la ficha de su empleado de ventas: tono, qué responde, qué no, cuándo escala.
- Arma la base de conocimiento del caso testigo (producto, precios, FAQ).
- Lo prueba en un playground: el prompt ya responde coherente.

**00:45–01:20 · Construcción espejo**
- Cada alumno escribe la ficha de SU agente.
- Carga su base de conocimiento (catálogo / FAQ / info del negocio que juntó de tarea).
- Prueba un primer prompt y ajusta.

**01:20–01:30 · Cierre + checkpoint**
- **Checkpoint:** ficha completa + KB cargada + un primer prompt que responde algo coherente.
- **Tarea async:** completar huecos de la KB; pensar qué canal van a usar.

**Fricciones a anticipar**
- KB pobre o desordenada → dar plantilla de estructura mínima.
- Querer que el agente "haga todo" → recordar el alcance de la semana 1.
- Prompts vagos → enseñar a ser específico con ejemplos.

---

## Semana 3 — CONECTAR · viernes 31/7

**Objetivo:** enchufar el agente al mundo real.
**Shift:** un sistema son piezas que se hablan (canal, datos, APIs), sin tecnicismo. El canal es intercambiable.

**00:00–00:15 · Arranque / mindset**
- Qué es un canal, una API, un webhook — explicado sin jerga.
- Por qué practicamos sobre canal de cero fricción (Telegram/web) y dejamos WhatsApp para producción.

**00:15–00:45 · Demo en vivo**
- Andrés conecta su agente a WhatsApp Web (su demo) y muestra el patrón "conectar piezas".
- Enchufa la base de conocimiento al agente vía el harness.
- Hace contestar un mensaje real de punta a punta.

**00:45–01:20 · Construcción espejo**
- Cada alumno conecta su agente a su canal de baja fricción (Telegram o widget web).
- Conecta su KB.
- Manda un mensaje de prueba y ve la respuesta.

**01:20–01:30 · Cierre + checkpoint**
- **Checkpoint:** el agente recibe un mensaje por su canal y responde con su conocimiento. Primer "está vivo".
- **Tarea async:** dejar el canal estable; listar los casos de venta que el agente debería manejar.

**Fricciones a anticipar**
- Tokens / credenciales del canal mal cargados → checklist de setup + plantilla.
- Confundir "anda en mi prueba" con "está conectado" → mostrar la diferencia en vivo.

---

## Semana 4 — CONSTRUIR · viernes 7/8

**Objetivo:** pasar de "responde preguntas" a "avanza la tarea".
**Shift:** la diferencia entre un bot que contesta y un agente que logra un objetivo. Comportamiento, memoria, guardrails y handoff.

**00:00–00:15 · Arranque / mindset**
- Un FAQ informa; un agente avanza una venta. Qué es un guardrail y un handoff a humano.
- Memoria de conversación: por qué importa que recuerde el hilo.

**00:15–00:45 · Demo en vivo**
- Andrés le da a su agente la lógica de venta: califica, ofrece, cierra o deriva.
- Agrega memoria de conversación y los límites (qué nunca hace, cuándo pasa a un humano).
- Prueba un diálogo completo que termina en una venta/derivación.

**00:45–01:20 · Construcción espejo**
- Cada alumno define el objetivo de su agente y le da el comportamiento para lograrlo.
- Agrega guardrails y la regla de derivación a humano.
- Prueba un diálogo real de su negocio.

**01:20–01:30 · Cierre + checkpoint**
- **Checkpoint:** el agente conversa y avanza la tarea (no solo informa), con guardrails y handoff funcionando.
- **Tarea async:** afinar respuestas con casos reales; preparar el paso a producción.

**Fricciones a anticipar**
- El agente "alucina" o promete de más → guardrails y límites explícitos.
- No sabe cuándo callarse / derivar → definir disparadores de handoff.

---

## Semana 5 — LANZAR · viernes 14/8

**Objetivo:** dejarlo vivo y autónomo en producción.
**Shift:** la distancia entre "anda en mi prueba" y "está en producción 24/7 sin caerse" — deploy, logging, monitoreo, mantenimiento.

**00:00–00:15 · Arranque / mindset**
- Qué cambia al pasar a producción: que no se caiga, que se pueda monitorear, que se mantenga.
- Cómo repetir el método para el PRÓXIMO problema del negocio (que el método quede instalado).

**00:15–00:45 · Demo en vivo**
- Andrés deja su agente corriendo 24/7 en el servidor.
- Muestra logging y monitoreo básico.
- Muestra el paso a WhatsApp oficial (WABA) para producción — **upsell de setup**.

**00:45–01:20 · Construcción espejo**
- Cada alumno deja SU sistema corriendo en su propio servidor.
- Verifica que sigue vivo y que puede ver qué está pasando (logs).

**01:20–01:30 · Cierre + checkpoint**
- **Checkpoint final:** sistema en producción que el alumno usa en su negocio real. La promesa cumplida.
- Cierre del programa + cómo seguir (repetir el método, WABA, comunidad).

**Fricciones a anticipar**
- Anda local pero no en el server → checklist de deploy + plan B.
- Miedo a "soltarlo" → acompañar el primer día en producción.

---

## Transversal

- **Grupo privado** para soporte asincrónico entre clases.
- **Sesiones 1:1 de garantía** para quien quede trabado pese a haber cumplido los checkpoints.
- **Captura de prueba social desde el día 1:** grabar el "antes" (problema en sus palabras) y el "después" (sistema andando). Esos clips venden la segunda cohorte.
