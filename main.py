# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
import os
from routers import search, booking

app = FastAPI(
    title="Bus Booking System",
    description="Enterprise Bus Booking API with segment-aware seat management",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(search.router)
app.include_router(booking.router)

# Serve React static files (production build)
frontend_build = Path("frontend/dist")
if frontend_build.exists():
    app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")

# Serve React app for all other routes
@app.get("/{full_path:path}")
async def serve_react(full_path: str):
    # If it's an API route, let it pass through
    if full_path.startswith("api/"):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    # Serve React index.html
    index_path = Path("frontend/dist/index.html")
    if index_path.exists():
        return FileResponse(index_path)
    
    # If dist doesn't exist, return a helpful message
    return {
        "message": "React frontend not built. Run 'cd frontend && npm run build' to build production bundle.",
        "dev_server": "For development, run 'cd frontend && npm run dev' (runs on http://localhost:5173)"
    }

# Root endpoint
@app.get("/")
async def root():
    index_path = Path("frontend/dist/index.html")
    if index_path.exists():
        return FileResponse(index_path)
    return {
        "message": "Bus Booking System API",
        "docs": "http://localhost:8000/docs",
        "dev_frontend": "http://localhost:5173",
        "build_frontend": "cd frontend && npm run build"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)