import pytest
import typing as t
from pyutils.reminder import parse_hour, parse_weekday, WEEKDAYS, RemindDate # noqa F401


def test_parse_weekday():
    assert parse_weekday("friday") == WEEKDAYS.FRIDAY
    assert parse_weekday("TUESDAY") == WEEKDAYS.TUESDAY
    assert parse_weekday("MonDay") == WEEKDAYS.MONDAY
    assert parse_weekday("wednesday") != WEEKDAYS.SUNDAY


def test_parse_hour():
    assert parse_hour("15") == (15, 0)
    assert parse_hour("15.13") == (15, 13)
    assert parse_hour("12:40") == (12, 40)
    assert parse_hour("1") != (17, 50)


@pytest.fixture
def remind_dates():
    return [
        RemindDate(weekday=WEEKDAYS.FRIDAY),
        RemindDate(hour=15),
        RemindDate(minute=40),
        RemindDate(weekday=WEEKDAYS.MONDAY, hour=9, minute=10),
        RemindDate(weekday=WEEKDAYS.TUESDAY, hour=15),
        RemindDate(weekday=WEEKDAYS.SATURDAY, minute=10),
        RemindDate(hour=18, minute=10),
    ]


def test_remind_date(remind_dates: t.List[RemindDate]):
    with pytest.raises(TypeError):
        RemindDate()

    for date in remind_dates:
        assert (date.hour or date.minute or date.weekday) is not None
