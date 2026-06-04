# services/pnr_service.py
import random
import string
import uuid
import time
from datetime import datetime
from models import (
    Booking, Payment, BookingCreate, BookingStatus,
    PaymentStatus, SeatSegmentBooking
)
import moc_data as db
from services.seat_service import release_locks
def _generate_pnr() -> str:
    prefix = "BUS"
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"{prefix}{suffix}"
def _calculate_fare(trip_id: str, seat_count: int) -> dict:
    trip = db.TRIPS.get(trip_id)
    if not trip:
        raise ValueError("Trip not found")
    base_total       = trip.base_fare * seat_count
    gst_amount       = round(base_total * trip.gst_rate, 2)
    convenience_fee  = trip.convenience_fee
    grand_total      = round(base_total + gst_amount + convenience_fee, 2)
    return {
        "base_fare_per_seat": trip.base_fare,
        "seat_count": seat_count,
        "base_total": base_total,
        "gst_rate": trip.gst_rate,
        "gst_amount": gst_amount,
        "convenience_fee": convenience_fee,
        "grand_total": grand_total,
    }
def confirm_booking(booking_req: BookingCreate) -> dict:
    trip = db.TRIPS.get(booking_req.trip_id)
    if not trip:
        raise ValueError("Trip not found")
    seat_numbers = [p.seat_number for p in booking_req.passengers]
    if len(seat_numbers) > 6:
        raise ValueError("Maximum 6 seats per transaction")
    # Fare calculation
    fare = _calculate_fare(booking_req.trip_id, len(seat_numbers))
    # Mock payment — always succeeds in mock mode
    payment_id  = f"PAY-{uuid.uuid4().hex[:10].upper()}"
    txn_id      = f"TXN-{int(time.time())}"
    payment = Payment(
        id=payment_id,
        booking_id="",             # filled below
        amount=fare["grand_total"],
        method=booking_req.payment_method,
        status=PaymentStatus.SUCCESS,
        transaction_id=txn_id,
    )
    # Create booking
    booking_id = f"BKG-{uuid.uuid4().hex[:8].upper()}"
    pnr = _generate_pnr()
    booking = Booking(
        id=booking_id,
        pnr=pnr,
        trip_id=booking_req.trip_id,
        user_id=booking_req.user_id,
        from_stop=booking_req.from_stop,
        to_stop=booking_req.to_stop,
        passengers=booking_req.passengers,
        seat_numbers=seat_numbers,
        status=BookingStatus.CONFIRMED,
        total_amount=fare["grand_total"],
        payment_id=payment_id,
        booked_at=datetime.now(),
    )
    payment.booking_id = booking_id
    # Persist to mock store
    db.BOOKINGS[booking_id] = booking
    db.PAYMENTS[payment_id] = payment
    # Record segment bookings in seat map
    seat_map = db.SEAT_MAPS.setdefault(
        booking_req.trip_id,
        __import__("models").TripSeatMap(trip_id=booking_req.trip_id)
    )
    for passenger in booking_req.passengers:
        seg = SeatSegmentBooking(
            seat_number=passenger.seat_number,
            booked_from_stop=booking_req.from_stop,
            booked_to_stop=booking_req.to_stop,
            passenger_gender=passenger.gender,
        )
        seat_map.bookings.setdefault(passenger.seat_number, []).append(seg)
    # Release locks
    release_locks(booking_req.trip_id, seat_numbers)
    return {
        "booking_id": booking_id,
        "pnr": pnr,
        "trip_id": booking_req.trip_id,
        "fare_breakdown": fare,
        "payment": {
            "id": payment_id,
            "txn_id": txn_id,
            "method": booking_req.payment_method,
            "status": "success",
        },
        "seats": seat_numbers,
        "status": "confirmed",
    }