#!/usr/bin/env python

import re

from collections import Counter, defaultdict
from functools import reduce
from operator import add

# https://www.redblobgames.com/grids/hexagons/#neighbors-cube
steps = {
    'w': (-1, 1, 0),
    'e': (1, -1, 0),
    'sw': (-1, 0, 1),
    'se': (0, -1, 1),
    'nw': (0, 1, -1),
    'ne': (1, 0, -1),
}

with open("input24.txt") as f:
    data = [re.findall(r'[ns]?[ew]', l) for l in f]


def move(coord, step):
    return tuple(map(add, coord, step))


def create_tiles():
    tiles = defaultdict(int)
    for path in data:
        coord = reduce(move, map(steps.get, path), (0, 0, 0))
        tiles[coord] ^= 1
    return tiles


def part1():
    return sum(c for c in create_tiles().values())


def part2():
    black = set(t for t, s in create_tiles().items() if s == 1)
    ndays = 100

    # Same as Day 17
    for _ in range(ndays):
        neighbors = Counter(
            move(c, d) for c in black for d in steps.values()
        )
        black = set.union(
            {c for c in black if neighbors[c] in (1, 2)},
            {c for c in set(neighbors) - black if neighbors[c] == 2},
        )

    return len(black)


print(f"P1: {part1()}")
print(f"P2: {part2()}")
