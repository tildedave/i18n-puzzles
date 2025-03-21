from collections import defaultdict
from typing import List, Set
from dataclasses import dataclass
import pytz
from datetime import datetime, date, timedelta

# Offices work from Monday to Friday, from 08:30 to 17:00, excluding public
# holidays. Everything is relative to a customer; for every 30 minutes of every
# day a customer cares, see if there's coverage.  if no coverage, increment by
# 30, continue

# To keep it simple for customers, TOPlap gives them support from 00:00 monday
# to 24:00 friday in their own time zone.


def is_weekday(d: date):
    return d.weekday() < 5


def test_stuff():
    customer_tz = pytz.timezone("America/Halifax")
    start_dt = customer_tz.localize(datetime(2022, 1, 1))
    ts = start_dt.timestamp()
    dt = datetime.fromtimestamp(ts, customer_tz)
    while dt.year != 2023:
        print(dt, dt.date().weekday())
        ts += 30 * 60
        dt = datetime.fromtimestamp(ts, customer_tz)

    assert False


@dataclass
class Location:
    name: str
    timezone: pytz.tzinfo.BaseTzInfo
    holidays: Set[date]


def parse_location(s: str) -> Location:
    name, tz_str, holiday_strs = s.split("\t")
    holidays = set()
    for s in holiday_strs.split(";"):
        holidays.add(datetime.strptime(s, "%d %B %Y").date())

    return Location(name, pytz.timezone(tz_str), holidays)


def answer(lines: List[str]):
    lines = lines[:-1]
    splitter = -1
    for i, line in enumerate(lines):
        if line == "":
            splitter = i
            break

    office_lines, customer_lines = lines[0:splitter], lines[splitter + 1 :]
    offices = [parse_location(l) for l in office_lines]
    customers = [parse_location(l) for l in customer_lines]

    start_dt = pytz.utc.localize(datetime(2022, 1, 1))
    end_dt = pytz.utc.localize(datetime(2023, 1, 1))

    # start_dt = pytz.utc.localize(datetime(2022, 12, 9))
    # end_dt = pytz.utc.localize(datetime(2022, 12, 10))

    dt = start_dt
    overtime_by_customer = defaultdict(int)

    while dt < end_dt:
        # Coverage is based on if the time is between 08:30 to 17:00
        # in their time
        has_coverage = False
        for office in offices:
            office_dt = dt.astimezone(office.timezone)
            if not is_weekday(office_dt.date()):
                continue

            if office_dt.date() in office.holidays:
                continue

            start_workday = office.timezone.localize(
                datetime(
                    office_dt.year,
                    office_dt.month,
                    office_dt.day,
                    hour=8,
                    minute=30,
                    second=0,
                )
            )
            end_workday = office.timezone.localize(
                datetime(
                    office_dt.year,
                    office_dt.month,
                    office_dt.day,
                    hour=17,
                    minute=0,
                    second=0,
                )
            )
            if start_workday <= office_dt < end_workday:
                has_coverage = True
                break

        for customer in customers:
            customer_dt = dt.astimezone(customer.timezone)
            if not is_weekday(customer_dt.date()):
                continue

            # Check if it's a holiday for the customer
            if customer_dt.date() in customer.holidays:
                continue

            if not has_coverage:
                overtime_by_customer[customer.name] += 30

        dt += timedelta(minutes=30)

    result = sorted(overtime_by_customer.values())
    print(result[-1] - result[0])
