#!/usr/bin/env python

from collections.abc import Callable, Sequence
from typing import TextIO

type FuelFn = Callable[[int], int]


def parse_data(f: TextIO) -> list[int]:
    return [int(x) for x in f.read().split(",")]


def find_target(positions: Sequence[int], fuel: FuelFn) -> int:
    def total_fuel(target: int) -> int:
        return sum(fuel(abs(target - x)) for x in positions)

    return min(total_fuel(i) for i in range(min(positions), max(positions) + 1))


def part1(data: Sequence[int]) -> int:
    return find_target(data, lambda d: d)


def part2(data: Sequence[int]) -> int:
    return find_target(data, lambda d: d * (d + 1) // 2)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
