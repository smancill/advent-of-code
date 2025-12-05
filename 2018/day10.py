#!/usr/bin/env python

import re
from collections.abc import Sequence
from itertools import count
from typing import Final, TextIO


class Point:
    _x: int
    _y: int
    _vx: Final[int]
    _vy: Final[int]

    def __init__(self, x: int, y: int, vx: int, vy: int) -> None:
        self._x = x
        self._y = y
        self._vx = vx
        self._vy = vy

    def move(self) -> None:
        self._x += self._vx
        self._y += self._vy

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y


def parse_data(f: TextIO) -> list[Point]:
    def parse_point(line: str) -> Point:
        values = re.findall(r"-?\d+", line)
        return Point(*map(int, values))

    return [parse_point(l) for l in f]


def show_message(points: Sequence[Point], h: int = 10) -> None:
    for t in count(1):
        for p in points:
            p.move()

        x0, x1 = min(p.x for p in points), max(p.x for p in points)
        y0, y1 = min(p.y for p in points), max(p.y for p in points)

        # heuristic: message should fit in a small bounding box
        # minimum height found after running the program a few times
        if y1 - y0 <= h:
            grid = {(p.x, p.y): "#" for p in points}
            print(f"After {t} seconds:")
            for j in range(y0, y1 + 1):
                for i in range(x0, x1 + 1):
                    print(grid.get((i, j), " "), end="")
                print()
            break


def main() -> None:
    data = parse_data(open(0))

    show_message(data)


if __name__ == "__main__":
    main()
