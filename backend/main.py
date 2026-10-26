"""
FastAPI Main Application Entry Point
Multimodal Construction Intelligence Platform Backend
"""

import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.routes.safety import router as safety_router
from backend.routes.cracks import router as cracks_router
from backend.routes.planning import router as planning_router
from backend.routes.weather import router as weather_router
from backend.routes.assistant import router as assistant_router
from modules.config import APP_TITLE, APP_SUBTITLE, APP_VERSION

app = FastAPI(
    title=APP_TITLE,
    description=f"{APP_SUBTITLE} — REST API Backend with Strict JSON Data Contracts",
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for React Frontend (Vite runs on port 5173 by default)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(safety_router)
app.include_router(cracks_router)
app.include_router(planning_router)
app.include_router(weather_router)
app.include_router(assistant_router)

# Mount sample_data statically so images can be served to frontend
sample_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sample_data")
if os.path.exists(sample_dir):
    app.mount("/static/samples", StaticFiles(directory=sample_dir), name="samples")


@app.get("/api/health", tags=["System"])
async def health_check():
    """Health check endpoint confirming API status and active environment."""
    return {
        "status": "healthy",
        "service": APP_TITLE,
        "version": APP_VERSION,
        "standards": ["IS 456:2000", "OSHA 1926", "IS 15844", "NBC 2016"],
        "docs_url": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
