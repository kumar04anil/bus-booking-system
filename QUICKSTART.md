# 🚀 Bus Booking App - Quick Start Guide

## Project Converted ✅

Your bus booking app has been converted from **FastAPI + Jinja2 Templates** to **FastAPI Backend + React SPA**.

## Directory Structure

```
bus_booking/
├── main.py                    # FastAPI server (entry point)
├── models.py                  # Pydantic schemas
├── moc_data.py               # Mock database
├── requirements.txt          # Python dependencies
├── README.md                 # Full documentation
├── routers/                  # API endpoints
├── services/                 # Business logic
└── frontend/                 # React app ⭐ NEW
    ├── src/
    │   ├── components/       # React components
    │   ├── styles/          # CSS files
    │   ├── api/             # API client
    │   └── App.jsx          # Main app
    ├── package.json
    └── vite.config.js
```

## Installation & Setup

### Step 1: Install Python Dependencies
```bash
cd /Users/aks/Workspace/python+React/bus_booking
pip3 install -r requirements.txt
# Or use: pip install -r requirements.txt
```

If you encounter permission issues, you can use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Run Backend Server (Terminal 1)
```bash
python main.py
# OR: uvicorn main:app --reload --port 8000
```

✅ Backend running at: http://localhost:8000
✅ API docs at: http://localhost:8000/docs

### Step 3: Install Frontend Dependencies (Terminal 2)
```bash
cd frontend
npm install
```

### Step 4: Run Frontend Dev Server (Terminal 2)
```bash
npm run dev
```

✅ Frontend running at: http://localhost:5173

## Using the App

1. **Open browser:** http://localhost:5173
2. **Search** for buses:
   - From: Mumbai
   - To: Bangalore
   - Date: 2026-06-10
3. **Select** a bus
4. **Choose** seats (click on green seats)
5. **Fill** passenger details
6. **Confirm** booking
7. **Get** PNR confirmation

## API Testing

### Use Swagger UI (Interactive)
Open: http://localhost:8000/docs

### Or use curl:
```bash
# List all cities
curl http://localhost:8000/api/search/cities

# Search buses
curl "http://localhost:8000/api/search/trips?source=Mumbai&destination=Bangalore&journey_date=2026-06-10"

# Get seat map
curl "http://localhost:8000/api/booking/seats/t1?from_stop=Mumbai&to_stop=Bangalore"
```

## Build for Production

### 1. Build React app:
```bash
cd frontend
npm run build
```

### 2. Run backend:
```bash
python main.py
# Frontend will be served from http://localhost:8000
```

## What Changed

### ✅ Improvements Made:
- **Removed** Jinja2 templates (not needed for SPA)
- **Added** React frontend with Vite
- **Created** modular React components
- **Implemented** responsive design (mobile-first)
- **Theme** Red + White + Dark Blue (as specified)
- **Features** All original features maintained + better UX
- **API** All endpoints remain unchanged (fully compatible)

### 📁 File Summary:
- **3 new components:** SearchForm, TripResults, SeatSelection, BookingConfirmation
- **5 CSS files:** Global + component-specific styling
- **1 API client:** Centralized Axios configuration
- **Updated main.py:** Serves React app + FastAPI
- **Frontend build:** Vite-based (fast development & builds)

## Troubleshooting

### Backend won't start?
```bash
# Check if port 8000 is in use
lsof -i :8000
# Or use a different port:
python main.py --port 8001
```

### Frontend build fails?
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### CORS errors?
- Backend already has CORS enabled for localhost:5173
- Check `main.py` line with `allow_origins`

### Need different port?
```bash
# Frontend on different port:
npm run dev -- --port 3000

# Backend on different port:
uvicorn main:app --port 8001
# Update API proxy in frontend/vite.config.js
```

## Next Steps

1. ✅ Test the app (follow "Using the App" section)
2. 📚 Read README.md for detailed documentation
3. 🔧 Check `requirements.txt` for Python packages needed
4. 📦 Check `frontend/package.json` for Node packages
5. 🚀 Deploy to production (build frontend, run backend)

## Key Files to Review

| File | Purpose |
|------|---------|
| `main.py` | Backend server & routing |
| `frontend/src/App.jsx` | Main React component |
| `frontend/src/api/client.js` | API communication |
| `routers/search.py` | Bus search endpoints |
| `routers/booking.py` | Booking endpoints |
| `models.py` | Data schemas |

## Support

- **API Documentation:** http://localhost:8000/docs
- **README.md:** Full technical documentation
- **Frontend components:** Check code comments in `frontend/src/components/`

---

**Happy booking! 🚌🎉**
