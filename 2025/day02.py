#!/usr/bin/env python

import re
from collections.abc import Iterator, Sequence
from typing import TextIO


def parse_data(f: TextIO) -> list[range]:
    def parse_range(ln: str) -> range:
        s, e = map(int, ln.split("-"))
        return range(s, e + 1)

    data = f.read().strip().split(",")
    return [parse_range(r) for r in data]


def invalid(id_ranges: Sequence[range], pattern: re.Pattern[str]) -> Iterator[int]:
    for r in id_ranges:
        for i in r:
            if pattern.match(str(i)):
                yield i


def part1(id_ranges: Sequence[range]) -> int:
    pattern = re.compile(r"^(\d+)\1$")
    return sum(invalid(id_ranges, pattern))


def part2(id_ranges: Sequence[range]) -> int:
    pattern = re.compile(r"^(\d+)(\1)+$")
    return sum(invalid(id_ranges, pattern))


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
