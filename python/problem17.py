from copy import copy
from typing import List
from dataclasses import dataclass
from itertools import combinations_with_replacement


@dataclass
class Fragment:
    line: str
    prefix: str
    suffix: str


def parse_fragment(line: str):
    prefix = []
    suffix = []
    while int(line[0:2], 16) >> 6 == 0b10:
        prefix.append(line[0:2])
        line = line[2:]
    while int(line[-2:], 16) >> 6 == 0b10:
        suffix.insert(0, line[-2:])
        line = line[:-2]

    return Fragment(line, "".join(prefix), "".join(suffix))


def test_parse():
    assert parse_fragment("91808d7ee2898b7ec3b1c3b17ec3b17e") == (
        "7ee2898b7ec3b1c3b17ec3b17e",
        "91808d",
        "",
    )


def paragraphs(lines):
    paragraph = []
    for line in lines:
        if line == "":
            yield paragraph
            paragraph = []
        else:
            paragraph.append(line)

    yield paragraph


def merge_fragments(fragment1: Fragment, fragment2: Fragment):
    if fragment1.suffix == "" and fragment2.prefix == "":
        return Fragment(fragment1.line + fragment2.line, "", "")

    if fragment1.suffix == "" or fragment2.prefix == "":
        return None

    # next check that the bytes are correct
    first_byte = int(fragment1.suffix[0:2], 16)
    if first_byte >> 7 == 0:
        # single byte should be impossible
        assert False, "UTF-8 encoding with single byte"

    merge_ok = True
    if first_byte >> 5 == 0b110:
        merge_ok = len(fragment1.suffix) + len(fragment2.prefix) == 2
    elif first_byte >> 4 == 0b1110:
        merge_ok = len(fragment1.suffix) + len(fragment2.prefix) == 3
    elif first_byte >> 3 == 0b11110:
        merge_ok = len(fragment1.suffix) + len(fragment2.prefix) == 4
    else:
        print(first_byte, fragment1.suffix, "0b{:b}".format(first_byte))
        print(fragment1, fragment2)
        assert False, "impossible"

    if merge_ok:
        combinated = fragment1.suffix + fragment2.prefix
        for i in range(2, len(combinated), 2):
            b = combinated[i : i + 2]
            assert int(b, 16) >> 6 == 0b10

        return Fragment(
            fragment1.line + fragment1.suffix + fragment2.prefix,
            fragment1.prefix,
            fragment2.suffix,
        )

    return None


def answer(lines: List[str]):
    lines = lines[:-1]

    # Lining up also requires
    parsed_paragraphs = []
    for paragraph in paragraphs(lines):
        parsed_paragraph = []
        for line in paragraph:
            parsed_paragraph.append(parse_fragment(line))
        parsed_paragraphs.append(parsed_paragraph)

    # We need to merge these together.  Merging can be at any line however
    for p in parsed_paragraphs:
        print(p)

    # It seems plausible to believe that we won't have to find partial
    # matches, e.g. placing but maybe we will.  The example seems to indicate a world
    # where we patchwork it together.
    while len(parsed_paragraphs) > 1:
        next_paragraphs = []

        for p1, p2 in combinations_with_replacement(parsed_paragraphs, 2):
            i = 0
            merged_paragraphs = []
            while i < len(p1) and i < len(p2):
                i += 1
                if f := merge_fragments(p1[i], p2[i]):
                    merged_paragraphs.append(f)
                else:
                    merged_paragraphs = []
                    break
            else:
                print("sweet")
                if i < len(p1):
                    while i < len(p1):
                        merged_paragraphs.append(p1[i])
                        i += 1
                elif i < len(p2):
                    while i < len(p2):
                        merged_paragraphs.append(p2[i])
                        i += 1

            if merged_paragraphs:
                # Here's our match; yeah, this is inefficient
                next_paragraphs = copy(parsed_paragraphs)
                next_paragraphs.remove(p1)
                next_paragraphs.remove(p2)
                next_paragraphs.append(merged_paragraphs)
                break
        else:
            assert False, "no match found"

        parsed_paragraphs = next_paragraphs

    print(parsed_paragraphs)
