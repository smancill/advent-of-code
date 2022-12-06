#!/usr/bin/env python

import re
from string import ascii_lowercase
from typing import TextIO


def parse_data(f: TextIO) -> str:
    return f.read().rstrip()


def react(polymer: str) -> int:
    result: list[str] = []
    for unit in polymer:
        if result:
            a = ord(unit)
            b = ord(result[-1])
            if a - 32 == b or a + 32 == b:
                result.pop()
                continue
        result.append(unit)
    return len(result)


def remove_units(polymer: str) -> list[str]:
    return [re.sub(c, "", polymer, flags=re.I) for c in ascii_lowercase]


def part1(polymer: str) -> int:
    return react(polymer)


def part2(polymer: str) -> int:
    return min(react(p) for p in remove_units(polymer))


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
