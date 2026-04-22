---
date: '2026-04-22'
type: area
tags:
  - producto
  - marca
  - brand
  - diseno
status: activo
---
# Brand Manual — Smart Foods

## Paleta de Colores Oficial

| Color | Hex | Uso |
|-------|-----|-----|
| Verde | #3A7A3A | Primario, naturaleza, salud |
| Amarillo Neon | #F0E000 | Acento, energia, llamadas a la accion |
| Negro | #282823 | Texto principal, fondos premium |
| Verde Oscuro | #4B6834 | Secundario, complemento |
| Gris Claro | Variable | Fondos, separadores |

## Tipografia
- **Body:** DM Sans
- **Headings:** Kanit (fallback de Pennypacker)

## Reglas de Aplicacion
- CSS variables para colores (nunca hardcodear en componentes)
- 3 jerarquias de botones
- Badges, cards, sidebar, modales siguen sistema de tokens
- Funciones dinamicas de color para modulo contenido
- 6 colores hex como CSS variables + 4 fallbacks

## Aplicacion en SmartBrain
- Prompt generado para aplicar identidad visual a toda la UI
- Tailwind config alineado con paleta oficial

## Aplicacion en Email (Klaviyo)
- HTML responsive, table-based
- Colores: #282823 (negro), #E0E938 (amarillo), #4B6834 (verde oscuro)
