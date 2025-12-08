#!/usr/bin/env python

from itertools import combinations
from typing import TextIO

Matrix = list[list[int]]


def parse_data(f: TextIO) -> Matrix:
    return [[int(v) for v in l.split()] for l in f]


def part1(m: Matrix) -> int:
    return sum(max(r) - min(r) for r in m)


def part2(m: Matrix) -> int:
    return sum(
        x // y
        for r in m
        for x, y in combinations(sorted(r, reverse=True), 2)
        if x % y == 0
    )


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
