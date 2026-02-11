"""Time conversion utilities for astronomical calculations."""

from datetime import datetime, timezone
from typing import Union


def datetime_to_julian_day(dt: datetime) -> float:
    """
    Convert datetime to Julian Day Number.

    Args:
        dt: Python datetime object (aware or naive, treated as UTC if naive)

    Returns:
        Julian Day Number as float

    Reference:
        Astronomical Algorithms by Jean Meeus
    """
    # Ensure UTC timezone
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)

    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour
    minute = dt.minute
    second = dt.second
    microsecond = dt.microsecond

    # Convert to decimal day
    decimal_day = (
        day + (hour / 24.0) + (minute / 1440.0) +
        (second / 86400.0) + (microsecond / 86400000000.0)
    )

    # Adjust for January and February
    if month <= 2:
        year -= 1
        month += 12

    # Calculate Julian Day
    a = int(year / 100)
    b = 2 - a + int(a / 4)

    jd = (
        int(365.25 * (year + 4716))
        + int(30.6001 * (month + 1))
        + decimal_day
        + b
        - 1524.5
    )

    return jd


def julian_day_to_datetime(jd: float) -> datetime:
    """
    Convert Julian Day Number to datetime.

    Args:
        jd: Julian Day Number

    Returns:
        Python datetime object in UTC timezone
    """
    jd += 0.5
    z = int(jd)
    f = jd - z

    if z < 2299161:
        a = z
    else:
        alpha = int((z - 1867216.25) / 36524.25)
        a = z + 1 + alpha - int(alpha / 4)

    b = a + 1524
    c = int((b - 122.1) / 365.25)
    d = int(365.25 * c)
    e = int((b - d) / 30.6001)

    # Calculate day with decimal portion
    day_decimal = b - d - int(30.6001 * e) + f

    # Calculate month and year
    month = e - 1 if e < 14 else e - 13
    year = c - 4716 if month > 2 else c - 4715

    # Extract time components
    day = int(day_decimal)
    hour_decimal = (day_decimal - day) * 24
    hour = int(hour_decimal)
    minute_decimal = (hour_decimal - hour) * 60
    minute = int(minute_decimal)
    second_decimal = (minute_decimal - minute) * 60
    second = int(second_decimal)
    microsecond = int((second_decimal - second) * 1000000)

    return datetime(
        year, month, day, hour, minute, second, microsecond,
        tzinfo=timezone.utc
    )


def iso_to_julian_day(iso_string: str) -> float:
    """
    Convert ISO 8601 datetime string to Julian Day.

    Args:
        iso_string: ISO 8601 formatted datetime string

    Returns:
        Julian Day Number
    """
    dt = datetime.fromisoformat(iso_string)
    return datetime_to_julian_day(dt)
