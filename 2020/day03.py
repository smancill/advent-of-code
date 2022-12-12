#!/usr/bin/env python

import itertools
import math
from collections.abc import Sequence
from typing import Final, TextIO

SLOPES: Final = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]


def parse_data(f: TextIO) -> list[str]:
    return [l.rstrip() for l in f]


def count_trees(data: Sequence[str], delta: tuple[int, int]) -> int:
    w = len(data[0])
    dx, dy = delta
    # assuming it will exactly end at the last row
    iy = range(0, len(data), dy)
    ix = itertools.count(0, dx)
    return sum(1 for y, x in zip(iy, ix) if data[y][x % w] == "#")


def part1(data: Sequence[str]) -> int:
    return count_trees(data, SLOPES[1])


def part2(data: Sequence[str]) -> int:
    return math.prod(count_trees(data, slope) for slope in SLOPES)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
