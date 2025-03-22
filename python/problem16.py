from typing import List
from enum import Enum
import functools

extended_chars = "ÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜ¢£¥₧ƒáíóúñÑªº¿⌐¬½¼¡«»░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀αßΓπΣσµτΦΘΩδ∞φε∩≡±≥≤⌠⌡÷≈°∙·√ⁿ²■"

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
DOUBLE_UP = 5
DOUBLE_DOWN = 6
DOUBLE_LEFT = 7
DOUBLE_RIGHT = 8

directions = {
    "│": {UP, DOWN},
    "┤": {UP, DOWN, LEFT},
    "╡": {UP, DOWN, DOUBLE_LEFT},
    "╢": {LEFT, DOUBLE_UP, DOUBLE_DOWN},
    "╖": {LEFT, DOUBLE_DOWN},
    "╕": {DOUBLE_LEFT, DOWN},
    "╣": {DOUBLE_UP, DOUBLE_DOWN, DOUBLE_LEFT},
    "║": {DOUBLE_UP, DOUBLE_DOWN},
    "╗": {DOUBLE_LEFT, DOUBLE_DOWN},
    "╝": {DOUBLE_LEFT, DOUBLE_UP},
    "╜": {DOUBLE_UP, LEFT},
    "╛": {DOUBLE_LEFT, UP},
    "┐": {LEFT, DOWN},
    "└": {UP, RIGHT},
    "┴": {LEFT, RIGHT, UP},
    "┬": {LEFT, RIGHT, DOWN},
    "├": {UP, DOWN, RIGHT},
    "─": {LEFT, RIGHT},
    "┼": {LEFT, RIGHT, UP, DOWN},
    "╞": {UP, DOWN, DOUBLE_RIGHT},
    "╟": {DOUBLE_UP, DOUBLE_DOWN, RIGHT},
    "╚": {DOUBLE_UP, DOUBLE_RIGHT},
    "╔": {DOUBLE_DOWN, DOUBLE_RIGHT},
    "╩": {DOUBLE_LEFT, DOUBLE_RIGHT, DOUBLE_UP},
    "╦": {DOUBLE_LEFT, DOUBLE_RIGHT, DOUBLE_DOWN},
    "╠": {DOUBLE_UP, DOUBLE_DOWN, DOUBLE_RIGHT},
    "═": {DOUBLE_LEFT, DOUBLE_RIGHT},
    "╬": {DOUBLE_LEFT, DOUBLE_RIGHT, DOUBLE_UP, DOUBLE_DOWN},
    "╧": {DOUBLE_RIGHT, DOUBLE_LEFT, UP},
    "╨": {LEFT, RIGHT, DOUBLE_UP},
    "╤": {DOUBLE_LEFT, DOUBLE_RIGHT, DOWN},
    "╥": {DOUBLE_DOWN, LEFT, RIGHT},
    "╙": {DOUBLE_UP, RIGHT},
    "╘": {DOUBLE_RIGHT, UP},
    "╒": {DOWN, DOUBLE_RIGHT},
    "╓": {DOUBLE_DOWN, RIGHT},
    "╫": {DOUBLE_UP, DOUBLE_DOWN, LEFT, RIGHT},
    "╪": {DOUBLE_LEFT, DOUBLE_RIGHT, UP, DOWN},
    "┘": {LEFT, UP},
    "┌": {RIGHT, DOWN},
}

expanded_direction = {
    UP: {UP, DOUBLE_UP},
    DOWN: {DOWN, DOUBLE_DOWN},
    LEFT: {LEFT, DOUBLE_LEFT},
    RIGHT: {RIGHT, DOUBLE_RIGHT},
}


@functools.lru_cache
def rotate_char_right(ch: str):
    new_direction = set()
    for dir in directions[ch]:
        new_direction.add(rotate_right(dir))

    for k, d in directions.items():
        if d == new_direction:
            return k

    raise ValueError("did not match")


@functools.lru_cache
def rotate_char_left(ch: str):
    new_direction = set()
    for dir in directions[ch]:
        new_direction.add(rotate_left(dir))

    for k, d in directions.items():
        if d == new_direction:
            return k

    raise ValueError("did not match")


def test_rotate_left():
    assert rotate_char_left("╒") == "╙"


def test_rotate_right():
    assert rotate_char_right("┘") == "└"
    assert rotate_char_right("└") == "┌"
    assert rotate_char_right("┌") == "┐"
    assert rotate_char_right("┐") == "┘"


def rotate_right(direction):
    if direction == LEFT:
        return UP
    if direction == DOUBLE_LEFT:
        return DOUBLE_UP
    if direction == UP:
        return RIGHT
    if direction == DOUBLE_UP:
        return DOUBLE_RIGHT
    if direction == RIGHT:
        return DOWN
    if direction == DOUBLE_RIGHT:
        return DOUBLE_DOWN
    if direction == DOWN:
        return LEFT
    if direction == DOUBLE_DOWN:
        return DOUBLE_LEFT
    assert False, "invalid rotate_right input"


def rotate_left(direction):
    if direction == LEFT:
        return DOWN
    if direction == DOUBLE_LEFT:
        return DOUBLE_DOWN
    if direction == UP:
        return LEFT
    if direction == DOUBLE_UP:
        return DOUBLE_LEFT
    if direction == RIGHT:
        return UP
    if direction == DOUBLE_RIGHT:
        return DOUBLE_UP
    if direction == DOWN:
        return RIGHT
    if direction == DOUBLE_DOWN:
        return DOUBLE_RIGHT


