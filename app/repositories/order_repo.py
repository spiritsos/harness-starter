from app.db import get_connection

COLUMNS = "id, customer_id, status, amount_krw, created_at"


def fetch_all() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(f"SELECT {COLUMNS} FROM orders ORDER BY id").fetchall()
    return [dict(r) for r in rows]


def fetch_by_id(order_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(f"SELECT {COLUMNS} FROM orders WHERE id = ?", (order_id,)).fetchone()
    return dict(row) if row else None
