from app.models import Customer
from app.pagination import clamp_limit, decode_cursor, encode_cursor
from app.repositories import customer_repo


def list_customers(cursor: str | None, limit: int) -> tuple[list[Customer], str | None]:
    limit = clamp_limit(limit)
    after_id = decode_cursor(cursor)
    rows = customer_repo.fetch_page(after_id, limit + 1)
    has_more = len(rows) > limit
    rows = rows[:limit]
    next_cursor = encode_cursor(rows[-1]["id"]) if has_more and rows else None
    return [Customer(**r) for r in rows], next_cursor


def get_customer(customer_id: int) -> Customer | None:
    row = customer_repo.fetch_by_id(customer_id)
    return Customer(**row) if row else None
