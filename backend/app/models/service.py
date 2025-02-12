from pydantic import BaseModel, Field, field_validator
from decimal import Decimal

class Service(BaseModel):
    title: str = Field(..., min_length=1, max_length=40)
    description: str = Field(..., min_length=1, max_length=350)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    currency: str = "COP"
    duration: int = Field(..., gt=0, lt=300)
