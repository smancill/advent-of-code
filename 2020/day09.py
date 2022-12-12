#!/usr/bin/env python

from collections.abc import Sequence
from itertools import combinations, filterfalse
from typing import Final, TextIO

PREAMBLE: Final = 25


def parse_data(f: TextIO) -> list[int]:
    return [int(l) for l in f]


def part1(data: Sequence[int], preamble: int = PREAMBLE) -> int:
    def is_valid(i: int) -> bool:
        start, end = i - preamble, i
        return any(a + b == data[i] for a, b in combinations(data[start:end], 2))

    i = next(filterfalse(is_valid, range(preamble, len(data))))
    return data[i]


def part2(data: Sequence[int], preamble: int = PREAMBLE) -> int:
    inv = part1(data, preamble)
    for i in range(len(data)):
        j = i + 1
        sum = data[i]
        while True:
            sum += data[j]
            if sum == inv:
                sub = data[i : j + 1]
                return min(sub) + max(sub)
            elif sum > inv:
                break
            else:
                j += 1

    assert False


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
