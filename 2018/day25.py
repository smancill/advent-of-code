#!/usr/bin/env python

import re
from collections.abc import Sequence
from typing import Final, TextIO

type Coord = tuple[int, int, int, int]
type Constellation = set[Coord]

MAX_DIST: Final = 3


def parse_data(f: TextIO) -> list[Coord]:
    def parse_coord(line: str) -> Coord:
        x, y, z, t = map(int, re.findall(r"-?\d+", line))
        return (x, y, z, t)

    return [parse_coord(l) for l in f]


def _dist(c1: Coord, c2: Coord) -> int:
    return sum(abs(i1 - i2) for i1, i2 in zip(c1, c2, strict=True))


def find_constellation(orig: Coord, points: Sequence[Coord]) -> Constellation:
    group = set()
    queue = {orig}
    while queue:
        current = queue.pop()
        group.add(current)
        near = [p for p in points if _dist(p, current) <= MAX_DIST and p not in group]
        queue.update(near)
    return group


def find_constelations(points: Sequence[Coord]) -> list[Constellation]:
    constelations = []
    queue = set(points)
    while queue:
        orig = queue.pop()
        const = find_constellation(orig, points)
        queue -= const
        constelations.append(const)
    return constelations


def part1(points: Sequence[Coord]) -> int:
    constelations = find_constelations(points)
    return len(constelations)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")


if __name__ == "__main__":
    main()
