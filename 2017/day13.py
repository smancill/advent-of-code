#!/usr/bin/env python

from itertools import count
from typing import NamedTuple, TextIO


class Layer(NamedTuple):
    depth: int
    scanner_range: int
    scanner_period: int


def parse_data(f: TextIO) -> list[Layer]:
    def layer(ln: str) -> Layer:
        d, r = map(int, ln.split(":"))
        return Layer(d, r, 2 * (r - 1))

    return [layer(r) for r in f.readlines()]


def part1(layers: list[Layer]) -> int:
    return sum(d * r for d, r, T in layers if d % T == 0)


def part2(layers: list[Layer]) -> int:
    for delay in count():
        for d, _, T in layers:  # noqa: N806
            if (delay + d) % T == 0:
                break
        else:
            return delay
    raise AssertionError


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
