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
    StarRating: int
    TempRating: str
    Location: str
    PricePerNight: int

    def __str__(self) -> str:
        return f"""
Hotel {self.HotelName} in {self.City}, {self.Country}.
Rating: {self.StarRating}⭐.
£{self.PricePerNight} / Night.
"""
