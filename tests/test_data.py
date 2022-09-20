from app.data import get_all_holidays
from app.holiday import Holiday


def test_get_all_holidays() -> None:
    holidays = get_all_holidays()
    assert len(holidays) > 0
    for holiday in holidays:
        assert isinstance(holiday, Holiday)
