__all__ = ["get_all_holidays"]

import json
import os
from app.holiday import Holiday


def holiday_from_json(obj: dict[str, str | int]) -> Holiday:
    return Holiday(
        HolidayReference=obj["HolidayReference"],
        HotelName=obj["HotelName"],
        City=obj["City"],
        Continent=obj["Continent"],
        Country=obj["Country"],
        Category=obj["Category"],
        StarRating=obj["StarRating"],
        TempRating=obj["TempRating"],
        Location=obj["Location"],
        PricePerNight=obj["PricePerNight"]
    )


def get_all_holidays() -> list[Holiday]:
    """
    This reads in all of the holidays from the dataset\n
    Then returns them as a list of the Holiday object
    Which is declared in `holiday.py`
    """
    holiday_path = os.path.join("data", "holidays.json")
    with open(holiday_path, "r") as data:
        holidays = json.loads(data.read())

    return [holiday_from_json(holiday) for holiday in holidays]


def get_all_responses() -> list[dict[str, list[str]]]:
    """
    This reads in the potential responses from the response dataset
    """
    response_path = os.path.join("data", "responses.json")
    with open(response_path, "r") as data:
        responses = json.loads(data.read())

    return responses
