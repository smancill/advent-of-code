#!/usr/bin/env python

import itertools
import math
from collections.abc import Sequence
from typing import TextIO


def parse_data(f: TextIO) -> list[int]:
    return [int(l) for l in f]


def find_entries(numbers: Sequence[int], size: int) -> int:
    for entries in itertools.combinations(numbers, size):
        if sum(entries) == 2020:
            return math.prod(entries)
    assert False


def part1(data: Sequence[int]) -> int:
    return find_entries(data, 2)


def part2(data: Sequence[int]) -> int:
    return find_entries(data, 3)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
