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
        lines = [
            f"\nHotel {self.HotelName} in {self.City}, {self.Country}",
            f"Continent: {self.Continent.capitalize()}.",
            f"Location: {self.Location.capitalize()}",
            f"Rating: {self.StarRating}⭐",
            f"Temperature: {self.TempRating.capitalize()}",
            f"Price: £{self.PricePerNight} / Night"
        ]
        return "\n".join(lines)
