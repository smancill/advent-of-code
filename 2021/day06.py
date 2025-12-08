#!/usr/bin/env python

from collections import deque
from collections.abc import Sequence
from typing import TextIO

DAYS_CYCLE = 7
FIRST_CYCLE = DAYS_CYCLE + 2


def parse_data(f: TextIO) -> list[int]:
    return [int(l) for l in f.read().split(",")]


def population(cycles: Sequence[int], days: int) -> int:
    fish = deque(cycles.count(i) for i in range(FIRST_CYCLE))
    for _ in range(days):
        fish.rotate(-1)
        fish[DAYS_CYCLE - 1] += fish[-1]
    return sum(fish)


def part1(data: Sequence[int]) -> int:
    return population(data, 80)


def part2(data: Sequence[int]) -> int:
    return population(data, 256)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
