---
date: 2026-04-24
type: spec
tags: [smart-foods, marketing, shopify, cupones]
status: draft
---

# Shopify Discount API Integration

> Parte de [[index|Agente Marketing Autónomo]]

## Responsabilidad

Antes de enviar cualquier campaña con cupón, **crear el PriceRule + DiscountCode en Shopify programáticamente**.

Sin esto, el cupón que mandamos en el email no funciona y matamos conversión + confianza del cliente.

## API version

`SHOPIFY_API_VERSION=2026-01` (en `/etc/smartbrain/.env`).

## Flow completo

```
1. Decision layer decide lanzar campaña
   ↓
2. Genera campaign_id (ej: REACT45-2604-BRAIN15)
   ↓
3. Llama a ShopifyDiscountService.create_discount(...)
   ↓
4. Shopify responde con price_rule_id + discount_code_id
   ↓
5. Update campaign_attribution con los IDs
   ↓
6. Copy generator incluye el code en el copy
   ↓
7. Envío a audiencia
   ↓
8. Si campaña se pausa → ShopifyDiscountService.disable(price_rule_id)
```

## Convención de códigos

`[TIPO]-[DDMM]-[PRODUCTO][VALOR]`

| Tipo | Significado |
|---|---|
| `REACT45` | Reactivación 45d sin compra |
| `REACT90` | Reactivación 90d |
| `B2BREORD` | B2B reorden |
| `STOCK` | Stock alto, rotación lenta |
| `NEWSUB` | Nuevo suscriptor |
| `BDAY` | Cumpleaños / aniversario |
| `CARTABN` | Carrito abandonado |
| `VIP` | Top 50 D2C |

Ejemplos:
- `REACT45-2604-BRAIN15` — reactivación 45d, 26-abr, Brain Boost, 15% off
- `STOCK-IMMUNE-2604-20` — stock alto Immune, 26-abr, 20% off
- `CARTABN-2604-ALL10` — carrito abandonado, 10% off todo

## Servicio: `services/shopify_discount.py`

```python
import os
import httpx
from datetime import datetime, timedelta
from typing import Optional, Literal

SHOPIFY_SHOP = os.getenv("SHOPIFY_SHOP")  # smartfoods-arg.myshopify.com
SHOPIFY_TOKEN = os.getenv("SHOPIFY_TOKEN")
API_VERSION = "2026-01"
BASE = f"https://{SHOPIFY_SHOP}/admin/api/{API_VERSION}"
HEADERS = {"X-Shopify-Access-Token": SHOPIFY_TOKEN, "Content-Type": "application/json"}


async def create_discount(
    code: str,
    value: float,
    value_type: Literal["percentage", "fixed_amount"] = "percentage",
    scope: Literal["all", "collection", "product"] = "all",
    scope_id: Optional[int] = None,
    usage_limit: int = 500,
    expires_days: int = 14,
    combines_with: bool = False,
    customer_selection: Literal["all", "prerequisite"] = "all",
    prerequisite_customer_ids: Optional[list[int]] = None,
) -> dict:
    """
    Crea PriceRule + DiscountCode en Shopify.

    Returns: {price_rule_id, discount_code_id, code, expires_at}
    """
    starts_at = datetime.utcnow().isoformat() + "Z"
    ends_at = (datetime.utcnow() + timedelta(days=expires_days)).isoformat() + "Z"

    # value en Shopify va negativo para descuentos
    shopify_value = f"-{value}" if value_type == "percentage" else f"-{value}"

    price_rule_payload = {
        "price_rule": {
            "title": code,
            "target_type": "line_item",
            "target_selection": scope if scope == "all" else "entitled",
            "allocation_method": "across",
            "value_type": value_type,
            "value": shopify_value,
            "customer_selection": customer_selection,
            "usage_limit": usage_limit,
            "starts_at": starts_at,
            "ends_at": ends_at,
            "allocation_limit": 1,
        }
    }

    if scope == "collection" and scope_id:
        price_rule_payload["price_rule"]["entitled_collection_ids"] = [scope_id]
    elif scope == "product" and scope_id:
        price_rule_payload["price_rule"]["entitled_product_ids"] = [scope_id]

    if customer_selection == "prerequisite" and prerequisite_customer_ids:
        price_rule_payload["price_rule"]["prerequisite_customer_ids"] = prerequisite_customer_ids

    async with httpx.AsyncClient(timeout=30) as client:
        pr_resp = await client.post(
            f"{BASE}/price_rules.json",
            headers=HEADERS,
            json=price_rule_payload,
        )
        pr_resp.raise_for_status()
        price_rule = pr_resp.json()["price_rule"]

        dc_resp = await client.post(
            f"{BASE}/price_rules/{price_rule['id']}/discount_codes.json",
            headers=HEADERS,
            json={"discount_code": {"code": code}},
        )
        dc_resp.raise_for_status()
        discount_code = dc_resp.json()["discount_code"]

    return {
        "price_rule_id": str(price_rule["id"]),
        "discount_code_id": str(discount_code["id"]),
        "code": discount_code["code"],
        "expires_at": ends_at,
    }


async def disable_discount(price_rule_id: str) -> None:
    """
    No borra — setea ends_at a NOW para que deje de funcionar.
    Mantiene el histórico para atribución.
    """
    payload = {
        "price_rule": {
            "id": int(price_rule_id),
            "ends_at": datetime.utcnow().isoformat() + "Z",
        }
    }
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.put(
            f"{BASE}/price_rules/{price_rule_id}.json",
            headers=HEADERS,
            json=payload,
        )
        resp.raise_for_status()


async def get_usage(price_rule_id: str) -> int:
    """Cuántas veces se usó el cupón."""
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(
            f"{BASE}/price_rules/{price_rule_id}.json",
            headers=HEADERS,
        )
        resp.raise_for_status()
        return resp.json()["price_rule"].get("usage_count", 0)
```

