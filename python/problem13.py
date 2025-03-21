from typing import List


def hex_to_bytes(hex_str):
    return bytearray.fromhex(hex_str)


def decode_str(hex_str):
    if hex_str.startswith("feff"):
        yield bytearray.fromhex(hex_str[4:]).decode("utf-16-be")
        return

    if hex_str.startswith("efbbbf"):
        yield bytearray.fromhex(hex_str[6:]).decode("utf-8")
        return

    if hex_str.startswith("fffe"):
        yield bytearray.fromhex(hex_str[4:]).decode("utf-16-le")
        return

    for codec in ["utf-16-le", "utf-8", "utf-16-be", "latin-1"]:
        try:
            yield bytearray.fromhex(hex_str).decode(codec)
        except:
            pass


def test_decode():
    hexes = [
        "616e77c3a4686c65",
        "796c74e46de47373e4",
        "efbbbf73796b6b696dc3a46bc3b6",
        "0070006f00eb0065006d",
        "feff0069007400e4007000e400e4006800e4006e",
        "61757373e46774",
        "626c6173c3a9",
        "637261776cc3a9",
        "6c00e20063006800e2007400",
        "64657370656e68e1",
        "6c6964e172656973",
        "fffe6700e20063006800e9006500",
        "6500700069007400e100660069006f00",
        "feff007300fc006e006400650072006e",
        "fffe7200f600730074006900",
    ]
    for h in hexes:
        print(list(decode_str(h)))
    assert False


def answer(lines: List[str]):
    lines = lines[:-1]
    splitter = -1
    for i, line in enumerate(lines):
        if line == "":
            splitter = i
            break

    line_options = [list(decode_str(l)) for l in lines[0:splitter]]
    words = [l.strip() for l in lines[splitter + 1 :]]

    print(line_options)
    print(words)
    total = 0
    for word in words:
        idx = -1
        for i, ch in enumerate(word):
            if ch != ".":
                idx = i
                break
        if idx == -1:
            raise ValueError("did not find idx")

        found = False
        for i, options in enumerate(line_options):
            for option in options:
                if "Ã" in option:
                    continue

                if len(option) == len(word) and word[idx] == option[idx]:
                    print("match", option, word, i)
                    found = True
                    total += i + 1

            if found:
                break

        if not found:
            assert False, f"No match for {word}"

    print(total)
