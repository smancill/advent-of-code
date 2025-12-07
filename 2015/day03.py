#!/usr/bin/env python

from collections.abc import Iterable
from itertools import islice
from typing import TextIO


def parse_data(f: TextIO) -> str:
    return f.read().rstrip()


def deliver(moves: Iterable[str]) -> set[complex]:
    current = complex(0)
    visited = {current}
    for m in moves:
        match m:
            case "<":
                current -= 1
            case ">":
                current += 1
            case "^":
                current -= 1j
            case "v":
                current += 1j
            case _:
                raise AssertionError
        visited.add(current)
    return visited


def part1(data: str) -> int:
    santa = deliver(data)
    return len(santa)


def part2(data: str) -> int:
    santa = deliver(islice(data, 0, None, 2))
    robot = deliver(islice(data, 1, None, 2))
    return len(santa | robot)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
