from fastapi import APIRouter, HTTPException

from app.services import order_service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("")
def list_orders():
    orders = order_service.list_orders()
    return {"data": [o.model_dump() for o in orders], "meta": {"count": len(orders)}}


@router.get("/{order_id}")
def get_order(order_id: int):
    order = order_service.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="order not found")
    return {"data": order.model_dump(), "meta": {}}
