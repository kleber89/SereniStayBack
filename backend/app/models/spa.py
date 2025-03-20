from app.models.base_model import BaseEntity
from app.models.service import Service
from pydantic import Field
from typing import Optional, List
 
class Spa(BaseEntity):
    title: str = Field(..., min_length=1, max_length=40)
    description: Optional[str] = Field(None, max_length=350)
    address: str = Field(..., max_length=30)

class CreateSpa(Spa):
    owner_id: Optional[str] = None

class SpaWithServices(Spa):
    services: List[Service] = []