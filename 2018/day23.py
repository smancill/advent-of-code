#!/usr/bin/env python

import re
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TextIO

type Coord = tuple[int, int, int]


@dataclass(frozen=True)
class Bot:
    position: Coord
    radius: int


def parse_data(f: TextIO) -> list[Bot]:
    def parse_bot(line: str) -> Bot:
        *pos, r = re.findall(r"-?\d+", line)
        x, y, z = map(int, pos)
        return Bot((x, y, z), int(r))

    return [parse_bot(l) for l in f]


def _dist(c1: Coord, c2: Coord) -> int:
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])


def part1(bots: Sequence[Bot]) -> int:
    best = max(bots, key=lambda b: b.radius)
    return sum(1 for b in bots if _dist(b.position, best.position) <= best.radius)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")


if __name__ == "__main__":
    main()
