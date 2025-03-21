from typing import Optional, List
from functools import lru_cache

letters = dict((v, k) for k, v in enumerate("αβγδεζηθικλμνξοπρστυφχψω"))
letters["ς"] = letters["σ"]
for k, v in enumerate("ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"):
    letters[v] = k

variants = [
    "Οδυσσευς",
    "Οδυσσεως",
    "Οδυσσει",
    "Οδυσσεα",
    "Οδυσσευ",
]

# so the way you do this is for each word seeing if the "differences" in the
# letters match a precomputed series of differences.  we will do it per word


def _char_diffs(s: str):
    prev = 0
    yield 0
    prev = letters[s[0]]
    for ch in s[1:]:
        if ch not in letters:
            return

        next = letters[ch]
        yield (next - prev) % 24
        prev = next


@lru_cache
def char_diffs(s: str):
    return list(_char_diffs(s))


def char_shifts_required(word, dest):
    if char_diffs(word) != char_diffs(dest):
        return None

    word_idx = letters[word[0]]
    dest_idx = letters[dest[0]]
    if word_idx < dest_idx:
        return dest_idx - word_idx

    return 24 + dest_idx - word_idx


def test_char_shifts_required():
    assert char_shifts_required("Ξγτρρδτρ", "Οδυσσευς") == 1
    assert char_shifts_required("Φκβωωλβ", "Οδυσσευ") == 18


def contains_odysseus(s: str) -> Optional[int]:
    for word in s.split(" "):
        for variant in variants:
            if shift := char_shifts_required(word, variant):
                return shift

    return None


def test_contains_odyssesus():
    assert contains_odysseus("σζμ γ' ωοωλδθαξλδμξρ οπξρδυζ οξκτλζσθρ Ξγτρρδτρ.") == 1
    assert contains_odysseus("αφτ κ' λαλψφτ ωπφχλρφτ δξησηρζαλψφτ φελο, Φκβωωλβ.") == 18
    assert contains_odysseus("γ βρφαγζ ωνψν ωγφ πγχρρφ δρδαθωραγζ ρφανφ.") == None


def answer(lines: List[str]):
    total_shifts = 0
    for line in lines:
        if not line:
            continue
        if shift := contains_odysseus(line):
            total_shifts += shift

    print(total_shifts)
