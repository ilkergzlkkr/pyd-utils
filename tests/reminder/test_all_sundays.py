from datetime import date, timedelta


def allsundays(year):
    d = date(year, 1, 1)  # January 1st
    d += timedelta(days=6 - d.weekday())  # First Sunday
    while d.year == year:
        yield d
        d += timedelta(days=7)


def test_sundays():
    for d in allsundays(2022):
        assert d
