from app.data import get_all_holidays, get_valid_holidays
from app.holiday import Holiday


def test_get_all_holidays() -> None:
    holidays = get_all_holidays()
    assert len(holidays) > 0
    for holiday in holidays:
        assert isinstance(holiday, Holiday)


def test_get_valid_holidays() -> None:
    _holidays = [
        Holiday(
            1,
            "TestHotel",
            "TestCity",
            "TestContinent",
            "TestCountry",
            "TestCategory",
            1,
            "TestTempRating",
            "TestLocation",
            1
        )
    ]

    assert len(get_valid_holidays(_holidays, "StarRating", 5)) == 0
    assert len(get_valid_holidays(_holidays, "PricePerNight", 1)) == 1
