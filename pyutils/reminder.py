import asyncio
import typing as t
import dataclasses
import enum
import logging

from datetime import datetime, timedelta

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

    def __post_init__(self):
        if self.weekday == self.hour == self.minute is None:
            raise TypeError(f"any of {self!r} parameters must be supplied")


RD = t.TypeVar("RD", datetime, RemindDate)


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

    def set_last_seen(self):
        self.state["last_seen"] = datetime.now()

    async def wait_next(self) -> bool:
        raise NotImplementedError

    async def passive_remind(self) -> bool:
        if not isinstance(self.date, RemindDate):
            raise NotImplementedError

        async with self.lock:
            now = datetime.now()
            if (
                self.last_seen is not None
                and self.last_seen + self.timedelta > now  # noqa E501
            ):
                return False

            weekday, hour = now.weekday(), now.hour
            if weekday == self.date.weekday and hour == self.date.hour:
                self.set_last_seen()
                return True

            return False