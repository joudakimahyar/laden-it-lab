from contextlib import asynccontextmanager
from datetime import datetime, timezone
import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.database import get_connection, init_db

STATIC_DIR = "static"

# Feste Beispielprodukte fuer den Start. id wird spaeter benutzt, um im
# Warenkorb auf ein Produkt zu verweisen.
PRODUCTS = [
    {"id": 1, "name": "Kaffee", "price": 2.50},
    {"id": 2, "name": "Brötchen", "price": 1.20},
    {"id": 3, "name": "Wasser 0,5l", "price": 1.00},
    {"id": 4, "name": "Schokoriegel", "price": 1.50},
    {"id": 5, "name": "Apfel", "price": 0.60},
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class CartItem(BaseModel):
    product_id: int
    quantity: int


class Sale(BaseModel):
    items: list[CartItem]


@app.get("/")
def read_index() -> FileResponse:
    return FileResponse(f"{STATIC_DIR}/index.html")


@app.get("/api/products")
def get_products() -> list[dict]:
    return PRODUCTS


@app.post("/api/sale")
def create_sale(sale: Sale) -> dict:
    if not sale.items:
        raise HTTPException(status_code=400, detail="Warenkorb ist leer")

    products_by_id = {product["id"]: product for product in PRODUCTS}
    sale_items = []
    total = 0.0

    for item in sale.items:
        product = products_by_id.get(item.product_id)
        if product is None:
            raise HTTPException(
                status_code=400, detail=f"Unbekanntes Produkt: {item.product_id}"
            )
        if item.quantity < 1:
            raise HTTPException(status_code=400, detail="Menge muss mindestens 1 sein")

        line_total = product["price"] * item.quantity
        total += line_total
        sale_items.append(
            {
                "product_id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": item.quantity,
                "line_total": round(line_total, 2),
            }
        )

    total = round(total, 2)
    connection = get_connection()
    connection.execute(
        "INSERT INTO sales (created_at, items, total) VALUES (?, ?, ?)",
        (datetime.now(timezone.utc).isoformat(), json.dumps(sale_items), total),
    )
    connection.commit()
    connection.close()

    return {"total": total, "items": sale_items}
