from fastapi import FastAPI

from app.api import customers, orders

app = FastAPI(title="Order Service", version="0.3.0")
app.include_router(customers.router)
app.include_router(orders.router)


@app.get("/health")
def health():
    return {"status": "ok"}