def reverse_direction(direction):
    if direction == LEFT:
        return RIGHT
    if direction == DOUBLE_LEFT:
        return DOUBLE_RIGHT
    if direction == UP:
        return DOWN
    if direction == DOUBLE_UP:
        return DOUBLE_DOWN
    if direction == RIGHT:
        return LEFT
    if direction == DOUBLE_RIGHT:
        return DOUBLE_LEFT
    if direction == DOWN:
        return UP
    if direction == DOUBLE_DOWN:
        return DOUBLE_UP
    assert False, "invalid reverse_direction input"


def walk(max_x: int, max_y: int):
    delta = 0
    # This double-emits corners but getting the +/- in place is pretty annoying
    # so we'll skip it
    while True:
        seen = False
        for x in range(delta, max_x - delta):
            seen = True
            yield (x, delta)

        for y in range(delta + 1, max_y - delta):
            seen = True
            yield (max_x - delta - 1, y)

        for x in range(max_x - delta - 1, delta - 1, -1):
            seen = True
            yield (x, max_y - delta - 1)

        for y in range(max_y - delta - 1, delta - 1, -1):
            seen = True
            yield (delta, y)

        delta += 1
        if not seen:
            break


def walk_direction(x, y, direction):
    if direction in {UP, DOUBLE_UP}:
        return (x, y - 1)
    if direction in {DOWN, DOUBLE_DOWN}:
        return (x, y + 1)
    if direction in {LEFT, DOUBLE_LEFT}:
        return (x - 1, y)
    if direction in {RIGHT, DOUBLE_RIGHT}:
        return (x + 1, y)
    assert False, "invalid walk_direction input"


def direction_to_string(d: int):
    if d == UP:
        return "UP"
    if d == DOWN:
        return "DOWN"
    if d == LEFT:
        return "LEFT"
    if d == RIGHT:
        return "RIGHT"
    assert False


def answer(lines: List[str]):
    lines = lines[:-1]

    if len(lines) > 10:
        lines = lines[5 : len(lines) - 6]
        lines = [l[7 : len(l) - 7] for l in lines]

    # We'll assume it's trimmed already; for real input we'll have to do this
    # (probably via hardcoded indices)
    rows = []
    for line in lines:
        row = []
        for ch in line:
            i = ord(ch)
            if i < 128:
                row.append(ch)
            else:
                row.append(extended_chars[i - 128])
        rows.append(row)

    for row in rows:
        print("".join(row))

    # go around the edges first, work our way inside
    max_x = len(row)
    max_y = len(rows)

    def in_bounds(x, y):
        return 0 <= x < max_x and 0 <= y < max_y

    def matches(ch, x, y, direction):
        # IF it doesn't point in that direction, no problems.  the way we walk
        # the squares means we lock everything in a spiral from the outside
        # going in
        print("\tchecking matches", ch, x, y, direction_to_string(direction))
        nx, ny = walk_direction(x, y, direction)

        if nx == 0 and ny == -1 and direction == UP:
            print("\tspecial case - starting point")
            return True
        elif nx == max_x - 1 and y == max_y - 1 and direction == DOWN:
            print("\tspecial case - ending point")
            return True

        s: set[int] = expanded_direction[direction]
        points_in_that_direction = s.intersection(directions[ch])
        if not points_in_that_direction:
            print("\tdoes not point in direction", direction)
            return True

        if not in_bounds(nx, ny):
            return False

        adjacent_ch = rows[ny][nx]
        needed = reverse_direction(next(iter(points_in_that_direction)))
        return needed in directions.get(adjacent_ch, set())

    total_rotations = 0
    locked_points = set()

    for x, y in walk(max_x, max_y):
        # As we walk we need to rotate the char to match the locked_dirs
        # We need the character at rows[y][x] to match EVERY locked_dir, both
        # directions
        ch = rows[y][x]
        if ch not in directions:
            # Nothing to do
            locked_points.add((x, y))
            continue

        num_rotations = 0
        while num_rotations < 4:
            print("ch now", ch)

            all_match = True
            for dir in {UP, LEFT, RIGHT, DOWN}:
                nx, ny = walk_direction(x, y, dir)

                if in_bounds(nx, ny) and (nx, ny) not in locked_points:
                    continue

                print(f"{direction_to_string(dir)} locked, checking it")
                matches_dir = matches(ch, x, y, dir)

                if not in_bounds(nx, ny):
                    matches_from_reverse_dir = True
                elif rows[ny][nx] not in directions:
                    matches_from_reverse_dir = True
                else:
                    rev_dir = reverse_direction(dir)
                    matches_from_reverse_dir = matches(rows[ny][nx], nx, ny, rev_dir)

                if matches_dir and matches_from_reverse_dir:
                    print(f"{direction_to_string(dir)} does match")
                else:
                    print(
                        f"{direction_to_string(dir)} does not match",
                        matches_dir,
                        matches_from_reverse_dir,
                    )
                    all_match = False
                    break

            if all_match:
                break

            prev_ch = ch
            rows[y][x] = rotate_char_right(ch)
            ch = rows[y][x]
            print(prev_ch, "rotated to", ch)
            num_rotations += 1
        else:
            raise ValueError("no rotation satisfying")

        total_rotations += num_rotations
        locked_points.add((x, y))

        for _y, row in enumerate(rows):
            for _x, ch in enumerate(row):
                if x == _x and y == _y:
                    print(f"\x1b[1;37;41m{rows[_y][_x]}\x1b[0m", end="")
                else:
                    print(rows[_y][_x], end="")
            print()
        print(total_rotations)
