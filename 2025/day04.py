#!/usr/bin/env python

from collections.abc import Iterable
from typing import Final, NamedTuple, TextIO


class Point(NamedTuple):
    x: int
    y: int


class Grid:
    _data: list[list[str]]
    _nx: int
    _ny: int

    ROLL: Final = "@"
    EMPTY: Final = "."
    LIMIT: Final = 4

    DIRECTIONS: Final = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]

    def __init__(self, data: list[str]) -> None:
        self._data = [list(r) for r in data]
        self._nx = len(data)
        self._ny = len(data[0])

    def rolls(self) -> Iterable[Point]:
        for i in range(self._nx):
            for j in range(self._ny):
                if self._data[i][j] == self.ROLL:
                    yield Point(i, j)

    def accessible(self) -> Iterable[Point]:
        for p in self.rolls():
            n = sum(1 for i, j in self._neighbors(p) if self._data[i][j] == self.ROLL)
            if n < self.LIMIT:
                yield p

    def extract(self) -> int:
        c = 0
        for i, j in self.accessible():
            self._data[i][j] = self.EMPTY
            c += 1
        return c

    def _neighbors(self, p: Point) -> Iterable[Point]:
        for i, j in self.DIRECTIONS:
            q = Point(p.x + i, p.y + j)
            if 0 <= q.x < self._nx and 0 <= q.y < self._ny:
                yield q


def parse_data(f: TextIO) -> Grid:
    return Grid([ln.strip() for ln in f])


def part1(grid: Grid) -> int:
    return sum(1 for _ in grid.accessible())


def part2(grid: Grid) -> int:
    total = 0
    while n := grid.extract():
        total += n
    return total


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
