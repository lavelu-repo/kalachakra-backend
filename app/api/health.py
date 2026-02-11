from fastapi import APIRouter
from pydantic import BaseModel

from app.ephemeris.swiss import get_ephemeris_provider

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    ephemeris: str
    date_range: dict[str, float]


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns API status and ephemeris configuration.
    """
    provider = get_ephemeris_provider()
    min_jd, max_jd = provider.get_supported_date_range()

    return HealthResponse(
        status="healthy",
        version="0.1.0",
        ephemeris="Swiss Ephemeris",
        date_range={
            "min_julian_day": min_jd,
            "max_julian_day": max_jd,
        },
    )
