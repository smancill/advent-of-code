#!/usr/bin/env python

import functools
import re
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from typing import Final, TextIO, TypeAlias

HexCoord: TypeAlias = tuple[int, int, int]
Steps: TypeAlias = list[str]

# https://www.redblobgames.com/grids/hexagons/#neighbors-cube
direction: Final[Mapping[str, HexCoord]] = {
    "w": (-1, 1, 0),
    "e": (1, -1, 0),
    "sw": (-1, 0, 1),
    "se": (0, -1, 1),
    "nw": (0, 1, -1),
    "ne": (1, 0, -1),
}


def parse_data(f: TextIO) -> list[Steps]:
    def parse_steps(line: str) -> Steps:
        return re.findall(r"[ns]?[ew]", line)

    return [parse_steps(l) for l in f]


def _move(coord: HexCoord, delta: HexCoord) -> HexCoord:
    return (coord[0] + delta[0], coord[1] + delta[1], coord[2] + delta[2])


def _create_tiles(data: Sequence[Steps]) -> dict[HexCoord, int]:
    tiles: dict[HexCoord, int] = defaultdict(int)
    for path in data:
        deltas = (direction[p] for p in path)
        coord = functools.reduce(_move, deltas, (0, 0, 0))
        tiles[coord] ^= 1
    return tiles


def part1(data: Sequence[Steps]) -> int:
    return sum(c for c in _create_tiles(data).values())


def part2(data: Sequence[Steps]) -> int:
    black = {t for t, s in _create_tiles(data).items() if s == 1}
    ndays = 100

    # Same as Day 17
    for _ in range(ndays):
        neighbors = Counter(_move(c, d) for c in black for d in direction.values())
        white = set(neighbors) - black

        still_black = {c for c in black if neighbors[c] in (1, 2)}
        become_black = {c for c in white if neighbors[c] == 2}

        black = still_black | become_black

    return len(black)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
