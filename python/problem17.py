from copy import copy
from typing import List
from dataclasses import dataclass
from itertools import combinations_with_replacement


@dataclass
class Fragment:
    line: str
    prefix: str
    suffix: str

    def length(self):
        return len(self.line) + len(self.prefix) + len(self.suffix)


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


def ends_with_bar(f: Fragment) -> bool:
    return f.suffix == "" and (f.line.endswith("7c") or f.line.endswith("e29591"))


def starts_with_bar(f: Fragment):
    return f.prefix == "" and (f.line.startswith("7c") or f.line.startswith("e29591"))


def merge_fragments(fragment1: Fragment, fragment2: Fragment):
    if starts_with_bar(fragment2):
        # print("cannot merge since fragment2 starts with a bar")
        return None

    if ends_with_bar(fragment1):
        # print("cannot merge since fragment1 ends with a bar")
        return None

    if fragment1.suffix == "" and fragment2.prefix == "":
        return Fragment(
            fragment1.line + fragment2.line, fragment1.prefix, fragment2.suffix
        )

    if fragment1.suffix == "":
        # print("cannot merge since fragment2 has a prefix but fragment1 has no suffix")
        return None

    if fragment2.prefix == "":
        # print("cannot merge since fragment1 has a suffix and fragment2 has no prefix")
        return None

    # next check that the bytes are correct
    first_byte = int(fragment1.suffix[0:2], 16)
    if first_byte >> 7 == 0:
        # single byte should be impossible
        assert False, "UTF-8 encoding with single byte"

    merge_ok = True
    if first_byte >> 5 == 0b110:
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

        f = Fragment(
            fragment1.line + fragment1.suffix + fragment2.prefix + fragment2.line,
            fragment1.prefix,
            fragment2.suffix,
        )
        assert f.length() == fragment1.length() + fragment2.length()
        return f
    # else:
    # print("no merge", fragment1, fragment2)

    return None


min_match_lines = 4


def test_sliding():
    p1 = [1] * 10
    p2 = [2] * 10
    # p1 slides forward
    for p2_offset in range(len(p2)):
        # prefix is [:p2_offset] p1 [p1 suffix]
        # only test for a match if the overlap is within min_match_lines
        prefix = p2[:p2_offset]
        overlap_idx = min(len(p2) - p2_offset, len(p1))
        p1_overlap = p1[:overlap_idx]
        p2_section = p2[p2_offset : p2_offset + overlap_idx]
        if len(p1) > overlap_idx:
            suffix = p1[overlap_idx:]
        else:
            suffix = p2[p2_offset + overlap_idx :]

        print(prefix, (p1_overlap, p2_section), suffix)
    # assert False


def merge_paragraphs(p1: List[Fragment], p2: List[Fragment]):
    # we want to run p1 | p2 next to each other so that at least
    # min_match_lines match
    # we'll have some slice logic, then we'll test the overlap is at least
    # min_match_lines
    # our perspective will be from p1's
    # we will consider starting like p1 p2 and then sliding p1 "forward" to match p2
    for p2_offset in range(len(p2)):
        # prefix is [:p2_offset] p1 [p1 suffix]
        # only test for a match if the overlap is within min_match_lines
        prefix = p2[:p2_offset]
        overlap_idx = min(len(p2) - p2_offset, len(p1))
        p1_overlap = p1[:overlap_idx]
        p2_overlap = p2[p2_offset : p2_offset + overlap_idx]
        if len(p1) > overlap_idx:
            suffix = p1[overlap_idx:]
        else:
            suffix = p2[p2_offset + overlap_idx :]

        if len(p1_overlap) < min_match_lines:
            continue

        merged = [merge_fragments(f1, f2) for f1, f2 in zip(p1_overlap, p2_overlap)]
        if all(merged):
            return prefix + merged + suffix

    # Slide p2 along p1 since this is required :-|
    for p1_offset in range(len(p1)):
        # prefix is [:p1_offset] p2 [suffix]
        prefix = p1[:p1_offset]
        overlap_idx = min(len(p1) - p1_offset, len(p2))
        p2_overlap = p2[:overlap_idx]
        p1_overlap = p1[p1_offset : p1_offset + overlap_idx]
        if len(p2) > overlap_idx:
            suffix = p2[overlap_idx:]
        else:
            suffix = p1[p1_offset + overlap_idx :]

        if len(p2_overlap) < min_match_lines:
            continue

        merged = [merge_fragments(f1, f2) for f1, f2 in zip(p1_overlap, p2_overlap)]
        if all(merged):
            return prefix + merged + suffix

    return None


