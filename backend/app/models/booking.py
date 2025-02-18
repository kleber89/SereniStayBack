from pydantic import Field, field_validator, ValidationError
from typing import List
from uuid import UUID, uuid4
from datetime import datetime, timezone
from app.models.base_model import BaseEntity
from app.models.service import Service

class Booking(BaseEntity):
    user_id: UUID
    services: List[Service]
    total_amount: float
    booking_date: datetime
    status: str = Field(..., pattern="^(pending|confirmed|cancelled)$")


    @field_validator("booking_date", mode="before")
    def validate_booking_date(cls, booking_date: datetime) -> datetime:
        if booking_date.tzinfo is None:
            booking_date = booking_date.replace(tzinfo=timezone.utc)  # Convertir a UTC si no tiene zona horaria

        if booking_date < datetime.now(timezone.utc):
            raise ValueError("The booking date cannot be in the past.")

        return booking_date