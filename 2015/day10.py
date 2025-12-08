#!/usr/bin/env python

from itertools import groupby
from typing import TextIO


def parse_data(f: TextIO) -> str:
    return f.read().strip()


def look_and_say(sequence: str, iterations: int) -> str:
    for _ in range(iterations):
        sequence = "".join(f"{len(list(g))}{k}" for k, g in groupby(sequence))
    return sequence


def part1(start: str) -> int:
    return len(look_and_say(start, iterations=40))


def part2(start: str) -> int:
    return len(look_and_say(start, iterations=50))


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
