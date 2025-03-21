from typing import List
import re
from fractions import Fraction


numbers = {
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
}

ten_powers = {
    "十": 10,
    "百": 100,
    "千": 1_000,
    "万": 10_000,
    "億": 100_000_000,
}


def japanese_to_number(s: str) -> int:
    parts = re.split(r"億|万", s)
    multiplier = 0
    total = 0
    for part in parts[::-1]:
        part_total = 0
        j = 0
        while j < len(part):
            if part[j] in ten_powers:
                part_total += ten_powers[part[j]]
                j += 1
                continue

            if j == len(part) - 1:
                part_total += numbers[part[j]]
                j += 1
                continue

            part_total += numbers[part[j]] * ten_powers[part[j + 1]]
            j += 2

        total += (10_000**multiplier) * part_total
        multiplier += 1
    return total


units_of_length = {
    "尺": Fraction(10, 33),
}
units_of_length["間"] = units_of_length["尺"] * 6
units_of_length["丈"] = units_of_length["尺"] * 10
units_of_length["町"] = units_of_length["尺"] * 360
units_of_length["里"] = units_of_length["尺"] * 12960
units_of_length["毛"] = units_of_length["尺"] / 10_000
units_of_length["厘"] = units_of_length["尺"] / 1_000
units_of_length["分"] = units_of_length["尺"] / 100
units_of_length["寸"] = units_of_length["尺"] / 10


def test_japanese_to_number():
    assert japanese_to_number("三百") == 300
    assert japanese_to_number("三百二十一") == 321
    assert japanese_to_number("四千") == 4000
    assert japanese_to_number("五万") == 50000
    assert japanese_to_number("九万九千九百九十九") == 99999
    assert japanese_to_number("四十二万四十二") == 420042
    assert japanese_to_number("九億八千七百六十五万四千三百二十一") == 987654321


def quantity(s: str) -> Fraction:
    return japanese_to_number(s[:-1]) * units_of_length[s[-1]]


def test_quantity():
    assert quantity("二百四十二町") == 242 * units_of_length["町"]


def answer(lines: List[str]):
    lines = lines[:-1]
    total = 0
    for line in lines:
        print(line)
        first, second = line.split(" × ")
        print(first, second)
        total += quantity(first) * quantity(second)

    print(total)
