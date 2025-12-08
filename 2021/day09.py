#!/usr/bin/env python

from collections.abc import Iterator
from math import prod
from typing import TextIO

type Coord = tuple[int, int]
type Area = dict[Coord, int]

DELTAS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def parse_data(f: TextIO) -> Area:
    area = {}
    for y, row in enumerate(f):
        for x, height in enumerate(row.strip()):
            area[x, y] = int(height)
    return area


def adjacents(area: Area, pos: Coord) -> Iterator[Coord]:
    adj = [(pos[0] + i, pos[1] + j) for i, j in DELTAS]
    return (p for p in adj if p in area)


def is_lowest_point(area: Area, pos: Coord) -> bool:
    return all(area[pos] < area[adj] for adj in adjacents(area, pos))


def find_basin(area: Area, lowest: Coord) -> set[Coord]:
    basin = {lowest}
    visited = {lowest}
    queue = list(adjacents(area, lowest))
    while queue:
        adj = queue.pop()
        if adj in visited:
            continue
        visited.add(adj)
        if area[adj] == 9:
            continue
        basin.add(adj)
        queue.extend(adjacents(area, adj))
    return basin


def part1(area: Area) -> int:
    return sum(area[p] + 1 for p in area if is_lowest_point(area, p))


def part2(area: Area) -> int:
    basins = [find_basin(area, p) for p in area if is_lowest_point(area, p)]
    basins.sort(key=lambda b: len(b))
    return prod(len(b) for b in basins[-3:])


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
