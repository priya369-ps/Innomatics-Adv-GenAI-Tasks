from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Cart System API", version="1.0.0")

# ── Product Catalog ────────────────────────────────────────────────────────────
products = [
    {"product_id": 1, "name": "Wireless Mouse",  "price": 499, "in_stock": True},
    {"product_id": 2, "name": "Notebook",         "price": 99,  "in_stock": True},
    {"product_id": 3, "name": "USB Hub",          "price": 799, "in_stock": False},
    {"product_id": 4, "name": "Pen Set",          "price": 49,  "in_stock": True},
]

# ── In-memory state ────────────────────────────────────────────────────────────
cart   = []   # list of cart items
orders = []   # list of placed orders
order_counter = 0  # auto-increment order_id


# ── Schemas ────────────────────────────────────────────────────────────────────
class CheckoutRequest(BaseModel):
    customer_name:    str
    delivery_address: str


# ── Helper ─────────────────────────────────────────────────────────────────────
def get_product(product_id: int):
    """Return product dict or raise 404."""
    for p in products:
        if p["product_id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail=f"Product with id={product_id} not found")


# ══════════════════════════════════════════════════════════════════════════════
# CART ENDPOINTS
# ══════════════════════════════════════════════════════════════════════════════

@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int = 1):
    """Add a product to the cart, or increase its quantity if already present."""

    # 1. Find product (404 if missing)
    product = get_product(product_id)

    # 2. Check stock (400 if out of stock)
    if not product["in_stock"]:
        raise HTTPException(status_code=400, detail=f"{product['name']} is out of stock")

    # 3. If already in cart → update quantity
    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            item["subtotal"]  = item["unit_price"] * item["quantity"]
            return {"message": "Cart updated", "cart_item": item}

    # 4. New item → append
    cart_item = {
        "product_id":   product_id,
        "product_name": product["name"],
        "quantity":     quantity,
        "unit_price":   product["price"],
        "subtotal":     product["price"] * quantity,
    }
    cart.append(cart_item)
    return {"message": "Added to cart", "cart_item": cart_item}


@app.get("/cart")
def view_cart():
    """View all items in the cart with grand total."""
    if not cart:
        return {"message": "Cart is empty"}

    grand_total = sum(item["subtotal"] for item in cart)
    return {
        "items":       cart,
        "item_count":  len(cart),
        "grand_total": grand_total,
    }


@app.delete("/cart/{product_id}")
def remove_from_cart(product_id: int):
    """Remove a product from the cart by product_id."""
    for i, item in enumerate(cart):
        if item["product_id"] == product_id:
            removed = cart.pop(i)
            return {"message": f"{removed['product_name']} removed from cart"}

    raise HTTPException(status_code=404, detail=f"Product id={product_id} not in cart")


@app.post("/cart/checkout")
def checkout(request: CheckoutRequest):
    """Checkout — creates one order per cart item, then clears the cart."""
    global order_counter

    # 400 if cart is empty
    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty — add items first")

    grand_total    = sum(item["subtotal"] for item in cart)
    orders_placed  = []

    for item in cart:
        order_counter += 1
        order = {
            "order_id":        order_counter,
            "customer_name":   request.customer_name,
            "delivery_address": request.delivery_address,
            "product":         item["product_name"],
            "quantity":        item["quantity"],
            "total_price":     item["subtotal"],
        }
        orders.append(order)
        orders_placed.append(order)

    cart.clear()   # empty the cart after checkout

    return {
        "message":      "Checkout successful",
        "orders_placed": orders_placed,
        "grand_total":  grand_total,
    }


# ══════════════════════════════════════════════════════════════════════════════
# ORDERS ENDPOINT
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/orders")
def get_orders():
    """View all placed orders."""
    return {
        "orders":       orders,
        "total_orders": len(orders),
    }


# ── Optional: products list for reference ──────────────────────────────────────
@app.get("/products")
def list_products():
    return {"products": products}