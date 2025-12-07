#!/usr/bin/env python

import re
from collections.abc import Sequence
from typing import TextIO


def parse_data(f: TextIO) -> list[str]:
    return [l.strip() for l in f]


def part1(data: Sequence[str]) -> int:
    def nice(s: str) -> bool:
        return (
            re.search(r"(.*[aeiou]){3,}", s) is not None
            and re.search(r"(.)\1", s) is not None
            and re.search(r"ab|cd|pq|xy", s) is None
        )

    return sum(nice(s) for s in data)


def part2(data: Sequence[str]) -> int:
    def nice(s: str) -> bool:
        return (
            re.search(r"(..).*\1", s) is not None
            and re.search(r"(.).\1", s) is not None
        )

    return sum(nice(s) for s in data)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