def test_merge2():
    p1 = [
        Fragment(
            line="e295942de295902de295902de295902de295902de295902de295902de295902d2de295902de295902de295902de29597",
            prefix="",
            suffix="",
        ),
        Fragment(
            line="7c7ee2898be2898bc3b1c3b1e2898b7e7ec3b1f091808de2898bc3b17e7ec3b1e2898b7ec3b1c3b1f091808d7ec3b17c",
            prefix="",
            suffix="",
        ),
        Fragment(
            line="e29591c3b1c3b1e2898b7e7ee2898bf091808d7ee2898b7ec3b1c3b17ec3b17ec3b1c3b1c3b1e2898bc3b17e7ee29591",
            prefix="",
            suffix="",
        ),
        Fragment(
            line="7c7ec3b1c3b1f091808dc3b1e2898bf091808d2dc2af7ec3b1c3b1c3b1c3b1c3b1c3b1c3b1e288922dc2afc2afc3b17c",
            prefix="",
            suffix="",
        ),
        Fragment(
            line="e295917ee2898bc3b17ec2af2df090b2a32dc2afc2afc2afc3b17ee2898bf091808de2898bc3b12d2d2d2dc3b1e29591",
            prefix="",
            suffix="",
        ),
        Fragment(
            line="7cc3b1e2898bc3b1c3b1e288922df090b2a32dc2afc2af2dc3b1c3b1c3b1f091808dc3b1c2afc2afe28892c2af2d7e7c",
            prefix="",
            suffix="",
        ),
        Fragment(
            line="e29591c3b1e2898b7e7ec2afe28892f090b2a32d2dc2afc2af2d7ec3b1f091808de2898b7ec2af2d2dc3b1c3b1e29591",
            prefix="",
            suffix="",
        ),
        Fragment(
            line="7c7ee2898bc3b1c3b1f090b2a32de28892c2afc2a4c2afe288922de2898b7ee2898b7ec3b1e2898bc2afe2898b7e7e7c",
            prefix="",
            suffix="",
        ),
        Fragment(
            line="e295917e7ec3b1c3b17ef090b2a3f090b2a3c2afc2aff090b2a32d2d2dc3b1",
            prefix="",
            suffix="c3",
        ),
        Fragment(
            line="7c7ec3b1e2898bf091808d7ee2898be2898b2d2dc2afc2afc2afe2898bc3b17e",
            prefix="",
            suffix="",
        ),
        Fragment(
            line="e29591c3b1e2898bc3b1c3b1c3b17ef091808dc3b17ec2afc3b1c3b17e7e",
            prefix="",
            suffix="f091",
        ),
        Fragment(
            line="7cc3b1c3b1e2898b7ee2898bc3b1e2898b7ee2898b2dc3b1e295b37ee2898b",
            prefix="",
            suffix="e2",
        ),
        Fragment(
            line="e29591c3b17ec3b1c3b1c3b1c3b1e2898b7ec3b1c3b1e2898bf091808d7e7e",
            prefix="",
            suffix="f0",
        ),
        Fragment(
            line="7ce2898bc3b17ee2898bc3b1e2898b7ec3b1c3b17ef091808dc3b17ee2898b",
            prefix="",
            suffix="",
        ),
        Fragment(
            line="e295917e7ef091808d7e7ec3b1e2898be2898b2dc3b1e2898b7ec3b17e",
            prefix="",
            suffix="",
        ),
        Fragment(
            line="7cc3b1e2898bc3b1c3b1c3b1c3b1f091808d2dc2af7e2dc2afe2898be28892",
            prefix="",
            suffix="f0",
        ),
        Fragment(line="e295917ec3b1f091808de2898b7e7e", prefix="", suffix="c2"),
        Fragment(line="7c7ec3b1c3b1e2898be2898b2d", prefix="", suffix="f090b2"),
        Fragment(line="e29591e2898b7ec3b1f091808d2d2d", prefix="", suffix="f0"),
        Fragment(line="7ce2898bc3b1e2898bc2afc2afc2af", prefix="", suffix="c2"),
        Fragment(line="e29591c3b1e2898b2dc2afc2af2d", prefix="", suffix="e288"),
        Fragment(line="7ce2898bc3b1c2afc2afc2afe2898b", prefix="", suffix="e2"),
        Fragment(line="e29591c3b17e7e7ef091808d7ee2898b", prefix="", suffix=""),
        Fragment(line="e2959a2de295902de295902de295902d", prefix="", suffix=""),
    ]
    p2 = [
        Fragment(line="c2afe288922df090b2a32d2dc2a4", prefix="af", suffix="f0"),
        Fragment(line="2d2df090b2a32dc2aff090b2a32e", prefix="a3", suffix="f0"),
        Fragment(line="e288922de288922d2dc2af2d", prefix="90b2a3", suffix="f0"),
        Fragment(line="2df090b2a32dc2afc2af2dc2af", prefix="af", suffix="e288"),
        Fragment(line="2dc3b1c2af7ee2898b7ee2898b", prefix="92", suffix="e289"),
        Fragment(line="e2898b7e7e7ef091808dc3b17e", prefix="898b", suffix="c3"),
        Fragment(line="c3b17e7ee2898bc3b1c3b1e2898b", prefix="", suffix="e289"),
        Fragment(line="e295902de295902de295902de295902d", prefix="", suffix=""),
    ]
    assert merge_paragraphs(p1, p2)


def answer(lines: List[str]):
    lines = lines[:-1]

    parsed_paragraphs = []
    for paragraph in paragraphs(lines):
        parsed_paragraph = []
        for line in paragraph:
            parsed_paragraph.append(parse_fragment(line))
        parsed_paragraphs.append(parsed_paragraph)

    m = parsed_paragraphs[0]
    remaining = parsed_paragraphs
    remaining.remove(m)

    while remaining:
        for p in remaining:
            if merged := merge_paragraphs(p, m):
                m = merged
                remaining.remove(p)
                break
            if merged := merge_paragraphs(m, p):
                m = merged
                remaining.remove(p)
                break
        else:
            print(len(remaining))
            print(paragraph_string(m))
            print("****")
            print(m)
            print("****")
            for p in remaining:
                print("****")
                print(p)
                print(paragraph_string(p))
                print("****")
            assert False, "no match found"
        print(paragraph_string(m))
        print(m)
        # if len(remaining) == 5:
        #     assert False

    print(m)
