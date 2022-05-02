from datetime import datetime, timedelta, timezone
from pyutils.reminder import WEEKDAYS, Remind, RemindDate  # noqa F401


async def test_remind():
    date = RemindDate(
        weekday=WEEKDAYS.FRIDAY, hour=15, timezone=timezone.utc
    )
    reminder = Remind(date, delay=timedelta(hours=1))

    date2 = datetime.now(timezone.utc)
    reminder2 = Remind(date2, delay=timedelta(minutes=2))

    assert reminder.lock and reminder2.lock
    assert (reminder.last_seen or reminder2.last_seen) is None
    assert reminder.state and reminder2.state
    assert reminder.state["last_seen"] == reminder2.last_seen
    assert reminder.weekday == WEEKDAYS.FRIDAY
    assert reminder2.weekday == date2.weekday()
    assert reminder.timedelta == timedelta(hours=1)
    assert reminder.timezone == reminder2.timezone == timezone.utc
    assert await reminder2.passive_remind()
    assert await reminder2.passive_remind() is False
    assert reminder2.last_seen
    assert (await reminder.passive_remind() is True) == (reminder.last_seen is not None)
