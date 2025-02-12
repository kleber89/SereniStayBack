from pydantic import BaseModel, Field, field_validator
from typing import List

class Spa(BaseModel):
    title: str = Field(..., min_length=1, max_length=40)
    description: str = Field(..., min_length=1, max_length=350)
    service: List[str] = Field(..., min_items=1, max_items=30)
    address: str = Field(..., min_length=1, max_length=30)


    @field_validator("service", mode="each")
    def validate_service_item(cls, service):
        if len(service) < 1 or len(service) > 30:
            raise ValueError("Each service name must be between 1 and 30 characters.")
        return service
