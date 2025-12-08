#!/usr/bin/env python

from collections.abc import Sequence
from typing import TextIO


def parse_data(f: TextIO) -> list[int]:
    return [int(ln) for ln in f]


def count_increases(values: Sequence[int], window_size: int) -> int:
    # (a + b + c) < (b + c + d) <=> a < d
    return sum(x < y for x, y in zip(values, values[window_size:], strict=False))


def part1(data: Sequence[int]) -> int:
    return count_increases(data, 1)


def part2(data: Sequence[int]) -> int:
    return count_increases(data, 3)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
