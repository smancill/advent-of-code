#!/usr/bin/env python

from collections.abc import Iterator
from itertools import islice
from typing import NamedTuple, TextIO


class Start(NamedTuple):
    a: int
    b: int


def parse_data(f: TextIO) -> Start:
    def parse(ln: str) -> int:
        return int(ln.split()[-1])

    a, b = map(parse, f.readlines())
    return Start(a, b)


def gen_a(start: int, picky: bool = False) -> Iterator[int]:
    factor = 16807
    val = start
    while True:
        val = val * factor % 2147483647
        if picky and val % 4 != 0:
            continue
        yield val


def gen_b(start: int, picky: bool = False) -> Iterator[int]:
    factor = 48271
    val = start
    while True:
        val = val * factor % 2147483647
        if picky and val % 8 != 0:
            continue
        yield val


def duel(start: Start, n: int, picky: bool = False) -> int:
    gen = zip(gen_a(start.a, picky), gen_b(start.b, picky), strict=False)
    return sum(1 for a, b in islice(gen, 0, n) if a & 0xFFFF == b & 0xFFFF)


def part1(start: Start) -> int:
    return duel(start, 40_000_000, picky=False)


def part2(start: Start) -> int:
    return duel(start, 5_000_000, picky=True)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
