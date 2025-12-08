#!/usr/bin/env python

import re
from collections import defaultdict
from collections.abc import Iterator, Sequence
from typing import TextIO

type Coord = tuple[int, int]
type Diagram = dict[Coord, int]


class Vent:
    x1: int
    y1: int
    x2: int
    y2: int

    def __init__(self, line: str):
        self.x1, self.y1, self.x2, self.y2 = map(int, re.findall(r"-?\d+", line))

    def points(self) -> Iterator[Coord]:
        def step(delta: int) -> int:
            if delta == 0:
                return 0
            if delta > 0:
                return 1
            return -1

        dx, dy = self.x2 - self.x1, self.y2 - self.y1
        sx, sy = step(dx), step(dy)
        np = max(abs(dx), abs(dy)) + 1
        x, y = self.x1, self.y1
        for _ in range(np):
            yield (x, y)
            x, y = x + sx, y + sy

    def __str__(self) -> str:
        return f"{self.x1},{self.y1} -> {self.x2},{self.y2}"


def parse_data(f: TextIO) -> list[Vent]:
    return [Vent(ln) for ln in f]


def count_overlaps(diagram: Diagram, min_vents: int = 2) -> int:
    return sum(1 for v in diagram.values() if v >= min_vents)


def show_vents(diagram: Diagram) -> None:
    mx = max(x for x, _ in diagram)
    my = max(y for _, y in diagram)
    for y in range(my + 1):
        for x in range(mx + 1):
            n = diagram[x, y]
            c = n if n > 0 else "."
            print(c, end="")
        print()


def part1(vents: Sequence[Vent]) -> int:
    diagram = defaultdict[Coord, int](int)
    for vent in vents:
        if vent.x1 == vent.x2 or vent.y1 == vent.y2:
            for x, y in vent.points():
                diagram[x, y] += 1
    return count_overlaps(diagram)


def part2(vents: Sequence[Vent]) -> int:
    diagram = defaultdict[Coord, int](int)
    for vent in vents:
        for x, y in vent.points():
            diagram[(x, y)] += 1
    return count_overlaps(diagram)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
