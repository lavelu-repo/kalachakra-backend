from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


Planet = Literal[
    "sun",
    "moon",
    "mercury",
    "venus",
    "mars",
    "jupiter",
    "saturn",
    "uranus",
    "neptune",
    "rahu",
    "ketu",
]


class PositionResponse(BaseModel):
    """Planetary position response."""

    planet: Planet
    longitude: float = Field(..., ge=0, lt=360, description="Ecliptic longitude in degrees")
    latitude: float = Field(..., ge=-90, le=90, description="Ecliptic latitude in degrees")
    distance: float = Field(..., gt=0, description="Distance in AU")
    right_ascension: float | None = Field(None, ge=0, lt=360, description="Right ascension in degrees")
    declination: float | None = Field(None, ge=-90, le=90, description="Declination in degrees")
    speed: float | None = Field(None, description="Longitude speed in degrees/day")
    is_retrograde: bool = Field(..., description="Whether planet is in retrograde motion")


class MultiPositionRequest(BaseModel):
    """Request for multiple planetary positions."""

    date: datetime = Field(..., description="UTC datetime for calculation")
    planets: list[Planet] = Field(..., min_length=1, description="List of planets to calculate")
    geocentric: bool = Field(True, description="Use geocentric (True) or heliocentric (False) coordinates")


class MultiPositionResponse(BaseModel):
    """Response with multiple planetary positions."""

    date: datetime
    julian_day: float
    positions: list[PositionResponse]
