from collections import defaultdict
from typing import List
from datetime import date


all_formats = ["YMD", "YDM", "DMY", "MDY"]


def date_from_format(format: str, date_str: str) -> date:
    first, second, third = [int(s) for s in date_str.split("-")]
    if format[0] == "Y":
        year = first
    elif format[1] == "Y":
        year = second
    elif format[2] == "Y":
        year = third
    else:
        raise ValueError("impossible")

    if format[0] == "M":
        month = first
    elif format[1] == "M":
        month = second
    elif format[2] == "M":
        month = third
    else:
        raise ValueError("impossible")

    if format[0] == "D":
        day = first
    elif format[1] == "D":
        day = second
    elif format[2] == "D":
        day = third
    else:
        raise ValueError("impossible")

    if year > 20:
        year = 1900 + year
    else:
        year = 2000 + year

    print(f"{year}-{month:02}-{day:02}")
    return date.fromisoformat(f"{year}-{month:02}-{day:02}")


def answer(lines: List[str]):
    # first create a reverse dict
    person_to_date_map = defaultdict(list)

    for line in lines:
        if len(line) == 0:
            continue

        ts, people = line.split(": ")
        for person in people.split(", "):
            person_to_date_map[person].append(ts)

    formats = defaultdict(lambda: set())
    for person in person_to_date_map:
        formats[person] = set(all_formats)

    for person, possiblities in person_to_date_map.items():
        for possiblity in possiblities:
            for format in all_formats:
                try:
                    _ = date_from_format(format, possiblity)
                except ValueError as e:
                    formats[person].discard(format)

    valid_people = []
    for person, possiblities in person_to_date_map.items():
        person_formats = formats[person]
        if len(person_formats) != 1:
            raise ValueError("did not eliminate all other options")
        person_format = next(iter(person_formats))
        for date_str in possiblities:
            d = date_from_format(person_format, date_str)
            print(person, date)
            if d == date(2001, 9, 11):
                valid_people.append(person)
                break

    print(" ".join(sorted(valid_people)))
