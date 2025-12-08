#!/usr/bin/env python

from operator import add
from typing import TextIO

# https://www.redblobgames.com/grids/hexagons/#neighbors-cube
STEP = {
    "n": (0, 1, -1),
    "s": (0, -1, 1),
    "ne": (1, 0, -1),
    "nw": (-1, 1, 0),
    "se": (1, -1, 0),
    "sw": (-1, 0, 1),
}


def parse_data(f: TextIO) -> str:
    return f.read().rstrip()


def count_steps(path: str) -> tuple[int, int]:
    pos = (0, 0, 0)
    dist = 0
    max_dist = 0
    for step in path.split(","):
        pos = tuple(map(add, pos, STEP[step]))
        dist = sum(map(abs, pos)) // 2
        max_dist = max(max_dist, dist)
    return (dist, max_dist)


def part1(data: str) -> int:
    return count_steps(data)[0]


def part2(data: str) -> int:
    return count_steps(data)[1]


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
