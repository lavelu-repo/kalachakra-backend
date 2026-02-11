"""Planetary position endpoints."""

from fastapi import APIRouter, HTTPException

from app.core.time_utils import datetime_to_julian_day
from app.ephemeris.swiss import get_ephemeris_provider
from app.schemas.positions import (
    MultiPositionRequest,
    MultiPositionResponse,
    PositionResponse,
)

router = APIRouter()


@router.post("/positions", response_model=MultiPositionResponse)
async def get_positions(request: MultiPositionRequest) -> MultiPositionResponse:
    """
    Get planetary positions for multiple planets at a given date/time.

    Args:
        request: Request containing date and list of planets

    Returns:
        Planetary positions with astronomical coordinates

    Raises:
        HTTPException: If calculation fails or date is out of range
    """
    try:
        # Convert datetime to Julian Day
        jd = datetime_to_julian_day(request.date)

        # Validate date range
        provider = get_ephemeris_provider()
        min_jd, max_jd = provider.get_supported_date_range()

        if not (min_jd <= jd <= max_jd):
            raise HTTPException(
                status_code=400,
                detail=f"Date out of supported range (1800-2200 CE). Julian Day {jd} not in [{min_jd}, {max_jd}]",
            )

        # Calculate positions for each planet
        positions = []
        for planet in request.planets:
            # Special handling for Rahu/Ketu
            if planet == "rahu":
                rahu_pos, _ = provider.get_lunar_nodes(jd)
                position = rahu_pos
            elif planet == "ketu":
                _, ketu_pos = provider.get_lunar_nodes(jd)
                position = ketu_pos
            else:
                position = provider.get_planet_position(
                    planet, jd, geocentric=request.geocentric
                )

            is_retrograde = provider.is_retrograde(planet, jd)

            positions.append(
                PositionResponse(
                    planet=planet,
                    longitude=position.longitude,
                    latitude=position.latitude,
                    distance=position.distance,
                    right_ascension=position.right_ascension,
                    declination=position.declination,
                    speed=position.longitude_speed,
                    is_retrograde=is_retrograde,
                )
            )

        return MultiPositionResponse(
            date=request.date,
            julian_day=jd,
            positions=positions,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")
