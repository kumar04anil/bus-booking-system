# 🚌 Bus Booking System - Python Backend + React Frontend

A full-stack bus booking application with a **FastAPI backend** and **React (Vite) frontend**.

## Architecture

```
bus_booking/
├── Backend (FastAPI)
│   ├── main.py              - FastAPI app entry point
│   ├── models.py            - Pydantic schemas
│   ├── moc_data.py         - Mock in-memory database
│   ├── routers/
│   │   ├── search.py       - Bus search API
│   │   ├── booking.py      - Booking management API
│   │   ├── auth.py         - (Future) Authentication
│   │   └── admin.py        - (Future) Admin endpoints
│   ├── services/
│   │   ├── seat_service.py - Seat availability & locking
│   │   ├── lock_service.py - 10-min seat lock timer
│   │   ├── pnr_service.py  - PNR generation & booking
│   │   └── cancellation.py - Refund calculations
│   └── requirements.txt    - Python dependencies
│
└── Frontend (React + Vite)
    ├── index.html          - Vite entry point
    ├── package.json        - Node dependencies
    ├── vite.config.js      - Vite configuration
    └── src/
        ├── main.jsx        - React entry point
        ├── App.jsx         - Main app component
        ├── App.css         - Global styles
        ├── index.css       - Base styles
        ├── api/
        │   └── client.js   - Axios API client
        ├── components/
        │   ├── SearchForm.jsx        - Search form
        │   ├── TripResults.jsx       - Bus list
        │   ├── SeatSelection.jsx     - Seat picker
        │   └── BookingConfirmation.jsx - Booking & payment
        └── styles/
            ├── SearchForm.css
            ├── TripResults.css
            ├── SeatSelection.css
            └── BookingConfirmation.css
```

## Quick Start

### Backend Setup

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Run the FastAPI server (port 8000)
python main.py
# OR
uvicorn main:app --reload --port 8000

# 3. View API docs
# Swagger UI:  http://localhost:8000/docs
# ReDoc:       http://localhost:8000/redoc
```

### Frontend Setup

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install Node dependencies
npm install

# 3. Run development server (port 5173)
npm run dev

# 4. For production build
npm run build

# 5. Preview production build
npm run preview
```

### Access the Application

| Component | URL | Notes |
|-----------|-----|-------|
| React Frontend (Dev) | http://localhost:5173 | Hot reload enabled |
| React Frontend (Prod) | http://localhost:8000 | Served by FastAPI after build |
| API Documentation | http://localhost:8000/docs | Swagger UI |
| Backend API | http://localhost:8000/api/ | JSON endpoints |

## API Endpoints

### Search
- `GET /api/search/cities` - List all available cities
- `GET /api/search/trips` - Search buses with filters

### Booking
- `GET /api/booking/seats/{trip_id}` - Get seat map for a trip
- `POST /api/booking/lock` - Lock seats (10-minute expiry)
- `POST /api/booking/release` - Release locked seats
- `POST /api/booking/confirm` - Confirm and create booking
- `GET /api/booking/{booking_id}` - Get booking details
- `GET /api/booking/pnr/{pnr}` - Get booking by PNR
- `POST /api/booking/cancel/{booking_id}` - Cancel booking
- `GET /api/booking/refund/{booking_id}` - Get refund estimate
- `GET /api/booking/user/{user_id}` - Get user's bookings

## Features Implemented

### Backend
✅ Segment-aware seat availability (A→B frees seat for B→C)
✅ 10-minute seat locking with countdown timer
✅ Max 6 seats per transaction
✅ Cancellation refund matrix (90% / 50% / 0%)
✅ Dual-deck sleeper grid (L/U + aisle)
✅ Chair car 3+2 grid with row labels
✅ Dynamic fare calculation (base + GST + convenience fee)
✅ PNR generation + booking confirmation
✅ Mock payment (UPI/Card/Net Banking)

### Frontend
✅ Responsive mobile-first design
✅ Real-time search with filters
✅ Interactive seat selection
✅ Passenger details form
✅ Fare breakdown display
✅ Booking confirmation with PNR
✅ Red + White + Dark Blue theme
✅ Smooth animations & transitions
✅ Error handling & loading states

## Technology Stack

### Backend
- **Framework:** FastAPI 0.111.0
- **Server:** Uvicorn 0.30.1
- **Validation:** Pydantic 2.7.1
- **Python:** 3.8+

### Frontend
- **Framework:** React 18.2.0
- **Build Tool:** Vite 4.4.0
- **HTTP Client:** Axios 1.6.0
- **Node:** 14+

## Development Workflow

### Start Backend
```bash
python main.py
```

### Start Frontend (in another terminal)
```bash
cd frontend && npm run dev
```

### Make API Changes
- Modify `routers/*.py` or `services/*.py`
- Backend auto-reloads (if running with `--reload`)
- No frontend restart needed (API proxy handles it)

### Make Frontend Changes
- Modify `frontend/src/**/*.jsx`
- Frontend auto-reloads (Vite HMR)
- Changes visible immediately

## Production Deployment

### Build Frontend
```bash
cd frontend
npm run build
# Creates: frontend/dist/
```

### Run Production Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
# Serves React app from frontend/dist/
# Serves API from /api/
```

## Mock Data

The system includes pre-configured mock data:

### Users
- `u1`: Arjun Mehta (male, ₹500 wallet)
- `u2`: Priya Sharma (female, ₹200 wallet)

### Routes
- Mumbai → Bangalore via Pune
- Delhi → Jaipur via Agra

### Buses
- `b1`: Royal Cruiser (Sleeper, AC)
- `b2`: Express Rider (Chair Car, AC)
- `b3`: Night Express (Sleeper, Non-AC)

### Trips
- Trip T1: 6/10/2026, 20:00 IST (Mumbai → Bangalore)
- Trip T2: 6/10/2026, 06:00 IST (Delhi → Jaipur)
- Trip T3: 6/11/2026, 21:00 IST (Mumbai → Bangalore)

## Testing

### Test Backend API
```bash
# Use Swagger UI
http://localhost:8000/docs

# Or test with curl
curl -X GET "http://localhost:8000/api/search/cities"
curl -X GET "http://localhost:8000/api/search/trips?source=Mumbai&destination=Bangalore&journey_date=2026-06-10"
```

### Test Frontend
1. Open http://localhost:5173
2. Search for a trip (Mumbai → Bangalore, 6/10/2026)
3. Select a bus
4. Choose seats
5. Fill passenger details
6. Confirm booking

## Common Issues

### CORS Error
- Ensure backend is running on port 8000
- Check `allow_origins` in `main.py`

### Vite Port Already in Use
```bash
npm run dev -- --port 3000  # Use different port
```

### Module Not Found
```bash
npm install  # Reinstall node modules
pip install -r requirements.txt  # Reinstall Python packages
```

## Future Enhancements

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User authentication & JWT tokens
- [ ] Payment gateway integration
- [ ] Real-time notifications
- [ ] Admin dashboard
- [ ] Booking history & cancellations
- [ ] Email confirmations
- [ ] Multi-language support

## License

MIT License

## Support

For issues or questions, please refer to the API documentation at `/docs`
