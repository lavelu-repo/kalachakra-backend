"""Abstract base class for ephemeris providers (Strategy pattern)."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal


@dataclass
class Position:
    """Celestial body position."""

    # Ecliptic coordinates
    longitude: float  # degrees (0-360)
    latitude: float  # degrees (-90 to +90)
    distance: float  # AU (astronomical units)

    # Equatorial coordinates (optional)
    right_ascension: float | None = None  # degrees (0-360)
    declination: float | None = None  # degrees (-90 to +90)

    # Velocity
    longitude_speed: float | None = None  # degrees/day


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
    "rahu",  # North lunar node
    "ketu",  # South lunar node
]


class EphemerisProvider(ABC):
    """
    Abstract base class for ephemeris calculation providers.

    This allows swapping between different ephemeris sources
    (Swiss Ephemeris, JPL HORIZONS, etc.) without changing client code.
    """

    @abstractmethod
    def get_planet_position(
        self, planet: Planet, jd: float, geocentric: bool = True
    ) -> Position:
        """
        Get planetary position at a given Julian Day.

        Args:
            planet: Planet identifier
            jd: Julian Day Number
            geocentric: If True, return geocentric position; else heliocentric

        Returns:
            Position object with coordinates

        Raises:
            ValueError: If planet is invalid or date is out of range
        """
        pass

    @abstractmethod
    def get_lunar_nodes(self, jd: float) -> tuple[Position, Position]:
        """
        Get Rahu (north node) and Ketu (south node) positions.

        Args:
            jd: Julian Day Number

        Returns:
            Tuple of (rahu_position, ketu_position)
        """
        pass

    @abstractmethod
    def is_retrograde(self, planet: Planet, jd: float) -> bool:
        """
        Check if a planet is in retrograde motion.

        Args:
            planet: Planet identifier
            jd: Julian Day Number

        Returns:
            True if planet is retrograde (apparent backward motion)
        """
        pass

    @abstractmethod
    def get_supported_date_range(self) -> tuple[float, float]:
        """
        Get the supported Julian Day range for this provider.

        Returns:
            Tuple of (min_jd, max_jd)
        """
        pass
