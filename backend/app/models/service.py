from pydantic import BaseModel, Field, field_validator
from decimal import Decimal

class Service(BaseModel):
    title: str = Field(..., min_length=1, max_length=40)
    description: str = Field(..., min_length=1, max_length=350)
    price: Decimal = Field(..., gt=0) #gt: the price must be greater than 0.
    currency: str = "COP"
    duration: int = Field(..., gt=0, lt=300) #gt: the time must be greater than 0 minutes and minor than 300 minutes.

    
    @field_validator("price", mode="before")
    def veridate_price(cls, price):
        "can only have 2 decimal places"

        return Decimal(f"{price:.2f}")
