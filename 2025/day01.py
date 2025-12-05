#!/usr/bin/env python

from collections.abc import Sequence
from typing import Final, NamedTuple, TextIO

TOTAL: Final = 100


class Rotation(NamedTuple):
    turn: str
    dist: int


def parse_data(f: TextIO) -> list[Rotation]:
    return [Rotation(ln[0], int(ln[1:])) for ln in f]


def part1(rotations: Sequence[Rotation]) -> int:
    count = 0
    dial = 50
    for r in rotations:
        match r.turn:
            case "R":
                dial += r.dist
            case "L":
                dial -= r.dist
        dial %= TOTAL
        if dial == 0:
            count += 1
    return count


def part2(rotations: Sequence[Rotation]) -> int:
    count = 0
    dial = 50
    for r in rotations:
        full, dist = divmod(r.dist, TOTAL)
        count += full
        match r.turn:
            case "R":
                dial += dist
                if dial >= TOTAL:
                    count += 1
            case "L":
                dial -= dist
                if -dist < dial <= 0:
                    count += 1
        dial %= TOTAL
    return count


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
