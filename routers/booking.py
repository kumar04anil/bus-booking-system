# routers/booking.py
from fastapi import APIRouter, HTTPException, Body
from models import BookingCreate
from services.pnr_service import confirm_booking
from services.cancellation import calculate_refund, cancel_booking
from services.seat_service import (
    generate_seat_grid, lock_seats, release_locks, prune_expired_locks
)
import moc_data as db
router = APIRouter(prefix="/api/booking", tags=["Booking"])
@router.get("/seats/{trip_id}")
def get_seat_map(trip_id: str, from_stop: str, to_stop: str):
    if trip_id not in db.TRIPS:
        raise HTTPException(404, "Trip not found")
    prune_expired_locks(trip_id)
    grid = generate_seat_grid(trip_id, from_stop, to_stop)
    trip = db.TRIPS[trip_id]
    return {
        "trip_id": trip_id,
        "from_stop": from_stop,
        "to_stop": to_stop,
        "lock_duration_seconds": 600,
        "grid": grid,
    }
@router.post("/lock")
def lock_selected_seats(
    trip_id: str = Body(...),
    seat_numbers: list[str] = Body(...)
):
    try:
        lock_seats(trip_id, seat_numbers)
        return {"locked": True, "seats": seat_numbers, "expires_in_seconds": 600}
    except ValueError as e:
        raise HTTPException(400, str(e))
@router.post("/release")
def release_selected_seats(
    trip_id: str = Body(...),
    seat_numbers: list[str] = Body(...)
):
    release_locks(trip_id, seat_numbers)
    return {"released": True}
@router.post("/confirm")
def create_booking(booking_req: BookingCreate):
    try:
        result = confirm_booking(booking_req)
        return result
    except ValueError as e:
        raise HTTPException(400, str(e))
@router.get("/{booking_id}")
def get_booking(booking_id: str):
    booking = db.BOOKINGS.get(booking_id)
    if not booking:
        raise HTTPException(404, "Booking not found")
    return booking
@router.get("/pnr/{pnr}")
def get_booking_by_pnr(pnr: str):
    for b in db.BOOKINGS.values():
        if b.pnr == pnr:
            return b
    raise HTTPException(404, "PNR not found")
@router.get("/refund/{booking_id}")
def get_refund_estimate(booking_id: str):
    try:
        return calculate_refund(booking_id)
    except ValueError as e:
        raise HTTPException(400, str(e))
@router.post("/cancel/{booking_id}")
def cancel(booking_id: str):
    try:
        return cancel_booking(booking_id)
    except ValueError as e:
        raise HTTPException(400, str(e))
@router.get("/user/{user_id}")
def get_user_bookings(user_id: str):
    bookings = [b for b in db.BOOKINGS.values() if b.user_id == user_id]
    return {"bookings": bookings, "count": len(bookings)}