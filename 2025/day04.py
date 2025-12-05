#!/usr/bin/env python

from collections.abc import Iterator
from typing import Final, NamedTuple, Sequence, TextIO


def parse_data(f: TextIO) -> list[str]:
    return [ln.strip() for ln in f]


class Coord(NamedTuple):
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

    def __init__(self, data: Sequence[str]) -> None:
        self._data = [list(r) for r in data]
        self._nx = len(data)
        self._ny = len(data[0])

    def rolls(self) -> Iterator[Coord]:
        for i in range(self._nx):
            for j in range(self._ny):
                if self._data[i][j] == self.ROLL:
                    yield Coord(i, j)

    def accessible(self) -> Iterator[Coord]:
        for roll in self.rolls():
            neighbors = self._neighbors(roll)
            count = sum(1 for i, j in neighbors if self._data[i][j] == self.ROLL)
            if count < self.LIMIT:
                yield roll

    def extract(self, rolls: Iterator[Coord]) -> int:
        count = 0
        for i, j in rolls:
            self._data[i][j] = self.EMPTY
            count += 1
        return count

    def _neighbors(self, roll: Coord) -> Iterator[Coord]:
        for i, j in self.DIRECTIONS:
            pos = Coord(roll.x + i, roll.y + j)
            if 0 <= pos.x < self._nx and 0 <= pos.y < self._ny:
                yield pos


def part1(data: Sequence[str]) -> int:
    grid = Grid(data)
    return sum(1 for _ in grid.accessible())


def part2(data: Sequence[str]) -> int:
    grid = Grid(data)
    total = 0
    while n := grid.extract(grid.accessible()):
        total += n
    return total


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
