---
date: 2026-05-31
type: refactor-plan
tags: [salto-cuantico, korean-root, refactor, backlog]
status: backlog
estimated_effort: 3-4 hours
priority: media
---

# Salto Cuántico — Plan de split del router monolítico

## Contexto

El router `backend/routers/salto_cuantico.py` tiene **2437 líneas** y 46 endpoints. Los 4 reviewers (python-reviewer, typescript-reviewer, security-reviewer, code-reviewer) coincidieron en que es la deuda técnica más grande pendiente. Pero el riesgo de regresión durante el split (helpers compartidos, imports cruzados, validators Pydantic) hizo que se postpone hasta una sesión dedicada donde se pueda invertir tiempo en tests E2E completos antes y después.

Mientras tanto el archivo tiene TOC navegable y boundaries claras por sección (`# §N`).

## Estructura propuesta

```
routers/
├── salto_cuantico/
│   ├── __init__.py            (~12 LOC)  APIRouter compuesto
│   ├── _shared.py             (~150)     helpers + modelos Pydantic comunes
│   ├── portal.py              (~450)     GET/POST /portal/{slug}/*
│   ├── admin_setup.py         (~280)     setup-checklist + settings + notify-kr
│   ├── admin_orders.py        (~280)     orders + queue + retry
│   ├── admin_dispatcher.py    (~200)     dispatcher/tick/status + blackouts
│   ├── admin_customers.py     (~200)     customers + unsubs + wa-inbound/status
│   ├── admin_content.py       (~480)     templates + assets + content CRUD
│   ├── admin_coupons.py       (~120)     coupons list + issue-manual
│   └── admin_metrics.py       (~280)     funnel + metrics + health
```

Total ~2450 LOC en 10 archivos (~245 LOC promedio).

## Procedimiento seguro

1. **Tests E2E baseline** antes de tocar nada
2. **Split incremental** (1 módulo por vez con verify)
3. **Move helpers** a `_shared.py`
4. **`__init__.py`** agrega routers
5. **`main.py` no cambia** (package exporta el mismo nombre)
6. **Verificar tests E2E** después de cada split

## Por qué no se hizo en sesión actual

1. Riesgo de regresión alto vs. beneficio inmediato bajo (sistema en dry-run)
2. Falta tiempo para tests E2E exhaustivos entre cada split
3. El TOC mejora navegabilidad al 70% sin tocar código
4. Otras deudas técnicas con mayor impacto operacional inmediato

## Cuándo agendar

- KR contrate otro dev
- Sumemos un 4to producto anchor
- Archivo crezca arriba de 3000 LOC
- Decidamos hacer multi-tenant (split + parametrización van juntos)
