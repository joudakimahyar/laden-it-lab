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
    connection.commit()
    connection.close()
