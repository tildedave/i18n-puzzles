from copy import copy
from typing import List


def answer(lines: List[str]):
    crosses = []
    split = -1
    for j in range(0, len(lines)):
        if lines[j] == "":
            split = j
            break

    if split == -1:
        raise Exception("did not find splitter")

    first_part = lines[0:j]
    second_part = lines[j + 1 :]

    crosses = []

    for i, line in enumerate(first_part):
        if (i + 1) % 3 == 0:
            line = line.encode("latin-1").decode("utf-8")
        if (i + 1) % 5 == 0:
            line = line.encode("latin-1").decode("utf-8")
        crosses.append((i, line))

    valids = {}
    for i in range(0, len(second_part)):
        k = second_part[i].strip()
        if k:
            valids[k] = set(crosses)

    while True:
        all_done = True
        next_valids = {}
        for k, possibilities in valids.items():
            idx = -1
            for j in range(0, len(k)):
                if k[j] != ".":
                    idx = j
                    break

            if idx == -1:
                raise Exception("did not find idx")

            if len(possibilities) != 1:
                all_done = False
                next_valids[k] = [
                    t
                    for t in possibilities
                    if len(k) == len(t[1]) and t[1][idx] == k[idx]
                ]
            else:
                next_valids[k] = possibilities

        valids = next_valids
        if all_done:
            break

    total = 0
    for vals in next_valids.values():
        total += vals[0][0] + 1

    print(total)
