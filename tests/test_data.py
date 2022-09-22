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


def test_get_valid_holidays_category_either_returns_all_categories() -> None:
    _holidays = [
        Holiday(
            1,
            "TestHotel",
            "TestCity",
            "TestContinent",
            "TestCountry",
            "active",
            1,
            "TestTempRating",
            "TestLocation",
            1
        ),
        Holiday(
            2,
            "TestHotel",
            "TestCity",
            "TestContinent",
            "TestCountry",
            "lazy",
            1,
            "TestTempRating",
            "TestLocation",
            1
        ),
        Holiday(
            3,
            "TestHotel",
            "TestCity",
            "TestContinent",
            "TestCountry",
            "active",
            1,
            "TestTempRating",
            "TestLocation",
            1
        )
    ]
    assert len(get_valid_holidays(_holidays, "Category", "either")) == 3
    assert get_valid_holidays(_holidays, "Category", "either") == _holidays


def test_get_valid_holidays_match_setting_is_valid_holiday() -> None:
    _holidays = [
        Holiday(
            1,
            "HotelName",
            "Leeds",
            "Europe",
            "England",
            "active",
            1,
            "cold",
            "city",
            80
        )
    ]

    assert len(get_valid_holidays(_holidays, "Continent", "asia")) == 0
    assert len(get_valid_holidays(_holidays, "TempRating", "cold")) == 1
    assert len(get_valid_holidays(_holidays, "Location", "city")) == 1
    assert len(get_valid_holidays(_holidays, "PricePerNight", 85)) == 1
    assert len(get_valid_holidays(_holidays, "PricePerNight", 80)) == 1
    assert len(get_valid_holidays(_holidays, "PricePerNight", 75)) == 0
