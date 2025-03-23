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
    try:
        bytes.fromhex(line).decode("utf-8")
    except UnicodeDecodeError as e:
        suffix.insert(0, line[e.start * 2 :])
        line = line[: e.start * 2]

    return Fragment(line, "".join(prefix), "".join(suffix))


def test_parse():
    assert parse_fragment("91808d7ee2898b7ec3b1c3b17ec3b17e") == Fragment(
        "7ee2898b7ec3b1c3b17ec3b17e",
        "91808d",
        "",
    )
    assert parse_fragment("e29591c3b1c3b1e2898b7e7ee2898bf0") == Fragment(
        "e29591c3b1c3b1e2898b7e7ee2898b",
        "",
        "f0",
    )


def print_fragment_line(line: str):
    return bytes.fromhex(line).decode("utf-8", errors="replace")


def paragraph_string(p: List[Fragment]):
    return "\n".join(print_fragment_line(f.line) for f in p)


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
    if fragment2.prefix == "" and (
        fragment2.line.startswith("7c") or fragment2.line.startswith("e29591")
    ):
        print("cannot merge since fragment2 starts with a bar")
        return None

    if fragment1.suffix == "" and (
        fragment1.line.endswith("7c") or fragment1.line.endswith("e29591")
    ):
        print("cannot merge since fragment1 ends with a bar")
        return None

    if fragment1.suffix == "" and fragment2.prefix == "":
        return Fragment(fragment1.line + fragment2.line, "", "")

    if fragment1.suffix == "":
        print("cannot merge since fragment2 has a prefix but fragment1 has no suffix")
        return None

    if fragment2.prefix == "":
        print("cannot merge since fragment1 has a suffix and fragment2 has no prefix")
        return None

    # next check that the bytes are correct
    first_byte = int(fragment1.suffix[0:2], 16)
    if first_byte >> 7 == 0:
        # single byte should be impossible
        assert False, "UTF-8 encoding with single byte"

    merge_ok = True
    if first_byte >> 5 == 0b110:
        print("2 bytes")
        merge_ok = len(fragment1.suffix) + len(fragment2.prefix) == 4
    elif first_byte >> 4 == 0b1110:
        merge_ok = len(fragment1.suffix) + len(fragment2.prefix) == 6
    elif first_byte >> 3 == 0b11110:
        merge_ok = len(fragment1.suffix) + len(fragment2.prefix) == 8
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
    else:
        print("no merge", fragment1, fragment2)

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

    while len(parsed_paragraphs) > 1:
        print("LOOP STARTING", len(parsed_paragraphs))
        next_paragraphs = []

        found_match = False
        for p1, p2 in combinations_with_replacement(parsed_paragraphs, 2):
            # We'll only try if len(p1) <= len(p2) (merging p1 INTO p2)
            if p1 == p2 or len(p1) > len(p2):
                continue
            i = 0
            merged_paragraphs = []

            offset = 0
            found_match = False
            while len(p1) + offset <= len(p2):
                merged_paragraphs = copy(p2[0:offset])
                while i < len(p1):
                    if f := merge_fragments(p1[i], p2[i + offset]):
                        print("-----")
                        print("merged")
                        print(print_fragment_line(p1[i].line))
                        print(print_fragment_line(p2[i + offset].line))
                        print("into")
                        print(print_fragment_line(f.line))
                        print("-----")

                        merged_paragraphs.append(f)
                    else:
                        # print("><><><><><><><")
                        # print("womp womp")
                        # print(print_fragment_line(p1[i].line))
                        # print(print_fragment_line(p2[i + offset].line))
                        # print("><><><><><><><")

                        merged_paragraphs = []
                        break
                    i += 1
                else:
                    # We have a match, add the rest of p2
                    while i < len(p2):
                        merged_paragraphs.append(p2[i])
                        i += 1
                    found_match = True

                if found_match:
                    break
                offset += 1

            if found_match:
                # Here's our match; yeah, this is inefficient
                next_paragraphs = copy(parsed_paragraphs)
                next_paragraphs.remove(p1)
                next_paragraphs.remove(p2)
                next_paragraphs.append(merged_paragraphs)

                print("offset", i)
                print("MERGING")
                print(paragraph_string(p1))
                print("AND")
                print(paragraph_string(p2))
                print("RESULT", paragraph_string(merged_paragraphs))
                break
        else:
            print("no matches found", parsed_paragraphs)
            assert False, "no match found"

        parsed_paragraphs = next_paragraphs

    print(parsed_paragraphs)
