# routers/search.py
from fastapi import APIRouter, Query, HTTPException
from datetime import date
from typing import Optional
from models import BusType, ACType, SearchRequest
import moc_data as db
router = APIRouter(prefix="/api/search", tags=["Search"])
@router.get("/cities")
def get_all_cities():
    cities = set()
    for route in db.ROUTES.values():
        for stop in route.stops:
            cities.add(stop.city)
    return sorted(list(cities))
@router.get("/trips")
def search_trips(
    source: str = Query(...),
    destination: str = Query(...),
    journey_date: date = Query(...),
    passenger_count: int = Query(1, ge=1, le=6),
    bus_type: Optional[BusType] = Query(None),
    ac_type: Optional[ACType] = Query(None),
    journey_window: Optional[str] = Query(None),  # "day" or "night"
):
    results = []
    for trip in db.TRIPS.values():
        if trip.journey_date != journey_date:
            continue
        if trip.status == "cancelled":
            continue
        route = db.ROUTES.get(trip.route_id)
        if not route:
            continue
        # Check source and destination exist in route (in correct order)
        stop_cities = [s.city.lower() for s in route.stops]
        src_lower   = source.lower()
        dst_lower   = destination.lower()
        if src_lower not in stop_cities or dst_lower not in stop_cities:
            continue
        src_order = next(s.stop_order for s in route.stops if s.city.lower() == src_lower)
        dst_order = next(s.stop_order for s in route.stops if s.city.lower() == dst_lower)
        if src_order >= dst_order:
            continue
        bus = db.BUSES.get(trip.bus_id)
        if not bus or bus.status != "active":
            continue
        # Apply filters
        if bus_type and bus.bus_type != bus_type:
            continue
        if ac_type and bus.ac_type != ac_type:
            continue
        if journey_window == "day" and trip.is_night_journey:
            continue
        if journey_window == "night" and not trip.is_night_journey:
            continue
        # Count available seats for this segment
        from services.seat_service import generate_seat_grid, prune_expired_locks
        prune_expired_locks(trip.id)
        grid = generate_seat_grid(trip.id, source, destination)
        all_seats = []
        for deck_seats in grid["decks"].values():
            all_seats.extend(deck_seats)
        available_count = sum(1 for s in all_seats if s["status"] in ("available", "female_reserved"))
        if available_count < passenger_count:
            continue
        driver = db.DRIVERS.get(trip.driver_id)
        # Fare calculation
        base_total      = trip.base_fare
        gst_amount      = round(base_total * trip.gst_rate, 2)
        total_fare      = round(base_total + gst_amount + trip.convenience_fee, 2)
        results.append({
            "trip_id": trip.id,
            "journey_date": str(trip.journey_date),
            "departure_time": trip.departure_time,
            "arrival_time": trip.arrival_time,
            "is_night_journey": trip.is_night_journey,
            "bus": {
                "id": bus.id,
                "name": bus.name,
                "number": bus.number,
                "type": bus.bus_type.value,
                "ac_type": bus.ac_type.value,
                "amenities": bus.amenities,
                "total_seats": bus.seat_config.total_seats,
            },
            "route": {
                "id": route.id,
                "name": route.name,
                "source": source,
                "destination": destination,
                "stops": [
                    {"city": s.city, "arrival": s.arrival_time,
                     "departure": s.departure_time, "order": s.stop_order}
                    for s in route.stops
                ],
            },
            "driver": {
                "name": driver.name if driver else "N/A",
                "experience_years": driver.experience_years if driver else 0,
                "rating": driver.rating if driver else 0,
            } if driver else None,
            "fare": {
                "base_fare": trip.base_fare,
                "gst": gst_amount,
                "convenience_fee": trip.convenience_fee,
                "total": total_fare,
            },
            "availability": {
                "available_seats": available_count,
                "total_seats": bus.seat_config.total_seats,
            },
        })
    return {"results": results, "count": len(results)}