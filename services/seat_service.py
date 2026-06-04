# services/seat_service.py
"""
Segment-based seat availability engine.
A seat booked from A->B remains AVAILABLE for B->C on the same trip.
"""
import time
from typing import List, Dict, Tuple
from models import (
    SeatStatus, TripSeatMap, Bus, Route, RouteStop,
    BusType, Gender
)
import moc_data as db
LOCK_DURATION_SECONDS = 600  # 10 minutes
def _get_stop_order(route: Route, city: str) -> int:
    for stop in route.stops:
        if stop.city.lower() == city.lower():
            return stop.stop_order
    raise ValueError(f"City '{city}' not found in route.")
def _segments_overlap(
    booked_from_order: int, booked_to_order: int,
    query_from_order: int, query_to_order: int
) -> bool:
    """
    Two segments overlap if they share any leg of the journey.
    Overlap condition: NOT (booked_to <= query_from OR booked_from >= query_to)
    """
    return not (booked_to_order <= query_from_order or booked_from_order >= query_to_order)
def get_seat_status(
    seat_number: str,
    trip_seat_map: TripSeatMap,
    bus: Bus,
    route: Route,
    query_from: str,
    query_to: str
) -> SeatStatus:
    """
    Determine live seat status for a specific travel segment.
    """
    now = time.time()
    # 1. Check lock (non-segment-specific — lock blocks globally)
    lock_expiry = trip_seat_map.locks.get(seat_number, 0)
    if lock_expiry > now:
        return SeatStatus.LOCKED
    # 2. Check segment overlap with existing bookings
    query_from_order = _get_stop_order(route, query_from)
    query_to_order   = _get_stop_order(route, query_to)
    bookings_for_seat = trip_seat_map.bookings.get(seat_number, [])
    for seg_booking in bookings_for_seat:
        b_from = _get_stop_order(route, seg_booking.booked_from_stop)
        b_to   = _get_stop_order(route, seg_booking.booked_to_stop)
        if _segments_overlap(b_from, b_to, query_from_order, query_to_order):
            # Check female-reserved
            if seat_number in bus.seat_config.female_reserved_seats:
                return SeatStatus.FEMALE_RESERVED
            return SeatStatus.BOOKED
    # 3. Female reserved (but currently available for this segment)
    if seat_number in bus.seat_config.female_reserved_seats:
        return SeatStatus.FEMALE_RESERVED  # Still shown as pink but selectable
    return SeatStatus.AVAILABLE
def generate_seat_grid(
    trip_id: str,
    from_stop: str,
    to_stop: str
) -> Dict:
    """
    Returns the full seat grid with status for a trip segment.
    Supports both Sleeper (dual-deck) and Chair Car (3+2 layout).
    """
    trip = db.TRIPS.get(trip_id)
    if not trip:
        raise ValueError(f"Trip {trip_id} not found")
    bus    = db.BUSES[trip.bus_id]
    route  = db.ROUTES[trip.route_id]
    seat_map = db.SEAT_MAPS.get(trip_id, TripSeatMap(trip_id=trip_id))
    grid = {"bus_type": bus.bus_type, "decks": {}}
    if bus.bus_type == BusType.SLEEPER:
        # Generate Lower (L1-L20) and Upper (U1-U20) deck
        for deck_prefix, count in [("L", bus.seat_config.lower_seats),
                                    ("U", bus.seat_config.upper_seats)]:
            deck_key = "lower" if deck_prefix == "L" else "upper"
            deck_seats = []
            for i in range(1, count + 1):
                seat_num = f"{deck_prefix}{i}"
                status = get_seat_status(
                    seat_num, seat_map, bus, route, from_stop, to_stop
                )
                deck_seats.append({
                    "seat_number": seat_num,
                    "status": status.value,
                    "deck": deck_key,
                    "row": (i - 1) // 4 + 1,
                    "col": (i - 1) % 4 + 1,
                })
            grid["decks"][deck_key] = deck_seats
    else:  # CHAIR CAR — 3+2 layout
        seats = []
        rows = bus.seat_config.total_seats // bus.seat_config.seats_per_row
        cols_left  = ["A", "B", "C"]   # 3-seat side
        cols_right = ["D", "E"]        # 2-seat side
        row_num = 1
        for r in range(1, rows + 1):
            for c in cols_left + cols_right:
                seat_num = f"{r}{c}"
                status = get_seat_status(
                    seat_num, seat_map, bus, route, from_stop, to_stop
                )
                seats.append({
                    "seat_number": seat_num,
                    "status": status.value,
                    "row": r,
                    "col": c,
                    "side": "left" if c in cols_left else "right",
                })
        grid["decks"]["main"] = seats
    return grid
# ─── Locking ──────────────────────────────────────────────────────────────────
def lock_seats(trip_id: str, seat_numbers: List[str]) -> bool:
    """Lock up to 6 seats for 10 minutes."""
    if len(seat_numbers) > 6:
        raise ValueError("Cannot select more than 6 seats per transaction.")
    seat_map = db.SEAT_MAPS.setdefault(
        trip_id, TripSeatMap(trip_id=trip_id)
    )
    expiry = time.time() + LOCK_DURATION_SECONDS
    for seat in seat_numbers:
        seat_map.locks[seat] = expiry
    return True
def release_locks(trip_id: str, seat_numbers: List[str]) -> None:
    seat_map = db.SEAT_MAPS.get(trip_id)
    if seat_map:
        for seat in seat_numbers:
            seat_map.locks.pop(seat, None)
def prune_expired_locks(trip_id: str) -> None:
    """Call periodically or before each seat map generation."""
    seat_map = db.SEAT_MAPS.get(trip_id)
    if not seat_map:
        return
    now = time.time()
    expired = [s for s, exp in seat_map.locks.items() if exp <= now]
    for s in expired:
        del seat_map.locks[s]