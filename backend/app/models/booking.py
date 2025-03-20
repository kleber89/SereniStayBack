from pydantic import Field, field_validator
from typing import List, Literal
from datetime import datetime
from app.models.base_model import BaseEntity

class Booking(BaseEntity):
    user_id: str
    spa_id: str
    services_id: List[str]
    reservation_datetime: datetime
    status: Literal["pending", "confirmed", "cancelled"] = Field(default="pending")


    @field_validator("reservation_datetime", mode="before")
    @classmethod
    def validate_datetime(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)  # Convierte string a datetime
        return value
    
