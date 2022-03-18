from datetime import timedelta, timezone
from pyutils.reminder import WEEKDAYS, Remind, RemindDate  # noqa F401


def test_remind():
    date = RemindDate(
        weekday=WEEKDAYS.FRIDAY, hour=15, timezone=timezone(timedelta(hours=3))
    )
    reminder = Remind(date, delay=timedelta(hours=1))

    assert reminder.lock
    assert reminder.last_seen is None
    assert reminder.state
    assert reminder.state["last_seen"] == reminder.last_seen
    assert reminder.date.weekday == WEEKDAYS.FRIDAY
    assert reminder.timedelta == timedelta(hours=1)
    assert reminder.date.timezone == timezone(timedelta(hours=3))
