#!/usr/bin/env python

from collections import deque
from collections.abc import Sequence
from copy import deepcopy
from typing import TextIO

Stacks = dict[int, deque[str]]
Move = tuple[int, int, int]


def parse_data(f: TextIO) -> tuple[Stacks, list[Move]]:
    def parse_initial(starting: Sequence[str]) -> Stacks:
        *crates, ids = starting
        cols = {int(c): i for i, c in enumerate(ids) if c != " "}
        stacks: Stacks = {}
        for l in reversed(crates):
            for s, i in cols.items():
                if i < len(l) and l[i] != " ":
                    stacks.setdefault(s, deque()).append(l[i])
        return stacks

    def parse_move(line: str) -> Move:
        tokens = line.split()
        n, s, t = tokens[1], tokens[3], tokens[5]
        return int(n), int(s), int(t)

    starting, procedure = [s.splitlines() for s in f.read().split("\n\n")]

    stacks = parse_initial(starting)
    moves = [parse_move(l) for l in procedure]
    return stacks, moves


def part1(stacks: Stacks, moves: Sequence[Move]) -> str:
    stacks = deepcopy(stacks)
    for n, source, target in moves:
        crates = list(stacks[source].pop() for _ in range(n))
        stacks[target].extend(crates)
    return "".join(s[-1] for s in stacks.values())


def part2(stacks: Stacks, moves: Sequence[Move]) -> str:
    stacks = deepcopy(stacks)
    for n, source, target in moves:
        crates = list(stacks[source].pop() for _ in range(n))
        stacks[target].extend(reversed(crates))
    return "".join(s[-1] for s in stacks.values())


def main() -> None:
    stacks, moves = parse_data(open(0))

    print(f"P1: {part1(stacks, moves)}")
    print(f"P2: {part2(stacks, moves)}")


if __name__ == "__main__":
    main()
