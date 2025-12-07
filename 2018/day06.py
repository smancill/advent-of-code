#!/usr/bin/env python

from collections import Counter
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from itertools import chain
from typing import Self, TextIO

type Coord = tuple[int, int]
type Nearest = Mapping[Coord, Coord]
type TotalDist = Mapping[Coord, int]


def parse_data(f: TextIO) -> list[Coord]:
    def parse_coord(line: str) -> Coord:
        x, y = map(int, line.split(","))
        return x, y

    return [parse_coord(l) for l in f]


@dataclass(frozen=True)
class BoundingBox:
    x0: int
    y0: int
    x1: int
    y1: int

    @classmethod
    def parse(cls, coords: Sequence[Coord]) -> Self:
        x0, y0 = min(x for x, _ in coords) - 1, min(y for _, y in coords) - 1
        x1, y1 = max(x for x, _ in coords) + 1, max(y for _, y in coords) + 1
        return cls(x0, y0, x1, y1)

    def coords(self) -> Iterator[Coord]:
        return (
            (x, y)
            for y in range(self.y0, self.y1 + 1)
            for x in range(self.x0, self.x1 + 1)
        )

    def border(self) -> Iterator[Coord]:
        return chain(
            ((x, self.y0) for x in range(self.x0, self.x1 + 1)),
            ((x, self.y1) for x in range(self.x0, self.x1 + 1)),
            ((self.x0, y) for y in range(self.y0, self.y1 + 1)),
            ((self.x1, y) for y in range(self.y0, self.y1 + 1)),
        )


def _dist(c1: Coord, c2: Coord) -> int:
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])


def calculate_dist(coords: Sequence[Coord]) -> tuple[BoundingBox, Nearest, TotalDist]:
    box = BoundingBox.parse(coords)
    nearest = {}
    total_dist = {}
    for c in box.coords():
        d = {p: _dist(c, p) for p in coords}
        nc, md = min(d.items(), key=lambda it: it[1])
        ct = Counter(d.values())
        if ct[md] == 1:
            nearest[c] = nc
        total_dist[c] = sum(d.values())
    return (box, nearest, total_dist)


def part1(box: BoundingBox, nearest: Nearest) -> int:
    # The areas of coords in the border of bounding box are infinite
    excluded = {nearest[c] for c in box.border() if c in nearest}
    nearest = {k: v for k, v in nearest.items() if v not in excluded}

    (_, count), *_ = Counter(nearest.values()).most_common()
    return count


def part2(total_dist: TotalDist, limit: int = 10000) -> int:
    return sum(1 for v in total_dist.values() if v < limit)


def main() -> None:
    coords = parse_data(open(0))
    box, nearest, total_dist = calculate_dist(coords)

    print(f"P1: {part1(box, nearest)}")
    print(f"P2: {part2(total_dist)}")


if __name__ == "__main__":
    main()
