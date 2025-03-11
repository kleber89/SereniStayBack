from pydantic import Field, field_validator
from typing import List, Literal, Optional
from uuid import UUID
from datetime import datetime, timezone
from app.models.base_model import BaseEntity
from app.models.service import Service

class Booking(BaseEntity):
    user_id: UUID
    spa_id: Optional[UUID]
    services: List[Service]
    booking_date: datetime
    status: Literal["pending", "confirmed", "cancelled"] = Field(default="pending")
 

    @field_validator("services", mode="before")
    def validate_services(cls, services):
        if isinstance(services, str):  # Si es un solo UUID en string
            services = [services]
        if not isinstance(services, list) or not services:
            raise ValueError("At least one service must be selected for the booking.")
        return [UUID(s) if isinstance(s, str) else s for s in services]


    @field_validator("booking_date", mode="before")
    def validate_booking_date(cls, booking_date):
        if isinstance(booking_date, str):  # Si es string, convertir a datetime
            booking_date = datetime.fromisoformat(booking_date)

        if booking_date.tzinfo is None:
            booking_date = booking_date.replace(tzinfo=timezone.utc)  # Convertir a UTC si no tiene zona horaria

        if booking_date < datetime.now(timezone.utc):
            raise ValueError("The booking date cannot be in the past.")

        return booking_date