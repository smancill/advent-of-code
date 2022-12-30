#!/usr/bin/env python

from collections.abc import Set
from typing import Final, NamedTuple, TextIO


class Coord(NamedTuple):
    x: int
    y: int
    z: int


def parse_data(f: TextIO) -> set[Coord]:
    def parse_coord(line: str) -> Coord:
        x, y, z = map(int, line.strip().split(","))
        return Coord(x, y, z)

    return {parse_coord(l) for l in f}


class BoundingBox:
    xlim: Final[tuple[int, int]]
    ylim: Final[tuple[int, int]]
    zlim: Final[tuple[int, int]]

    def __init__(self, cubes: Set[Coord]):
        xs, ys, zs = zip(*cubes)

        self.xlim = min(xs) - 1, max(xs) + 1
        self.ylim = min(ys) - 1, max(ys) + 1
        self.zlim = min(zs) - 1, max(zs) + 1

    def orig(self) -> Coord:
        return Coord(self.xlim[0], self.ylim[0], self.zlim[0])

    def __contains__(self, c: Coord) -> bool:
        return (
            self.xlim[0] <= c.x <= self.xlim[1]
            and self.ylim[0] <= c.y <= self.ylim[1]
            and self.zlim[0] <= c.z <= self.zlim[1]
        )


def _adjacent(c: Coord) -> list[Coord]:
    return [
        Coord(c.x + 1, c.y, c.z),
        Coord(c.x - 1, c.y, c.z),
        Coord(c.x, c.y + 1, c.z),
        Coord(c.x, c.y - 1, c.z),
        Coord(c.x, c.y, c.z + 1),
        Coord(c.x, c.y, c.z - 1),
    ]


def _flood_fill(cubes: Set[Coord]) -> set[Coord]:
    box = BoundingBox(cubes)
    visited = set(cubes)
    queue = [box.orig()]
    while queue:
        c = queue.pop()
        visited.add(c)
        queue.extend(a for a in _adjacent(c) if a in box and a not in visited)
    return visited - cubes


def part1(cubes: Set[Coord]) -> int:
    return sum(a not in cubes for c in cubes for a in _adjacent(c))


def part2(cubes: Set[Coord]) -> int:
    exterior = _flood_fill(cubes)
    return sum(a in exterior for c in cubes for a in _adjacent(c))


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
