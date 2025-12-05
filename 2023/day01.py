#!/usr/bin/env python

import re
from collections.abc import Sequence
from typing import TextIO


def parse_data(f: TextIO) -> list[str]:
    return f.readlines()


def part1(data: Sequence[str]) -> int:
    def get_number(s: str) -> int:
        m = re.findall(r"\d", s)
        assert m
        a, b = int(m[0]), int(m[-1])
        return 10 * a + b

    return sum(get_number(s) for s in data)


def part2(data: Sequence[str]) -> int:
    def get_digit(d: str) -> int:
        match d:
            case "one":
                return 1
            case "two":
                return 2
            case "three":
                return 3
            case "four":
                return 4
            case "five":
                return 5
            case "six":
                return 6
            case "seven":
                return 7
            case "eight":
                return 8
            case "nine":
                return 9
            case _:
                return int(d)

    def get_number(s: str) -> int:
        m = re.findall(r"(?=(one|two|three|four|five|six|seven|eight|nine|\d))", s)
        assert m
        a, b = get_digit(m[0]), get_digit(m[-1])
        return 10 * a + b

    return sum(get_number(s) for s in data)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
