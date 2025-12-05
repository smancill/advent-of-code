#!/usr/bin/env python

from collections.abc import Sequence
from typing import TextIO


def parse_data(f: TextIO) -> list[str]:
    return [ln.strip() for ln in f]


def part1(banks: Sequence[str]) -> int:
    def joltage(bank: str) -> int:
        b1 = max(bank[:-1])
        i1 = bank.find(b1) + 1
        b2 = max(bank[i1:])
        return 10 * int(b1) + int(b2)

    return sum(joltage(b) for b in banks)


def part2(banks: Sequence[str]) -> int:
    def joltage(bank: str, n: int) -> int:
        j = 0
        i = 0
        e = len(bank) - n + 1
        for _ in range(n):
            b = max(bank[i:e])
            i = bank.find(b, i) + 1
            e = e + 1
            j = 10 * j + int(b)
        return j

    return sum(joltage(b, 12) for b in banks)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
