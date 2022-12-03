#!/usr/bin/env python

from collections.abc import Sequence
from typing import TextIO


def parse_data(f: TextIO) -> list[str]:
    return [l.rstrip() for l in f]


def _priority(item: str) -> int:
    o = ord(item)
    if 65 <= o <= 90:
        return o - 38
    if 97 <= o <= 122:
        return o - 96
    raise ValueError()


def part1(rucksacks: Sequence[str]) -> int:
    def compartments(r: str) -> list[str]:
        h = len(r) // 2
        return [r[:h], r[h:]]

    def items(r: str) -> list[set[str]]:
        return [set(c) for c in compartments(r)]

    def missplaced(r: str) -> str:
        (item,) = set.intersection(*items(r))
        return item

    return sum(_priority(missplaced(r)) for r in rucksacks)


def part2(rucksacks: Sequence[str], group_size: int = 3) -> int:
    def items(group: Sequence[str]) -> list[set[str]]:
        return [set(g) for g in group]

    def badge(group: Sequence[str]) -> str:
        (badge,) = set.intersection(*items(group))
        return badge

    return sum(
        _priority(badge(rucksacks[i : i + group_size]))
        for i in range(0, len(rucksacks), group_size)
    )


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
