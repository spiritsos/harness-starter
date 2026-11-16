from app.db import get_connection


def fetch_page(after_id: int, limit: int) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, name, email, created_at FROM customers WHERE id > ? ORDER BY id LIMIT ?",
            (after_id, limit),
        ).fetchall()
    return [dict(r) for r in rows]


def fetch_by_id(customer_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, name, email, created_at FROM customers WHERE id = ?", (customer_id,)
        ).fetchone()
    return dict(row) if row else None
