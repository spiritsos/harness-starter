from pydantic import BaseModel


class Customer(BaseModel):
    id: int
    name: str
    email: str
    created_at: str


class Order(BaseModel):
    id: int
    customer_id: int
    status: str
    amount_krw: int
    created_at: str
