#!/usr/bin/env python

from collections.abc import Iterator
from itertools import accumulate
from typing import TextIO


def parse_data(f: TextIO) -> str:
    return f.read().strip()


def floors(directions: str) -> Iterator[int]:
    return accumulate(1 if d == "(" else -1 for d in directions)


def part1(data: str) -> int:
    *_, last = floors(data)
    return last


def part2(data: str) -> int:
    return next(i for i, f in enumerate(floors(data), 1) if f == -1)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
