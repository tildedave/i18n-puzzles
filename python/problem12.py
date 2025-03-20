from functools import cmp_to_key, partial
from typing import List
import unicodedata

english_alphabet = 'abcdefghijklmnopqrstuvwxyz'
english_letter_idxs = dict((v, k) for k, v in enumerate(english_alphabet))
for k, v in enumerate(english_alphabet.upper()):
    english_letter_idxs[v] = k
english_letter_idxs['ø'] = english_letter_idxs['o']
english_letter_idxs['ø'.upper()] = english_letter_idxs['o']
english_letter_idxs['å'] = english_letter_idxs['a']
english_letter_idxs['å'.upper()] = english_letter_idxs['a']
english_letter_idxs['ä'] = english_letter_idxs['a']
english_letter_idxs['ä'.upper()] = english_letter_idxs['a']

swedish_alphabet = 'abcdefghijklmnopqrstuvwxyzåäö'
swedish_letter_idxs = dict((v, k) for k, v in enumerate(swedish_alphabet))
for k, v in enumerate(swedish_alphabet.upper()):
    swedish_letter_idxs[v] = k

swedish_letter_idxs['æ'] = swedish_letter_idxs['ä']
swedish_letter_idxs['ø'] = swedish_letter_idxs['ö']
swedish_letter_idxs['æ'.upper()] = swedish_letter_idxs['ä']
swedish_letter_idxs['ø'.upper()] = swedish_letter_idxs['ö']

def english_accent_stripper(s: str):
    result = []
    s = s.replace('Æ', 'ae')
    for nc in unicodedata.normalize('NFD', s):
        if nc in english_letter_idxs:
            result.append(nc)

    return ''.join(result)

def swedish_accent_stripper(s):
    result = []
    for oc in s:
        if oc in swedish_letter_idxs:
            result.append(oc)

    return ''.join(result)


def dutch_accent_stripper(s):
    result = []
    idx = -1
    s = s.replace('Æ', 'AE')

    for i in range(len(s)):
        if s[i].isupper():
            idx = i
            break

    if idx == -1:
        raise ValueError('did not find first uppercase')

    for nc in unicodedata.normalize('NFD', s[idx:]):
        if nc in english_letter_idxs:
            result.append(nc)

    return ''.join(result)


def compare_lines(comparator, accent_stripper, line1, line2):
    name1 = line1.split(':')[0]
    name2 = line2.split(':')[0]

    last_name1, first_name1 = name1.split(',')
    last_name2, first_name2 = name2.split(',')

    print('name', last_name1, 'stripped', accent_stripper(last_name1), '|', 'name', last_name2, 'stripped', accent_stripper(last_name2), last_name2)

    if d := comparator(accent_stripper(last_name1), accent_stripper(last_name2)):
        return d

    return comparator(accent_stripper(first_name1), accent_stripper(first_name2))


def word_comparator(is_letter, letter_comparator, s1, s2):
    while s1:
        if not s2:
            return -1

        c1 = s1[0]
        if not is_letter(c1):
            print('unknown letter', c1)
            s1 = s1[1:]
            continue

        c2 = s2[0]
        if not is_letter(c2):
            print('unknown letter', c2)
            s2 = s2[1:]
            continue

        if s := letter_comparator(c1, c2):
            return s

        s1 = s1[1:]
        s2 = s2[1:]

    return 0


def letter_comparator(alphabet_idxs, c1, c2):
    i1 = alphabet_idxs[c1]
    i2 = alphabet_idxs[c2]
    if i1 == i2:
        return 0
    if i1 < i2:
        return -1
    if i2 < i1:
        return 1
    assert False


english_word_comparator = partial(
    word_comparator,
    lambda c : c in english_letter_idxs,
    partial(letter_comparator, english_letter_idxs))

swedish_word_comparator = partial(
    word_comparator,
    lambda c : c in swedish_letter_idxs,
    partial(letter_comparator, swedish_letter_idxs))

def test_english_comparator():
    assert english_word_comparator('Olofsson', 'O\'Neill') == -1
    assert english_word_comparator('O\'Neill', 'Olofsson') == 1


def test_swedish_comparator():
    assert swedish_word_comparator('Ök', 'Øl') == -1
    assert swedish_word_comparator('Øl', 'Öm') == -1
    assert swedish_word_comparator('Navarrete Ortiz', 'Vandersteen') == -1
    assert swedish_word_comparator('Reynoso Pedroza', 'Anttila') == 1


def answer(lines: List[str]):
    lines = lines[:-1]
    middle = (len(lines) - 1) // 2

    english_sorted = sorted(lines, key=cmp_to_key(partial(compare_lines, english_word_comparator, english_accent_stripper)))
    swedish_sorted = sorted(lines, key=cmp_to_key(partial(compare_lines, swedish_word_comparator, swedish_accent_stripper)))
    dutch_sorted = sorted(lines, key=cmp_to_key(partial(compare_lines, english_word_comparator, dutch_accent_stripper)))

    a = int(english_sorted[middle].split(':')[1].strip())
    b = int(swedish_sorted[middle].split(':')[1].strip())
    c = int(dutch_sorted[middle].split(':')[1].strip())

    print(a * b * c)
