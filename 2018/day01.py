#!/usr/bin/env python

from collections.abc import Sequence
from itertools import accumulate, cycle
from typing import TextIO


def parse_data(f: TextIO) -> list[int]:
    return [int(l) for l in f]


def part1(changes: Sequence[int]) -> int:
    return sum(changes)


def part2(changes: Sequence[int]) -> int:
    freqs = {0}
    for f in accumulate(cycle(changes)):
        if f in freqs:
            return f
        freqs.add(f)
    raise AssertionError


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
