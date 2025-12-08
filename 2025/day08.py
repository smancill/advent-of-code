#!/usr/bin/env python

import math
from collections.abc import Iterator, Sequence
from itertools import combinations, islice
from typing import TextIO

type Coord = tuple[int, int, int]
type Circuit = frozenset[int]


def parse_data(f: TextIO) -> list[Coord]:
    def parse(ln: str) -> Coord:
        x, y, z = map(int, ln.strip().split(","))
        return (x, y, z)

    return [parse(ln) for ln in f]


def connect(boxes: Sequence[Coord]) -> Iterator[tuple[int, int, set[Circuit]]]:
    idx = range(len(boxes))

    # get pair of boxes sorted by distance
    pairs = list(combinations(idx, 2))
    pairs = sorted(pairs, key=lambda p: math.dist(boxes[p[0]], boxes[p[1]]))

    # initial circuits of single box
    circuits = {frozenset([i]) for i in idx}

    for i1, i2 in pairs:
        c1 = next(c for c in circuits if i1 in c)
        c2 = next(c for c in circuits if i2 in c)

        if c1 != c2:
            circuits -= {c1, c2}
            circuits |= {c1 | c2}

        yield (i1, i2, circuits)


def part1(boxes: Sequence[Coord], limit: int) -> int:
    circuits = set[Circuit]()
    for _, _, circuits in islice(connect(boxes), limit):  # noqa: B007
        pass
    top = sorted(circuits, key=lambda c: len(c))[-3:]
    return math.prod(map(len, top))


def part2(boxes: Sequence[Coord]) -> int:
    circuits = set[Circuit]()
    for b1, b2, circuits in connect(boxes):
        if len(circuits) == 1:
            return boxes[b1][0] * boxes[b2][0]
    raise AssertionError


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data, 1000)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
