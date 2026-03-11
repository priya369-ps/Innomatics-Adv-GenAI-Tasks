from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

# -----------------------------
# Products Data
# -----------------------------
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 599, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
    {"id": 4, "name": "USB Cable", "price": 199, "category": "Electronics", "in_stock": False},
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False}
]

# -----------------------------
# Day 1 Endpoints
# -----------------------------

@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }


@app.get("/products/category/{category_name}")
def get_by_category(category_name: str):

    result = [p for p in products if p["category"].lower() == category_name.lower()]

    if not result:
        return {"error": "No products found in this category"}

    return {
        "category": category_name,
        "products": result,
        "total": len(result)
    }


@app.get("/products/instock")
def get_instock():

    available = [p for p in products if p["in_stock"]]

    return {
        "in_stock_products": available,
        "count": len(available)
    }


@app.get("/store/summary")
def store_summary():

    in_stock_count = len([p for p in products if p["in_stock"]])
    out_stock_count = len(products) - in_stock_count
    categories = list(set([p["category"] for p in products]))

    return {
        "store_name": "My E-commerce Store",
        "total_products": len(products),
        "in_stock": in_stock_count,
        "out_of_stock": out_stock_count,
        "categories": categories
    }


@app.get("/products/search/{keyword}")
def search_products(keyword: str):

    results = [p for p in products if keyword.lower() in p["name"].lower()]

    if not results:
        return {"message": "No products matched your search"}

    return {
        "keyword": keyword,
        "results": results,
        "total_matches": len(results)
    }


@app.get("/products/deals")
def get_deals():

    cheapest = min(products, key=lambda p: p["price"])
    expensive = max(products, key=lambda p: p["price"])

    return {
        "best_deal": cheapest,
        "premium_pick": expensive
    }

# -----------------------------
# Day 2 - Product Filter
# -----------------------------

@app.get("/products/filter")
def filter_products(category: Optional[str] = None, min_price: int = 0):

    filtered = [
        p for p in products
        if p["price"] >= min_price and
        (category is None or p["category"].lower() == category.lower())
    ]

    return {
        "filters": {
            "category": category,
            "min_price": min_price
        },
        "results": filtered,
        "total": len(filtered)
    }


# -----------------------------
# Product Price Endpoint
# -----------------------------

@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):

    for p in products:
        if p["id"] == product_id:
            return {
                "name": p["name"],
                "price": p["price"]
            }

    return {"error": "Product not found"}


# -----------------------------
# Customer Feedback
# -----------------------------

feedback_list = []

class CustomerFeedback(BaseModel):
    customer_name: str = Field(min_length=2)
    product_id: int = Field(gt=0)
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)


@app.post("/feedback")
def submit_feedback(feedback: CustomerFeedback):

    feedback_list.append(feedback)

    return {
        "message": "Feedback submitted",
        "total_feedback": len(feedback_list),
        "data": feedback
    }


# -----------------------------
# Product Summary
# -----------------------------

@app.get("/products/summary")
def product_summary():

    in_stock = [p for p in products if p["in_stock"]]
    out_stock = [p for p in products if not p["in_stock"]]

    cheapest = min(products, key=lambda p: p["price"])
    expensive = max(products, key=lambda p: p["price"])

    categories = list(set([p["category"] for p in products]))

    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock),
        "out_of_stock_count": len(out_stock),
        "most_expensive": expensive,
        "cheapest": cheapest,
        "categories": categories
    }