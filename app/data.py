__all__ = ["get_all_holidays", "get_valid_holidays"]

import json
import os
from app.holiday import Holiday
from app.utils import lower_if_str


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


def get_valid_holidays(
    holidays: list[Holiday],
    key: str,
    value: str | int
) -> list[Holiday]:
    if key.lower() == "category" and value.lower() not in ["active", "lazy"]:
        return holidays

    out: list[Holiday] = []
    for holiday in holidays:
        match key.lower():
            case "continent" | "category" | "temprating" | "location":
                if lower_if_str(getattr(holiday, key)) == value.lower():
                    out.append(holiday)
            case "starrating":
                if int(getattr(holiday, key)) >= int(value):
                    out.append(holiday)
            case "pricepernight":
                if int(getattr(holiday, key)) <= int(value):
                    out.append(holiday)

    return out


def get_all_responses() -> list[dict[str, list[str]]]:
    """
    This reads in the potential responses from the response dataset
    """
    response_path = os.path.join("data", "responses.json")
    with open(response_path, "r") as data:
        responses = json.loads(data.read())

    return responses
