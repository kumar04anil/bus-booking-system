# mock_data.py
"""
In-memory mock data store — replaces a real database.
All mutations happen on these dicts; wire to a real DB later.
"""
from datetime import date
from models import (
    User, Bus, Route, Driver, Trip, Booking, Payment,
    BusType, ACType, BusStatus, SeatConfig, RouteStop, TripSeatMap,
    Gender, BookingStatus, PaymentStatus
)
# ─── Users ────────────────────────────────────────────────────────────────────
USERS: dict[str, User] = {
    "u1": User(
        id="u1", name="Arjun Mehta", email="arjun@example.com",
        phone="9876543210", gender=Gender.MALE, wallet_balance=500.0
    ),
    "u2": User(
        id="u2", name="Priya Sharma", email="priya@example.com",
        phone="9123456789", gender=Gender.FEMALE, wallet_balance=200.0
    ),
}
# Plain-text passwords (mock only — hash in production)
USER_PASSWORDS: dict[str, str] = {
    "arjun@example.com": "pass123",
    "priya@example.com": "pass456",
}
# ─── Drivers ──────────────────────────────────────────────────────────────────
from models import Driver
DRIVERS: dict[str, Driver] = {
    "d1": Driver(
        id="d1", name="Ramesh Kumar", license_number="MH12-20180045",
        experience_years=12, rating=4.7, total_km_driven=180000,
        is_license_verified=True, is_available=True, shift_status="on_shift"
    ),
    "d2": Driver(
        id="d2", name="Suresh Patil", license_number="KA09-20150033",
        experience_years=8, rating=4.3, total_km_driven=95000,
        is_license_verified=True, is_available=True, shift_status="on_shift"
    ),
}
# ─── Buses ────────────────────────────────────────────────────────────────────
BUSES: dict[str, Bus] = {
    "b1": Bus(
        id="b1", number="MH12-AB-1234", name="Royal Cruiser",
        bus_type=BusType.SLEEPER, ac_type=ACType.AC,
        amenities=["WiFi", "USB Charging", "Blanket", "Water Bottle"],
        seat_config=SeatConfig(
            total_seats=40, lower_seats=20, upper_seats=20,
            female_reserved_seats=["L1", "L2", "U1", "U2"]
        ),
        status=BusStatus.ACTIVE
    ),
    "b2": Bus(
        id="b2", number="KA09-CD-5678", name="Express Rider",
        bus_type=BusType.CHAIR, ac_type=ACType.AC,
        amenities=["WiFi", "USB Charging", "Snacks"],
        seat_config=SeatConfig(
            total_seats=45, seats_per_row=5,
            female_reserved_seats=["1A", "1B", "2A", "2B"]
        ),
        status=BusStatus.ACTIVE
    ),
    "b3": Bus(
        id="b3", number="TN07-EF-9012", name="Night Express",
        bus_type=BusType.SLEEPER, ac_type=ACType.NON_AC,
        amenities=["Blanket", "Water Bottle"],
        seat_config=SeatConfig(
            total_seats=36, lower_seats=18, upper_seats=18,
            female_reserved_seats=["L1", "L2", "U1"]
        ),
        status=BusStatus.ACTIVE
    ),
}
# ─── Routes ───────────────────────────────────────────────────────────────────
ROUTES: dict[str, Route] = {
    "r1": Route(
        id="r1", name="Mumbai - Pune - Bangalore",
        source="Mumbai", destination="Bangalore",
        stops=[
            RouteStop(city="Mumbai", departure_time="20:00", stop_order=0, distance_from_origin_km=0),
            RouteStop(city="Pune", arrival_time="22:30", departure_time="22:45", stop_order=1, distance_from_origin_km=150),
            RouteStop(city="Bangalore", arrival_time="08:00", stop_order=2, distance_from_origin_km=980),
        ],
        total_km=980
    ),
    "r2": Route(
        id="r2", name="Delhi - Agra - Jaipur",
        source="Delhi", destination="Jaipur",
        stops=[
            RouteStop(city="Delhi", departure_time="06:00", stop_order=0, distance_from_origin_km=0),
            RouteStop(city="Agra", arrival_time="08:30", departure_time="08:45", stop_order=1, distance_from_origin_km=200),
            RouteStop(city="Jaipur", arrival_time="12:00", stop_order=2, distance_from_origin_km=550),
        ],
        total_km=550
    ),
}
# ─── Trips ────────────────────────────────────────────────────────────────────
TRIPS: dict[str, Trip] = {
    "t1": Trip(
        id="t1", bus_id="b1", route_id="r1", driver_id="d1",
        journey_date=date(2026, 6, 10),
        departure_time="20:00", arrival_time="08:00",
        base_fare=1200.0, is_night_journey=True
    ),
    "t2": Trip(
        id="t2", bus_id="b2", route_id="r2", driver_id="d2",
        journey_date=date(2026, 6, 10),
        departure_time="06:00", arrival_time="12:00",
        base_fare=800.0, is_night_journey=False
    ),
    "t3": Trip(
        id="t3", bus_id="b3", route_id="r1", driver_id="d1",
        journey_date=date(2026, 6, 11),
        departure_time="21:00", arrival_time="09:30",
        base_fare=900.0, is_night_journey=True
    ),
}
# ─── Seat Maps ────────────────────────────────────────────────────────────────
# Pre-book a few seats to demo segment availability
from models import SeatSegmentBooking
SEAT_MAPS: dict[str, TripSeatMap] = {
    "t1": TripSeatMap(
        trip_id="t1",
        bookings={
            "L3": [SeatSegmentBooking(seat_number="L3", booked_from_stop="Mumbai",
                                      booked_to_stop="Pune", passenger_gender=Gender.MALE)],
            "U5": [SeatSegmentBooking(seat_number="U5", booked_from_stop="Mumbai",
                                      booked_to_stop="Bangalore", passenger_gender=Gender.MALE)],
            "L7": [SeatSegmentBooking(seat_number="L7", booked_from_stop="Pune",
                                      booked_to_stop="Bangalore", passenger_gender=Gender.FEMALE)],
        }
    ),
    "t2": TripSeatMap(
        trip_id="t2",
        bookings={
            "3A": [SeatSegmentBooking(seat_number="3A", booked_from_stop="Delhi",
                                      booked_to_stop="Jaipur", passenger_gender=Gender.MALE)],
            "5C": [SeatSegmentBooking(seat_number="5C", booked_from_stop="Delhi",
                                      booked_to_stop="Agra", passenger_gender=Gender.FEMALE)],
        }
    ),
    "t3": TripSeatMap(trip_id="t3", bookings={}),
}
# ─── Bookings & Payments ──────────────────────────────────────────────────────
BOOKINGS: dict[str, Booking] = {}
PAYMENTS: dict[str, Payment] = {}