from typing import List
import unicodedata
import re
from collections import Counter


def answer(lines: List[str]):
    num_valid = 0

    for line in lines:
        if line == '':
            continue

        if password_is_valid(line):
            num_valid += 1

    print(num_valid)


def password_is_valid(line: str) -> bool:
    if len(line) < 4 or len(line) > 12:
        return False

    has_digit = False
    has_vowel = False
    has_consonant = False
    letters = Counter()

    for ch in line:
        if ch.isdigit():
            # print(f'{ch} is a digit')
            has_digit = True
            continue

        l = letter(ch)
        if not l:
            continue

        if l.lower() in ['a', 'e', 'i', 'o', 'u']:
            has_vowel = True
        else:
            has_consonant = True

        letters[l.lower()] += 1
        if letters[l.lower()] == 2:
            return False

    return has_digit and has_vowel and has_consonant

def letter(ch: str):
    desc = unicodedata.name(ch)
    if m := re.search(r' LETTER (\w).*', desc):
        letter = m.group(1)
        category = unicodedata.category(ch)
        if category[1] == 'l':
            return letter.lower()
        elif category[1] == 'u':
            return letter.upper()
    else:
        return None


def test_letter():
    assert letter('ë') == 'e'
    assert letter('ñ') == 'n'
    assert letter('ŷ') == 'y'


def test_passwords():
    assert not password_is_valid('iS0')
    assert not password_is_valid('V8AeC1S7KhP4Ļu')
    assert not password_is_valid('pD9Ĉ*jXh')
    assert not password_is_valid('E1-0')
    assert not password_is_valid('ĕnz2cymE')
    assert not password_is_valid('tqd~üō')
    assert password_is_valid('IgwQúPtd9')
    assert password_is_valid('k2lp79ąqV')
