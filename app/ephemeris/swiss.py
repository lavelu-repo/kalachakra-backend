"""Swiss Ephemeris implementation of the ephemeris provider."""

import swisseph as swe
from pathlib import Path
from app.core.config import settings
from app.ephemeris.base import EphemerisProvider, Planet, Position



# Allow switching between Mean and True nodes via settings
RAHU_TYPE = swe.TRUE_NODE if getattr(settings, "USE_TRUE_NODE", True) else swe.MEAN_NODE

# Swiss Ephemeris planet constants
PLANET_MAP = {
    "sun": swe.SUN,
    "moon": swe.MOON,
    "mercury": swe.MERCURY,
    "venus": swe.VENUS,
    "mars": swe.MARS,
    "jupiter": swe.JUPITER,
    "saturn": swe.SATURN,
    "uranus": swe.URANUS,
    "neptune": swe.NEPTUNE,
    "rahu": RAHU_TYPE,
}


class SwissEphemerisProvider(EphemerisProvider):
    """Swiss Ephemeris implementation with ~0.001° accuracy."""

    def __init__(self, ephemeris_path: str | None = None) -> None:
        """
        Initialize Swiss Ephemeris provider.

        Args:
            ephemeris_path: Path to Swiss Ephemeris data files.
                          If None, uses settings.EPHEMERIS_PATH
        """
        self.ephemeris_path = ephemeris_path or settings.EPHEMERIS_PATH

        # Set ephemeris path if it exists
        path = Path(self.ephemeris_path)
        if path.exists() and path.is_dir():
            swe.set_ephe_path(str(path.absolute()))
            print(f"Ephemeris path set to: {path.absolute()}")

        # Configure sidereal mode once if needed
        if getattr(settings, "ZODIAC_TYPE", "tropical").lower() == "sidereal":
            ayan_setting = getattr(settings, "AYANAMSA", "LAHIRI")

            AYAN_MAP = {
                "LAHIRI": swe.SIDM_LAHIRI,
                "RAMAN": swe.SIDM_RAMAN,
                "KRISHNAMURTI": swe.SIDM_KRISHNAMURTI,
                "FAGAN_BRADLEY": swe.SIDM_FAGAN_BRADLEY,
            }

            ayan = AYAN_MAP.get(str(ayan_setting).upper(), swe.SIDM_LAHIRI)
            swe.set_sid_mode(ayan, 0, 0)
            print(f"Sidereal mode configured with Ayanamsa: {ayan_setting} -> {ayan}")




    def get_planet_position(
        self, planet: Planet, jd: float, geocentric: bool = True
    ) -> Position:
        """Get planetary position using Swiss Ephemeris."""
        
        if planet not in PLANET_MAP:
            raise ValueError(f"Unknown planet: {planet}")
        
        base_flags = swe.FLG_SWIEPH | swe.FLG_SPEED

        if getattr(settings, "ZODIAC_TYPE", "tropical") == "sidereal":
            base_flags |= swe.FLG_SIDEREAL
        
        if not geocentric:
            base_flags |= swe.FLG_HELCTR

        planet_code = PLANET_MAP[planet]

        # GET ECLIPTIC POSITION (Longitude, Latitude, Distance, Speed)
        res_ecl, ret_flag = swe.calc_ut(jd, planet_code, base_flags)
        if ret_flag < 0:
            raise RuntimeError(f"Swiss Ephemeris error: {ret_flag}")

        # GET EQUATORIAL POSITION (Right Ascension, Declination)
        # We call it again with the Equatorial flag to let the library handle the math
        res_eq, _ = swe.calc_ut(jd, planet_code, base_flags | swe.FLG_EQUATORIAL)

        return Position(
            longitude=res_ecl[0],
            latitude=res_ecl[1],
            distance=res_ecl[2],
            longitude_speed=res_ecl[3],
            right_ascension=res_eq[0],
            declination=res_eq[1]
        )

    def get_lunar_nodes(self, jd: float) -> tuple[Position, Position]:
        """Get Rahu (north node) and Ketu (south node) positions."""
        # Get Rahu (north node) position
        rahu_pos = self.get_planet_position("rahu", jd, geocentric=True)

        # Ketu is always 180° opposite to Rahu
        ketu_longitude = (rahu_pos.longitude + 180.0) % 360.0
        ketu_speed = rahu_pos.longitude_speed

        ketu_pos = Position(
            longitude=ketu_longitude,
            latitude=-rahu_pos.latitude,
            distance=rahu_pos.distance,
            longitude_speed=rahu_pos.longitude_speed,
            right_ascension=(rahu_pos.right_ascension + 180.0) % 360.0 if rahu_pos.right_ascension else None,
            declination=-rahu_pos.declination if rahu_pos.declination else None
        )

        return (rahu_pos, ketu_pos)

    def is_retrograde(self, planet: Planet, jd: float) -> bool:
        """Check if planet is retrograde (negative longitude speed)."""
        # Rahu/Ketu can move direct if using 'True Node', otherwise Mean is always retrograde
        if planet in ("sun", "moon", "rahu", "ketu"):
            # Sun, Moon, and lunar nodes don't go retrograde
            return False

        position = self.get_planet_position(planet, jd)
        # In Western astrology, Mean Node speed is negative, but usually not called "retrograde"
        return position.longitude_speed < 0

    def get_supported_date_range(self) -> tuple[float, float]:
        """
        Get supported date range for Swiss Ephemeris.

        Returns:
            Tuple of (min_jd, max_jd)
            Approximately 2999 BCE to 3000 CE
        """
        # Swiss Ephemeris supports roughly -3000 to +3000
        # JD 625673.5 = 1800-01-01, JD 2525593.5 = 2200-01-01
        # Using conservative range for accuracy
        return (625673.5, 2525593.5)  # 1800 CE to 2200 CE

    def close(self) -> None:
        """Close Swiss Ephemeris and free resources."""
        swe.close()

# Global provider instance
_provider: SwissEphemerisProvider | None = None

def get_ephemeris_provider() -> SwissEphemerisProvider:
    """Get or create the global ephemeris provider instance."""
    global _provider
    if _provider is None:
        _provider = SwissEphemerisProvider()
    return _provider