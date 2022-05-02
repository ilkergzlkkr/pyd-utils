import asyncio
import typing as t
import dataclasses
import enum
import logging

from datetime import datetime, timedelta, timezone

log = logging.getLogger(__name__)


class WEEKDAYS(enum.IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


def parse_weekday(weekday: str) -> WEEKDAYS:
    if weekday.upper() in WEEKDAYS._member_names_:
        return WEEKDAYS._member_map_[weekday.upper()]


def parse_hour(hour: str) -> t.Tuple[float, float]:
    hour = hour.replace(".", ":")
    if ":" in hour:
        hour, minute = hour.split(":")
    else:
        minute = None
    return float(hour), float(minute) if minute else 0.0


@dataclasses.dataclass
class RemindDate:
    weekday: t.Optional[WEEKDAYS] = None
    hour: float = None
    minute: float = None
    timezone: t.Optional[timezone] = None

    def __post_init__(self):
        if self.weekday == self.hour == self.minute is None:
            raise TypeError(f"any of {self!r} parameters must be supplied")


RD = t.TypeVar("RD", datetime, RemindDate)
# TODO: if reminder is in a specific datetime
# ask for start & end argument NOT delay argument
# remove weekday property


class Remind:
    def __init__(
        self,
        date: RD,
        delay: t.Optional[timedelta] = None,
        lock: t.Optional[asyncio.Lock] = None,
    ) -> None:
        self.date = date
        self.timedelta = delay or timedelta(hours=1)
        self.lock = lock or asyncio.Lock()
        self.state = {"last_seen": None}

    @property
    def last_seen(self) -> t.Optional[datetime]:
        return self.state["last_seen"]

    @property
    def weekday(self) -> t.Optional[WEEKDAYS]:
        return (
            self.date.weekday()
            if isinstance(self.date, datetime)
            else self.date.weekday
        )

    @property
    def timezone(self) -> t.Optional[timezone]:
        return (
            self.date.tzinfo if isinstance(self.date, datetime) else self.date.timezone
        )

    def set_last_seen(self):
        self.state["last_seen"] = datetime.now(tz=self.timezone)

    async def wait_next(self) -> bool:
        raise NotImplementedError

    async def passive_remind(self) -> bool:
        async with self.lock:
            now = datetime.now(tz=self.timezone)
            if (
                self.last_seen is not None
                and self.last_seen + self.timedelta > now  # noqa E501
            ):
                return False

            if isinstance(self.date, datetime):
                # >---- (reached, date)---timedelta---(passed) ----<
                passed = now > self.date + self.timedelta
                reached = now >= self.date

                if passed or not reached:
                    return False

            else:
                weekday, hour, minute = now.weekday(), now.hour, now.minute
                # optionals passed from check using -or-
                if (
                    weekday != (self.weekday or weekday)
                    or hour != (self.date.hour or hour)
                    or minute != (self.date.minute or minute)
                ):
                    return False

            self.set_last_seen()
            return True
