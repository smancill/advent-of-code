#!/usr/bin/env python

from collections import Counter
from collections.abc import Sequence
from itertools import combinations
from typing import TextIO


def parse_data(f: TextIO) -> list[str]:
    return [l.rstrip() for l in f]


def part1(box_ids: Sequence[str]) -> int:
    with2 = 0
    with3 = 0
    for box_id in box_ids:
        freqs = Counter(box_id)
        if 2 in freqs.values():
            with2 += 1
        if 3 in freqs.values():
            with3 += 1
    return with2 * with3


def part2(box_ids: Sequence[str]) -> str:
    for x, y in combinations(box_ids, 2):
        common = [a for a, b in zip(x, y) if a == b]
        if len(common) == len(x) - 1:
            return "".join(common)
    assert False


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
