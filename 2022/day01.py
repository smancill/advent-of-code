#!/usr/bin/env python

from collections.abc import Sequence
from itertools import islice
from typing import TextIO, TypeAlias

Calories: TypeAlias = list[int]


def parse_data(f: TextIO) -> list[Calories]:
    def parse_calories(elf: str) -> Calories:
        return [int(c) for c in elf.split()]

    return [parse_calories(e) for e in f.read().split("\n\n")]


def part1(data: Sequence[Calories]) -> int:
    return sum(max(data, key=sum))


def part2(data: Sequence[Calories], n: int = 3) -> int:
    sd = sorted(data, key=sum, reverse=True)
    return sum([sum(c) for c in islice(sd, n)])


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
