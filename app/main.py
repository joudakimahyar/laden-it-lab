from contextlib import asynccontextmanager
from datetime import datetime, timezone
import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.database import get_connection, init_db
from app.receipt import generate_receipt_pdf

STATIC_DIR = "static"


def fetch_products() -> list[dict]:
    connection = get_connection()
    rows = connection.execute("SELECT id, name, price FROM products ORDER BY id").fetchall()
    connection.close()
    return [dict(row) for row in rows]


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


class ProductIn(BaseModel):
    name: str
    price: float

class TicketIn(BaseModel):
    title: str
    description: str
    priority: str

class TicketStatusUpdate(BaseModel):
    status: str

@app.get("/")
def read_index() -> FileResponse:
    return FileResponse(f"{STATIC_DIR}/index.html")


@app.get("/artikel")
def read_articles_page() -> FileResponse:
    return FileResponse(f"{STATIC_DIR}/articles.html")


@app.get("/bericht")
def read_report_page() -> FileResponse:
    return FileResponse(f"{STATIC_DIR}/report.html")

@app.get("/tickets")
def read_tickets_page() -> FileResponse:
    return FileResponse(f"{STATIC_DIR}/tickets.html")

@app.get("/api/products")
def get_products() -> list[dict]:
    return fetch_products()


@app.post("/api/products")
def create_product(product: ProductIn) -> dict:
    if not product.name.strip():
        raise HTTPException(status_code=400, detail="Name darf nicht leer sein")
    if product.price < 0:
        raise HTTPException(status_code=400, detail="Preis darf nicht negativ sein")

    connection = get_connection()
    cursor = connection.execute(
        "INSERT INTO products (name, price) VALUES (?, ?)",
        (product.name.strip(), product.price),
    )
    connection.commit()
    new_id = cursor.lastrowid
    connection.close()

    return {"id": new_id, "name": product.name.strip(), "price": product.price}


@app.put("/api/products/{product_id}")
def update_product(product_id: int, product: ProductIn) -> dict:
    if not product.name.strip():
        raise HTTPException(status_code=400, detail="Name darf nicht leer sein")
    if product.price < 0:
        raise HTTPException(status_code=400, detail="Preis darf nicht negativ sein")

    connection = get_connection()
    cursor = connection.execute(
        "UPDATE products SET name = ?, price = ? WHERE id = ?",
        (product.name.strip(), product.price, product_id),
    )
    connection.commit()
    updated = cursor.rowcount
    connection.close()

    if updated == 0:
        raise HTTPException(status_code=404, detail="Artikel nicht gefunden")

    return {"id": product_id, "name": product.name.strip(), "price": product.price}


@app.delete("/api/products/{product_id}")
def delete_product(product_id: int) -> dict:
    connection = get_connection()
    cursor = connection.execute("DELETE FROM products WHERE id = ?", (product_id,))
    connection.commit()
    deleted = cursor.rowcount
    connection.close()

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Artikel nicht gefunden")

    return {"ok": True}


@app.post("/api/sale")
def create_sale(sale: Sale) -> dict:
    if not sale.items:
        raise HTTPException(status_code=400, detail="Warenkorb ist leer")

    products_by_id = {product["id"]: product for product in fetch_products()}
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
    created_at = datetime.now(timezone.utc).isoformat()
    connection = get_connection()
    cursor = connection.execute(
        "INSERT INTO sales (created_at, items, total) VALUES (?, ?, ?)",
        (created_at, json.dumps(sale_items), total),
    )
    connection.commit()
    sale_id = cursor.lastrowid
    connection.close()

    return {"id": sale_id, "total": total, "items": sale_items}


@app.get("/api/sale/{sale_id}/receipt")
def get_sale_receipt(sale_id: int) -> Response:
    connection = get_connection()
    row = connection.execute(
        "SELECT id, created_at, items, total FROM sales WHERE id = ?", (sale_id,)
    ).fetchone()
    connection.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Verkauf nicht gefunden")

    items = json.loads(row["items"])
    pdf_bytes = generate_receipt_pdf(row["id"], row["created_at"], items, row["total"])

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="beleg-{sale_id}.pdf"'},
    )


@app.get("/api/report")
def get_report(date: str | None = None) -> dict:
    if date is None:
        report_date = datetime.now(timezone.utc).date().isoformat()
    else:
        try:
            report_date = datetime.strptime(date, "%Y-%m-%d").date().isoformat()
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Datum muss im Format JJJJ-MM-TT sein"
            )

    connection = get_connection()
    row = connection.execute(
        "SELECT COUNT(*) AS count, COALESCE(SUM(total), 0) AS total "
        "FROM sales WHERE created_at LIKE ?",
        (f"{report_date}%",),
    ).fetchone()
    connection.close()

    return {"date": report_date, "count": row["count"], "total": round(row["total"], 2)}
@app.get("/api/tickets")
def get_tickets() -> list[dict]:
    connection = get_connection()
    rows = connection.execute(
        "SELECT id, created_at, title, description, priority, status FROM tickets ORDER BY id DESC"
    ).fetchall()
    connection.close()
    return [dict(row) for row in rows]


@app.post("/api/tickets")
def create_ticket(ticket: TicketIn) -> dict:
    if not ticket.title.strip():
        raise HTTPException(status_code=400, detail="Titel darf nicht leer sein")
    if ticket.priority not in ("niedrig", "mittel", "hoch"):
        raise HTTPException(status_code=400, detail="Priorität muss niedrig, mittel oder hoch sein")

    created_at = datetime.now(timezone.utc).isoformat()
    connection = get_connection()
    cursor = connection.execute(
        "INSERT INTO tickets (created_at, title, description, priority, status) VALUES (?, ?, ?, ?, 'offen')",
        (created_at, ticket.title.strip(), ticket.description.strip(), ticket.priority),
    )
    connection.commit()
    new_id = cursor.lastrowid
    connection.close()

    return {
        "id": new_id,
        "created_at": created_at,
        "title": ticket.title.strip(),
        "description": ticket.description.strip(),
        "priority": ticket.priority,
        "status": "offen",
    }


@app.put("/api/tickets/{ticket_id}")
def update_ticket_status(ticket_id: int, update: TicketStatusUpdate) -> dict:
    if update.status not in ("offen", "in Bearbeitung", "gelöst"):
        raise HTTPException(status_code=400, detail="Status muss offen, in Bearbeitung oder gelöst sein")

    connection = get_connection()
    cursor = connection.execute(
        "UPDATE tickets SET status = ? WHERE id = ?",
        (update.status, ticket_id),
    )
    connection.commit()
    updated = cursor.rowcount
    connection.close()

    if updated == 0:
        raise HTTPException(status_code=404, detail="Ticket nicht gefunden")

    return {"id": ticket_id, "status": update.status}
