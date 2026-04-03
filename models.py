from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: Optional[int] = None

class Product(ProductCreate):
    id: int
