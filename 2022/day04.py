#!/usr/bin/env python

from collections.abc import Sequence
from dataclasses import dataclass
from typing import TextIO


@dataclass(frozen=True)
class Pair:
    elf1: range
    elf2: range


def parse_data(f: TextIO) -> list[Pair]:
    def parse_range(r: str) -> range:
        b, e = map(int, r.split("-"))
        return range(b, e + 1)

    def parse_pair(line: str) -> Pair:
        r1, r2 = [parse_range(r) for r in line.split(",")]
        return Pair(r1, r2)

    return [parse_pair(l) for l in f]


def part1(pairs: Sequence[Pair]) -> int:
    def overlap(p: Pair) -> bool:
        return (p.elf1[0] <= p.elf2[0] and p.elf2[-1] <= p.elf1[-1]) or (
            p.elf2[0] <= p.elf1[0] and p.elf1[-1] <= p.elf2[-1]
        )

    return sum(1 for p in pairs if overlap(p))


def part2(pairs: Sequence[Pair]) -> int:
    def overlap(p: Pair) -> bool:
        return p.elf1[0] <= p.elf2[-1] and p.elf2[0] <= p.elf1[-1]

    return sum(1 for p in pairs if overlap(p))


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
