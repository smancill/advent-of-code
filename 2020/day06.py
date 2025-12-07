#!/usr/bin/env python

from collections.abc import Sequence, Set
from functools import reduce
from typing import TextIO

type Answers = Set[str]
type Group = Sequence[Answers]


def parse_data(f: TextIO) -> list[Group]:
    def parse_group(g: str) -> Group:
        return [set(p) for p in g.split()]

    return [parse_group(g) for g in f.read().split("\n\n")]


def part1(groups: Sequence[Group]) -> int:
    def n_answers(g: Group) -> int:
        return len(reduce(lambda a, b: a | b, g))

    return sum(n_answers(group) for group in groups)


def part2(groups: Sequence[Group]) -> int:
    def n_answers(g: Group) -> int:
        return len(reduce(lambda a, b: a & b, g))

    return sum(n_answers(group) for group in groups)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
