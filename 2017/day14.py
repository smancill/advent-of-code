#!/usr/bin/env python

from functools import reduce
from operator import xor
from typing import TextIO

type Grid = list[list[int]]
type Coord = tuple[int, int]
type Region = frozenset[Coord]


def parse_data(f: TextIO) -> Grid:
    return gen_grid(f.read().rstrip())


def gen_grid(key: str, size: int = 128) -> Grid:
    grid: Grid = [[]] * size
    for i in range(size):
        row = knot_hash(f"{key}-{i}")
        row = f"{int(row, 16):0128b}"
        grid[i] = [int(b) for b in row]
    return grid


def knot_hash(key: str) -> str:
    size = 256
    rounds = 64

    numbers = list(range(size))
    lengths = [ord(c) for c in key] + [17, 31, 73, 47, 23]

    pos = 0
    skip = 0
    for _ in range(rounds):
        for length in lengths:
            idx = [(pos + i) % size for i in range(length)]
            val = [numbers[i] for i in idx]
            for i, v in zip(idx, reversed(val), strict=True):
                numbers[i] = v
            pos += (length + skip) % size
            skip += 1

    output = [reduce(xor, numbers[i : i + 16]) for i in range(0, 256, 16)]

    return "".join(f"{x:02x}" for x in output)


def find_region(grid: Grid, orig: Coord) -> Region:
    region = set()
    queue = {orig}
    while queue:
        x, y = queue.pop()
        if not grid[x][y]:
            continue
        if (x, y) in region:
            continue
        region.add((x, y))
        if x > 0:
            queue.add((x - 1, y))
        if y > 0:
            queue.add((x, y - 1))
        if x < 127:
            queue.add((x + 1, y))
        if y < 127:
            queue.add((x, y + 1))
    return frozenset(region)


def get_regions(grid: Grid) -> set[Region]:
    regions = set()
    size = len(grid)
    queue = {(i, j) for i in range(size) for j in range(size) if grid[i][j]}
    while queue:
        coord = queue.pop()
        region = find_region(grid, coord)
        queue -= region
        regions.add(region)
    return regions


def part1(grid: Grid) -> int:
    return sum(sum(row) for row in grid)


def part2(grid: Grid) -> int:
    return len(get_regions(grid))


def main() -> None:
    grid = parse_data(open(0))

    print(f"P1: {part1(grid)}")
    print(f"P2: {part2(grid)}")


if __name__ == "__main__":
    main()
