from datetime import datetime, timedelta, timezone
from pyutils.reminder import WEEKDAYS, Remind, RemindDate  # noqa F401


async def test_remind():
    date = RemindDate(weekday=WEEKDAYS.FRIDAY, hour=15, timezone=timezone.utc)
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

    # if reminder works -> it sets the last_seen
    assert (await reminder.passive_remind() is True) == (reminder.last_seen is not None)


async def test_remind_minute():
    now = datetime.now()
    date = RemindDate(minute=now.minute)
    reminder = Remind(date)

    incorrect_date = RemindDate(minute=(now.minute == 59 and 15) or 59)
    incorrect_reminder = Remind(incorrect_date)

    assert await reminder.passive_remind()
    assert await reminder.passive_remind() is False
    assert await incorrect_reminder.passive_remind() is False


async def test_remind_datetime():
    next_week = datetime.now(timezone.utc) + timedelta(weeks=1)
    previous_week = datetime.now(timezone.utc) + timedelta(weeks=-1)

    next, previous = Remind(next_week), Remind(previous_week)

    # datetime objects should not `remind` if date is passed
    # even if the both weekdays and hours are the same
    assert await next.passive_remind() is False
    assert await previous.passive_remind() is False
