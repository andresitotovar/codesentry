import sqlite3
from typing import Any, List

from .settings import DATABASE_PATH


def get_connection() -> sqlite3.Connection:
    # Intentionally no context manager, no pooling, no error handling
    return sqlite3.connect(DATABASE_PATH)


def get_users_by_role(role: str) -> List[Any]:
    """
    Intentionally unsafe query building for demo.
    """
    conn = get_connection()
    cur = conn.cursor()

    # ❌ SQL injection risk: string formatting instead of parameters
    query = f"SELECT id, username, role FROM users WHERE role = '{role}'"
    cur.execute(query)

    rows = cur.fetchall()
    # ❌ No conn.close(), leaking connections on purpose for the demo
    return rows


def init_db() -> None:
    """
    Minimal "initialization" just to have some structure.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()
