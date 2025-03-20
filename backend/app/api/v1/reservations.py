from fastapi import APIRouter, HTTPException, Depends
from app.services.facade import Facade
from app.models.booking import Booking
from uuid import UUID

router = APIRouter()
facade = Facade()

@router.post("/api/v1/create_booking")
async def create_reservation(booking: Booking, facade: Facade = Depends()):
    """creating reservations"""

    booking_id = await facade.create_booking(booking.model_dump())
    if not booking_id:
        raise HTTPException(status_code=400, detail="Failed to create reservation")

    return {"success": "Reserve created", "booking_id": str(booking_id)}


@router.put("/api/v1/cancel_booking/{booking_id}/cancel")
async def cancel_reservation(booking_id: str, facade: Facade = Depends()):
    """Cancela una reserva por su ID"""

    success = await facade.delete_booking(booking_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reservation not found or already canceled")

    return {"success": "Reservation cancelled successfully"}


@router.get("/api/v1/bookings")
async def get_all_reservations():
    """show all my reservations"""

    return await facade.get_all_bookings()