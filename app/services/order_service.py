from app.models import Order
from app.repositories import order_repo


def list_orders() -> list[Order]:
    return [Order(**r) for r in order_repo.fetch_all()]


def get_order(order_id: int) -> Order | None:
    row = order_repo.fetch_by_id(order_id)
    return Order(**row) if row else None


def monthly_revenue_krw(orders: list[Order]) -> dict[str, int]:
    totals: dict[str, int] = {}
    for order in orders:
        if order.status == "CANCELLED":
            continue
        month = order.created_at[:7]
        totals[month] = totals.get(month, 0) + order.amount_krw
    return totals