## Edge cases

### 1. Shopify falla al crear el cupón

```python
try:
    discount = await create_discount(...)
except httpx.HTTPStatusError as e:
    await mark_campaign_failed(campaign_id, reason=f"shopify_discount_error: {e.response.text}")
    await send_wa_alert(
        phone="5491165973204",
        msg=f"No pude crear cupón {code} en Shopify. Error: {e.response.status_code}. "
            f"Campaña {campaign_id} pausada. Abrí Shopify Admin y revisá."
    )
    return
```

### 2. Código duplicado

Shopify responde 422 "has already been taken". Agregar sufijo aleatorio:
```python
code_final = f"{code}-{random.randint(100, 999)}" if duplicate_error else code
```

### 3. Rate limit (40 req/s bucket)

Wrapper con retry + exponential backoff:
```python
@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
async def create_discount(...): ...
```

### 4. Cupón forwarded / compartido fuera del segmento

`usage_limit` contiene el blast radius. Si campaña es a 1.200 personas con `usage_limit=1200`, peor caso todos fueron usados por gente fuera del segmento — conversión cero pero no perdemos más plata.

Para cupones >20% off o segmentos VIP, usar `customer_selection="prerequisite"` con `prerequisite_customer_ids` = lista de Shopify customer IDs del segmento. Solo esos clientes pueden aplicarlo.

### 5. Cliente aplica cupón pero abandona checkout

Ese order no llega al webhook. No se cuenta como revenue. OK, es correcto — solo atribuimos conversiones reales.

### 6. Cliente aplica 2 cupones (nuestro + otro)

`combines_with_*` controls están en False por default. Shopify rechaza combinar. OK.

### 7. Order de prueba / interno

Skiplist por email interno:
```python
INTERNAL_EMAILS = ["andres@smartfoods.com.ar", "flor@smartfoods.com.ar"]
if order.customer_email in INTERNAL_EMAILS:
    return  # no atribuir
```

## Mapeo scope → producto Smart Foods

| Scope lógico | Shopify collection_id o product_id |
|---|---|
| `brain_boost` | product_id de Brain Boost 50g |
| `immune_boost` | product_id de Immune Boost 50g |
| `inner_glow` | product_id de Inner Glow |
| `longevity` | product_id de Longevity Boost |
| `all_extracts` | collection_id "Extractos" |
| `coffee` | collection_id "Cafés" |
| `bars` | collection_id "Barras" |
| `all` | sin scope, aplica a todo |

Cache los IDs en `ops.db` → tabla `shopify_product_refs(name, shopify_id, type)`. Refrescar semanal.

## Tests pre-deploy

1. Crear cupón `TEST-DISCOUNT-01` via servicio → verificar en Shopify Admin
2. Aplicar en checkout real con carrito → validar descuento aplica
3. Disable el cupón → reintentar → debe rechazar
4. Crear 10 cupones en paralelo → verificar rate limit no explota
5. Intentar crear cupón duplicado → debe fallar con 422, retry agrega sufijo
