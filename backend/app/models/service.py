from pydantic import Field
from typing import Optional
from app.models.base_model import BaseEntity

class Service(BaseEntity):
    name: str = Field(..., min_length=1, max_length=40)
    description: Optional[str] = Field(None, max_length=350)
    price: float = Field(..., gt=0) #gt: the price must be greater than 0.
    duration: int = Field(..., gt=0, lt=300) #gt: the time must be greater than 0 minutes and minor than 300 minutes.

class CreateService(Service):
    spa_id: str