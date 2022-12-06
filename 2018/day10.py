#!/usr/bin/env python

import re
from collections.abc import Sequence
from dataclasses import dataclass
from itertools import count
from typing import Final, TextIO


@dataclass
class Point:
    x: int
    y: int
    vx: Final[int]
    vy: Final[int]

    def move(self) -> None:
        self.x += self.vx
        self.y += self.vy


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
