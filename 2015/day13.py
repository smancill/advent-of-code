#!/usr/bin/env python

import re
from collections import defaultdict
from collections.abc import Sequence
from itertools import permutations
from typing import TextIO

type Happiness = dict[str, dict[str, int]]


def parse_data(f: TextIO) -> Happiness:
    def parse_line(line: str) -> tuple[str, str, int]:
        if m := re.match(r"(\w+) would (gain|lose) (\d+) .* (\w+)\.", line):
            a, v, u, b = m.groups()
            u = int(u) if v == "gain" else -int(u)
            return a, b, u
        raise ValueError(line)

    happiness: Happiness = defaultdict(dict)
    for l in f:
        a, b, u = parse_line(l)
        happiness[a][b] = u
    return happiness


def optimal_happiness(happiness: Happiness) -> int:
    def total_happiness(seats: Sequence[str]) -> int:
        def change(i: int) -> int:
            p, a, b = seats[i], seats[(i - 1) % n], seats[(i + 1) % n]
            return happiness[p][a] + happiness[p][b]

        n = len(seats)
        return sum(change(i) for i in range(n))

    return max(total_happiness(seats) for seats in permutations(happiness))


def part1(data: Happiness) -> int:
    return optimal_happiness(data)


def part2(data: Happiness) -> int:
    data = {"me": {k: 0 for k in data}} | {k: v | {"me": 0} for k, v in data.items()}
    return optimal_happiness(data)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
