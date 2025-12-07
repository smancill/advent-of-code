#!/usr/bin/env python

from collections.abc import Sequence
from dataclasses import dataclass
from typing import TextIO


@dataclass(frozen=True)
class Dimensions:
    width: int
    height: int
    length: int


def parse_data(f: TextIO) -> list[Dimensions]:
    def parse_dimensions(line: str) -> Dimensions:
        w, h, l = map(int, line.split("x"))
        return Dimensions(w, h, l)

    return [parse_dimensions(l) for l in f]


def _sides(d: Dimensions) -> list[tuple[int, int]]:
    return [(d.width, d.length), (d.width, d.height), (d.height, d.length)]


def paper_size(d: Dimensions) -> int:
    sides = [a * b for a, b in _sides(d)]
    extra = min(sides)
    return sum(2 * s for s in sides) + extra


def ribbon_size(d: Dimensions) -> int:
    ribbon = min(2 * (a + b) for a, b in _sides(d))
    bow = d.width * d.height * d.length
    return ribbon + bow


def part1(data: Sequence[Dimensions]) -> int:
    return sum(paper_size(d) for d in data)


def part2(data: Sequence[Dimensions]) -> int:
    return sum(ribbon_size(d) for d in data)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
