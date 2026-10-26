"""
FastAPI Weather-Aware Construction Protocols Route.
"""

from fastapi import APIRouter
from modules.config import WEATHER_CONDITIONS

router = APIRouter(prefix="/api/weather", tags=["Daily Weather Advisory"])


@router.get("/advisories")
async def get_weather_advisories():
    """Returns dynamic safety rules, crane protocols, and concreting directives by weather condition."""
    return WEATHER_CONDITIONS
