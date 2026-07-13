import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "kasse.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    connection = get_connection()
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            items TEXT NOT NULL,
            total REAL NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'offen'
        )
        """
    )
    # Beim allerersten Start ist die Tabelle leer. Damit die App danach
    # genauso aussieht wie vorher (mit den bisherigen Beispielprodukten),
    # fuellen wir sie einmalig.
    product_count = connection.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    if product_count == 0:
        connection.executemany(
            "INSERT INTO products (name, price) VALUES (?, ?)",
            [
                ("Kaffee", 2.50),
                ("Brötchen", 1.20),
                ("Wasser 0,5l", 1.00),
                ("Schokoriegel", 1.50),
                ("Apfel", 0.60),
            ],
        )

    connection.commit()
    connection.close()
