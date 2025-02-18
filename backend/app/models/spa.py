from app.models.service import Service
from app.models.base_model import BaseEntity
from pydantic import Field, field_validator
from typing import List, Optional

class Spa(BaseEntity):
    title: str = Field(..., min_length=1, max_length=40)
    description: Optional[str] = Field(None, max_length=350)
    service: List[Service] = Field(..., min_items=1, max_items=30)
    address: str = Field(..., max_length=30)


    @field_validator("service", mode="before")
    def validate_service_item(cls, service):
        if len(service) < 1 or len(service) > 30:
            raise ValueError("Each service name must be between 1 and 30 characters.")
        return service
