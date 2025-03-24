from fractions import Fraction

u2067 = b"\xe2\x81\xa7"
u2066 = b"\xe2\x81\xa6"
u2069 = b"\xe2\x81\xa9"


def bidi(line: str):
    decomped = list(line)
    embedding_level = [None] * len(line)
    current_level = 0
    highest_level = -1

    for i, ch in enumerate(decomped):
        if ch == "\u2067":
            assert current_level % 2 == 0
            current_level += 1
        if ch == "\u2066":
            assert current_level % 2 == 1
            current_level += 1
        if ch == "\u2069":
            current_level -= 1
        if (
            ch in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            and current_level % 2 == 1
        ):
            embedding_level[i] = current_level + 1
        else:
            embedding_level[i] = current_level
        highest_level = max(highest_level, embedding_level[i])

    while highest_level > 0:
        for j in range(len(decomped)):
            if embedding_level[j] == highest_level:
                k = j
                while embedding_level[k] == highest_level:
                    k += 1

                decomped[j:k] = decomped[j:k][::-1]

                for i in range(j, k):
                    if decomped[i] == ")":
                        decomped[i] = "("
                    elif decomped[i] == "(":
                        decomped[i] = ")"

                while j < k:
                    embedding_level[j] = highest_level - 1
                    j += 1
        highest_level -= 1

    return "".join(ch for ch in decomped if ch not in {"\u2067", "\u2066", "\u2069"})


def parse_number(n: str):
    if "/" in n:
        top, bottom = n.split("/")
        return Fraction(int(top), int(bottom))
    return int(n)


def compute(s: str):
    s = s.replace("\u2067", "")
    s = s.replace("\u2066", "")
    s = s.replace("\u2069", "")
    if " * " in s:
        lhs, rhs = s.split(" * ")
        return parse_number(lhs) * parse_number(rhs)
    if " / " in s:
        lhs, rhs = s.split(" / ")
        return Fraction(parse_number(lhs), parse_number(rhs))
    if " + " in s:
        lhs, rhs = s.split(" + ")
        return parse_number(lhs) + parse_number(rhs)
    if " - " in s:
        lhs, rhs = s.split(" - ")
        return parse_number(lhs) - parse_number(rhs)

    assert False, "invalid computation"


def eval_string(s: str):
    # Ignore all u2067, etc
    # Find the deepest paren, compute, recurse, etc
    for j in range(len(s)):
        if s[j] == "(":
            k = j + 1
            while s[k] not in {"(", ")"}:
                k += 1
            if s[k] == ")":
                return eval_string(s[0:j] + str(compute(s[j + 1 : k])) + s[k + 1 :])
            # otherwise fall through and compute from here
        else:
            j += 1

    return compute(s)


def test_bidi():
    assert (
        bidi("⁧(1 * ((⁦(66 / 2)⁩ - 15) - 4)) * (1 + (1 + 1))⁩")
        == "((1 + 1) + 1) * ((4 - (15 - (66 / 2))) * 1)"
    )
    assert (
        bidi(
            "73 + (3 * (1 * \u2067(((3 + (6 - 2)) * 6) + \u2066((52 * 6) / \u2067(13 - (7 - 2))\u2069)\u2069)\u2069))"
        )
        == "73 + (3 * (1 * (((52 * 6) / ((2 - 7) - 13)) + (6 * ((2 - 6) + 3)))))"
    )


def test_eval_string():
    assert eval_string("1 + (5 * 6)") == 31
    assert eval_string("((1 + 1) + 1) * ((4 - (15 - (66 / 2))) * 1)") == 66


def answer(lines: list[str]):
    total = 0
    for l in lines:
        total += abs(eval_string(l) - eval_string(bidi(l)))
    print(total)
