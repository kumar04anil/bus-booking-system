# models.py
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List, Literal
from datetime import datetime, date
from enum import Enum
import uuid
# ─────────────────────────────────────────────
# Enums
# ─────────────────────────────────────────────
class BusType(str, Enum):
    SLEEPER = "sleeper"
    CHAIR = "chair"
class ACType(str, Enum):
    AC = "AC"
    NON_AC = "Non-AC"
class SeatStatus(str, Enum):
    AVAILABLE = "available"
    BOOKED = "booked"
    LOCKED = "locked"
    FEMALE_RESERVED = "female_reserved"
    SELECTED = "selected"
class BusStatus(str, Enum):
    ACTIVE = "active"
    IN_SERVICE = "in_service"
    MAINTENANCE = "maintenance"
    SUSPENDED = "suspended"
class PaymentMethod(str, Enum):
    UPI = "UPI"
    CARD = "Card"
    NET_BANKING = "Net Banking"
class PaymentStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"
class BookingStatus(str, Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    PENDING = "pending"
class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
# ─────────────────────────────────────────────
# User
# ─────────────────────────────────────────────
class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    gender: Optional[Gender] = None
class UserCreate(UserBase):
    password: str
class User(UserBase):
    id: str
    wallet_balance: float = 0.0
    created_at: datetime = datetime.now()
    is_active: bool = True
    class Config:
        from_attributes = True
# ─────────────────────────────────────────────
# Route Stop
# ─────────────────────────────────────────────
class RouteStop(BaseModel):
    city: str
    arrival_time: Optional[str] = None    # "HH:MM"
    departure_time: Optional[str] = None  # "HH:MM"
    stop_order: int
    distance_from_origin_km: float = 0.0
class Route(BaseModel):
    id: str
    name: str
    source: str
    destination: str
    stops: List[RouteStop]
    total_km: float
    is_active: bool = True
# ─────────────────────────────────────────────
# Bus
# ─────────────────────────────────────────────
class SeatConfig(BaseModel):
    total_seats: int
    lower_seats: int = 0      # For sleeper
    upper_seats: int = 0      # For sleeper
    seats_per_row: int = 3    # For chair (3+2 = 5)
    female_reserved_seats: List[str] = []
class Bus(BaseModel):
    id: str
    number: str
    name: str
    bus_type: BusType
    ac_type: ACType
    amenities: List[str] = []
    seat_config: SeatConfig
    status: BusStatus = BusStatus.ACTIVE
    total_km_driven: float = 0.0
# ─────────────────────────────────────────────
# Driver
# ─────────────────────────────────────────────
class Driver(BaseModel):
    id: str
    name: str
    license_number: str
    experience_years: int
    rating: float
    total_km_driven: float
    is_license_verified: bool
    is_available: bool = True
    shift_status: Literal["on_shift", "off_shift", "on_leave"] = "off_shift"
# ─────────────────────────────────────────────
# Trip / Schedule  ← KEY ENTITY
# ─────────────────────────────────────────────
class Trip(BaseModel):
    id: str
    bus_id: str
    route_id: str
    driver_id: str
    journey_date: date
    departure_time: str   # "HH:MM" from source
    arrival_time: str     # "HH:MM" at destination
    base_fare: float
    gst_rate: float = 0.18
    convenience_fee: float = 50.0
    is_night_journey: bool = False
    status: Literal["scheduled", "in_progress", "completed", "cancelled"] = "scheduled"
# ─────────────────────────────────────────────
# Seat Availability (Segment-aware)
# ─────────────────────────────────────────────
class SeatSegmentBooking(BaseModel):
    seat_number: str
    booked_from_stop: str
    booked_to_stop: str
    passenger_gender: Optional[Gender] = None
class TripSeatMap(BaseModel):
    trip_id: str
    # seat_number -> list of segment bookings
    bookings: dict[str, List[SeatSegmentBooking]] = {}
    # seat_number -> lock expiry timestamp (epoch)
    locks: dict[str, float] = {}
# ─────────────────────────────────────────────
# Passenger
# ─────────────────────────────────────────────
class Passenger(BaseModel):
    name: str
    age: int
    gender: Gender
    contact: str
    seat_number: str
    special_requests: Optional[str] = None
# ─────────────────────────────────────────────
# Booking
# ─────────────────────────────────────────────
class BookingCreate(BaseModel):
    trip_id: str
    user_id: str
    from_stop: str
    to_stop: str
    passengers: List[Passenger]
    payment_method: PaymentMethod
class Booking(BaseModel):
    id: str
    pnr: str
    trip_id: str
    user_id: str
    from_stop: str
    to_stop: str
    passengers: List[Passenger]
    seat_numbers: List[str]
    status: BookingStatus = BookingStatus.CONFIRMED
    total_amount: float
    payment_id: Optional[str] = None
    booked_at: datetime = datetime.now()
    cancellation_time: Optional[datetime] = None
    refund_amount: Optional[float] = None
# ─────────────────────────────────────────────
# Payment
# ─────────────────────────────────────────────
class Payment(BaseModel):
    id: str
    booking_id: str
    amount: float
    method: PaymentMethod
    status: PaymentStatus = PaymentStatus.PENDING
    transaction_id: Optional[str] = None
    created_at: datetime = datetime.now()
# ─────────────────────────────────────────────
# Search Request
# ─────────────────────────────────────────────
class SearchRequest(BaseModel):
    source: str
    destination: str
    journey_date: date
    passenger_count: int = 1
    bus_type: Optional[BusType] = None
    ac_type: Optional[ACType] = None
    journey_window: Optional[Literal["day", "night"]] = None