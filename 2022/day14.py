#!/usr/bin/env python

from collections.abc import Iterator, Sequence
from typing import Final, TextIO, TypeAlias

AIR: Final = "."
ROCK: Final = "#"
SAND: Final = "o"

SOURCE: Final = "+"
ORIG: Final = 500

Limits: TypeAlias = tuple[int, int]
Coord: TypeAlias = tuple[int, int]
Rock: TypeAlias = list[tuple[Coord, Coord]]


def parse_data(f: TextIO) -> list[Rock]:
    def parse_coord(coord: str) -> Coord:
        x, y = coord.split(",")
        return int(x), int(y)

    def parse_rock(line: str) -> Rock:
        coords = [parse_coord(c) for c in line.strip().split(" -> ")]
        return [r for r in zip(coords[:-1], coords[1:])]

    return [parse_rock(l) for l in f]


class Map2D:
    _data: Final[list[list[str]]]

    def __init__(self, height: int, width: int, initial: str):
        self._data = [[initial] * width for _ in range(height)]

    @property
    def width(self) -> int:
        return len(self._data[0])

    @property
    def height(self) -> int:
        return len(self._data)

    def __getitem__(self, key: tuple[int, int]) -> str:
        return self._data[key[1]][key[0]]

    def __setitem__(self, key: tuple[int, int], item: str) -> None:
        self._data[key[1]][key[0]] = item


class Cave:
    _data: Final[Map2D]
    _source: Final[Coord]

    def __init__(self, rocks: Sequence[Rock], floor_delta: int = 0):
        # Make cave
        coords = Cave._coords(rocks)

        xlim, ylim = Cave._limits(coords, floor_delta)
        width, height = Cave._size(xlim, ylim)

        self._data = Map2D(height, width, AIR)

        # Set rocks
        for c in coords:
            c = Cave._normalize(c, xlim)
            self._data[c] = ROCK

        # Set optional floor
        if Cave._use_floor(floor_delta):
            for c in Cave._floor(width, height):
                self._data[c] = ROCK

        # Set source of sand
        self._source = Cave._normalize((ORIG, 0), xlim)
        self._data[self._source] = SOURCE

    @staticmethod
    def _coords(rocks: Sequence[Rock]) -> set[Coord]:
        def line_coords(line: tuple[Coord, Coord]) -> list[Coord]:
            (x0, y0), (x1, y1) = line
            if x0 == x1:
                y0, y1 = (y0, y1) if y0 < y1 else (y1, y0)
                return [(x0, y) for y in range(y0, y1 + 1)]
            elif y0 == y1:
                x0, x1 = (x0, x1) if x0 < x1 else (x1, x0)
                return [(x, y0) for x in range(x0, x1 + 1)]
            else:
                raise ValueError(line)

        return {c for r in rocks for l in r for c in line_coords(l)}

    @staticmethod
    def _floor(width: int, height: int) -> list[Coord]:
        return [(x, height - 1) for x in range(width)]

    @staticmethod
    def _normalize(coord: Coord, xlim: Limits) -> Coord:
        return (coord[0] - xlim[0], coord[1])

    @staticmethod
    def _limits(coords: set[Coord], floor_delta: int) -> tuple[Limits, Limits]:
        x0, x1 = min(x for x, _ in coords), max(x for x, _ in coords)
        y0, y1 = min(y for _, y in coords), max(y for _, y in coords)

        if Cave._use_floor(floor_delta):
            y1 = y1 + floor_delta
            x0 = min(x0, ORIG - y1)
            x1 = max(x1, ORIG + y1)

        # Extra columns because sand may roll down left/rigth of min/max rocks
        x0, x1 = x0 - 1, x1 + 1

        return (x0, x1), (y0, y1)

    @staticmethod
    def _size(xlim: Limits, ylim: Limits) -> tuple[int, int]:
        width = xlim[1] - xlim[0] + 1
        height = ylim[1] + 1
        return width, height

    @staticmethod
    def _use_floor(floor_delta: int) -> bool:
        return floor_delta > 0

    def fill(self) -> None:
        M = self._data

        def move_to(x: int, y: int) -> Coord | None:
            if M[(target := (x, y + 1))] == AIR:
                return target
            if M[(target := (x - 1, y + 1))] == AIR:
                return target
            if M[(target := (x + 1, y + 1))] == AIR:
                return target
            return None

        while True:
            x, y = self._source
            M[x, y] = SAND
            prev = SOURCE

            falling = True
            while True:
                if y == M.height - 1:
                    M[x, y] = AIR
                    break
                if target := move_to(x, y):
                    M[x, y] = prev
                    M[target] = SAND
                    x, y = target
                else:
                    falling = False
                    break
                prev = AIR

            if falling or (x, y) == self._source:
                break

    def count(self) -> int:
        return sum(1 for _ in self._sand())

    def _sand(self) -> Iterator[Coord]:
        return (
            (x, y)
            for y in range(self._data.height)
            for x in range(self._data.width)
            if self._data[x, y] == SAND
        )

    def __str__(self) -> str:
        def row(y: int) -> str:
            return "".join(self._data[x, y] for x in range(self._data.width))

        return "\n".join(row(y) for y in range(self._data.height))


def part1(data: Sequence[Rock]) -> int:
    cave = Cave(data)
    cave.fill()
    return cave.count()


def part2(data: Sequence[Rock]) -> int:
    cave = Cave(data, floor_delta=2)
    cave.fill()
    return cave.count()


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
