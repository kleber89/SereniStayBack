from pydantic import Field, field_validator, ValidationError
from typing import List
from uuid import UUID, uuid4
from datetime import datetime
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
        if booking_date < datetime.now():
            raise ValueError("The booking date cannot be in the past.")
        return booking_date
    

if __name__ == "__main__":
    # Test 1: Creación válida de una reserva
    print("\n🔹 Test 1: Creación válida de Booking")
    try:
        user_id = uuid4()  # Simulamos un ID de usuario
        services = [
            Service(id=uuid4(), title="Massage", price=50.00, currency="COP", duration=60),
            Service(id=uuid4(), title="Facial", price=40.00, currency="COP", duration=45)
        ]
        booking = Booking(
            id=uuid4(),
            user_id=user_id,
            services=services,
            booking_date=datetime(2025, 2, 20, 15, 30),  # Fecha futura
            total_amount=90.00,
            status="pending",
        )
        print("✅ Booking creado correctamente:", booking.dict())
    except ValidationError as e:
        print("❌ Error:", e)

    # Test 2: Intento de crear una reserva con fecha en el pasado
    print("\n🔹 Test 2: Intento de reserva con fecha pasada")
    try:
        booking = Booking(
            id=uuid4(),
            user_id=user_id,
            services=services,
            booking_date=datetime(2020, 2, 20, 15, 30),  # Fecha pasada
            total_amount=90.00,
            status="confirmed",
        )
    except ValidationError as e:
        print("❌ Error esperado:", e)

    # Test 3: Intento de crear una reserva con servicios vacíos
    print("\n🔹 Test 3: Intento de reserva sin servicios")
    try:
        booking = Booking(
            id=uuid4(),
            user_id=user_id,
            services=[],  # Lista vacía de servicios
            booking_date=datetime(2025, 2, 20, 15, 30),
            total_amount=0.00,
            status="pending",
        )
    except ValidationError as e:
        print("❌ Error esperado:", e)