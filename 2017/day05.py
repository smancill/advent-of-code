#!/usr/bin/env python

from collections.abc import Callable
from typing import NamedTuple, TextIO


class Exit(NamedTuple):
    steps: int
    jumps: list[int]


def parse_data(f: TextIO) -> list[int]:
    return [int(l) for l in f.readlines()]


def run(jumps: list[int], inc: Callable[[int], int]) -> Exit:
    jumps = jumps[:]
    size = len(jumps)
    pointer = 0
    steps = 0
    while True:
        offset = jumps[pointer]
        jumps[pointer] += inc(offset)
        steps += 1
        pointer += offset
        if pointer < 0 or pointer >= size:
            break
    return Exit(steps, jumps)


def part1(jumps: list[int]) -> Exit:
    return run(jumps, lambda _: 1)


def part2(jumps: list[int]) -> Exit:
    return run(jumps, lambda i: -1 if i >= 3 else 1)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data).steps}")
    print(f"P2: {part2(data).steps}")


if __name__ == "__main__":
    main()
