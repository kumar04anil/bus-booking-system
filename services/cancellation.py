# services/cancellation.py
"""
Cancellation refund matrix:
  > 24h before departure  → 90% refund
  4h – 24h before         → 50% refund
  < 4h before             → 0% refund
"""
from datetime import datetime, date, timedelta
from models import Booking, Trip, BookingStatus
import moc_data as db
def _get_departure_datetime(trip: Trip) -> datetime:
    h, m = map(int, trip.departure_time.split(":"))
    return datetime.combine(trip.journey_date, datetime.min.time().replace(hour=h, minute=m))
def calculate_refund(booking_id: str) -> dict:
    booking = db.BOOKINGS.get(booking_id)
    if not booking:
        raise ValueError("Booking not found")
    if booking.status == BookingStatus.CANCELLED:
        raise ValueError("Booking already cancelled")
    trip = db.TRIPS.get(booking.trip_id)
    if not trip:
        raise ValueError("Trip not found")
    departure_dt = _get_departure_datetime(trip)
    now = datetime.now()
    hours_remaining = (departure_dt - now).total_seconds() / 3600
    if hours_remaining > 24:
        refund_pct = 0.90
        policy = "> 24h before departure"
    elif hours_remaining >= 4:
        refund_pct = 0.50
        policy = "4–24h before departure"
    else:
        refund_pct = 0.00
        policy = "< 4h before departure"
    refund_amount = round(booking.total_amount * refund_pct, 2)
    return {
        "booking_id": booking_id,
        "pnr": booking.pnr,
        "total_paid": booking.total_amount,
        "refund_percentage": int(refund_pct * 100),
        "refund_amount": refund_amount,
        "hours_to_departure": round(hours_remaining, 1),
        "policy": policy,
        "cancellable": True,
    }
def cancel_booking(booking_id: str) -> dict:
    refund_info = calculate_refund(booking_id)
    booking = db.BOOKINGS[booking_id]
    trip    = db.TRIPS[booking.trip_id]
    seat_map = db.SEAT_MAPS.get(booking.trip_id)
    # Remove segment bookings for these seats
    if seat_map:
        for seat in booking.seat_numbers:
            seat_map.bookings.pop(seat, None)
    # Update booking
    booking.status = BookingStatus.CANCELLED
    booking.cancellation_time = datetime.now()
    booking.refund_amount = refund_info["refund_amount"]
    # Credit wallet
    user = db.USERS.get(booking.user_id)
    if user and refund_info["refund_amount"] > 0:
        user.wallet_balance += refund_info["refund_amount"]
    # Update payment status
    for payment in db.PAYMENTS.values():
        if payment.booking_id == booking_id:
            payment.status = "refunded"
            break
    return {**refund_info, "status": "cancelled", "wallet_credited": refund_info["refund_amount"]}