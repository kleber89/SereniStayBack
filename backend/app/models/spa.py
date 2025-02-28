from app.models.base_model import BaseEntity
from pydantic import Field, field_validator
from typing import List, Optional, Dict, Any

class Spa(BaseEntity):
    title: str = Field(..., min_length=1, max_length=40)
    description: Optional[str] = Field(None, max_length=350)
    address: str = Field(..., max_length=30)
    services: List[Dict[str, Any]] = Field(..., min_items=1, max_items=30)

class CreateSpa(Spa):
    owner_id: Optional[str] = None


    @field_validator("services", mode="before")
    def validate_service_item(cls, services):
        for s in services:
            if len(services) < 1 or len(services) > 30:
                raise ValueError("Each service name must be between 1 and 30 characters.")
            return services
