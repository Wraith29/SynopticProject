__all__ = ["Holiday"]

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Holiday:
    HolidayReference: int
    HotelName: str
    City: str
    Continent: str
    Country: str
    Category: str
    StarRating: str
    TempRating: str
    Location: str
    PricePerNight: int