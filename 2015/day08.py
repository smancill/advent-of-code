#!/usr/bin/env python

import re
from collections.abc import Sequence
from typing import TextIO


def parse_data(f: TextIO) -> list[str]:
    return [l.rstrip() for l in f]


def decode(s: str) -> str:
    return s[1:-1].encode("raw_unicode_escape").decode("unicode-escape")


def encode(s: str) -> str:
    s = re.sub(r"\\|\"", r"\\\0", s)
    return f'"{s}"'


def part1(data: Sequence[str]) -> int:
    return sum(len(s) - len(decode(s)) for s in data)


def part2(data: Sequence[str]) -> int:
    return sum(len(encode(s)) - len(s) for s in data)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
