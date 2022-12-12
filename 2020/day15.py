#!/usr/bin/env python

from collections.abc import Sequence
from typing import TextIO


def parse_data(f: TextIO) -> list[int]:
    return [int(i) for i in f.read().split(",")]


def find_number(starting: Sequence[int], turns: int) -> int:
    prev = {n: i + 1 for i, n in enumerate(starting)}
    last = starting[-1]
    for i in range(len(starting), turns):
        prev[last], last = i, (i - prev[last] if last in prev else 0)
    return last


def part1(data: Sequence[int]) -> int:
    return find_number(data, 2020)


def part2(data: Sequence[int]) -> int:
    return find_number(data, 30_000_000)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
