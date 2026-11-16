from fastapi import APIRouter, HTTPException, Query

from app.pagination import DEFAULT_LIMIT
from app.services import customer_service

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("")
def list_customers(cursor: str | None = None, limit: int = Query(DEFAULT_LIMIT, ge=1)):
    try:
        items, next_cursor = customer_service.list_customers(cursor, limit)
    except ValueError:
        raise HTTPException(status_code=400, detail="invalid cursor") from None
    return {
        "data": [c.model_dump() for c in items],
        "meta": {"next_cursor": next_cursor, "limit": limit},
    }


@router.get("/{customer_id}")
def get_customer(customer_id: int):
    customer = customer_service.get_customer(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="customer not found")
    return {"data": customer.model_dump(), "meta": {}}
