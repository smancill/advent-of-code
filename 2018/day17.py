#!/usr/bin/env python

import re
from collections.abc import Sequence
from itertools import count
from typing import Final, NamedTuple, TextIO

CLAY: Final = "#"
SAND: Final = "."

SOURCE: Final = "+"
WATER: Final = "~"
FLOW: Final = "|"


class Coord(NamedTuple):
    x: int
    y: int


class Limits(NamedTuple):
    low: int
    high: int


def parse_data(f: TextIO) -> list[Coord]:
    clay: list[Coord] = []
    for line in f:
        if m := re.match(r"x=(\d+), y=(\d+)..(\d+)", line):
            x, y0, y1 = map(int, m.group(1, 2, 3))
            clay.extend(Coord(x, y) for y in range(y0, y1 + 1))
        elif m := re.match(r"y=(\d+), x=(\d+)..(\d+)", line):
            y, x0, x1 = map(int, m.group(1, 2, 3))
            clay.extend(Coord(x, y) for x in range(x0, x1 + 1))
    return clay


class Map2D:
    _data: Final[list[list[str]]]

    def __init__(self, width: int, height: int, initial: str):
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

    def __str__(self) -> str:
        return "\n".join("".join(r) for r in self._data)


class WaterMap(Map2D):
    _orig: Coord

    def __init__(self, orig: Coord, clay: Sequence[Coord]):
        xlim, ylim = self._limits(clay)
        width, height = self._size(xlim, ylim)

        super().__init__(width, height, SAND)
        for c in clay:
            c = self._normalize(c, xlim)
            self[c] = CLAY

        self._orig = self._normalize(orig, xlim)
        self[self._orig] = SOURCE

    @staticmethod
    def _limits(clay: Sequence[Coord]) -> tuple[Limits, Limits]:
        x0, x1 = min(x for x, _ in clay), max(x for x, _ in clay)
        y0, y1 = min(y for _, y in clay), max(y for _, y in clay)

        # Extra columns because water may flow left/rigth of min/max veins
        x0, x1 = x0 - 1, x1 + 1

        return Limits(x0, x1), Limits(y0, y1)

    @staticmethod
    def _size(xlim: Limits, ylim: Limits) -> tuple[int, int]:
        width = xlim.high - xlim.low + 1
        height = ylim.high + 1
        return width, height

    @staticmethod
    def _normalize(coord: Coord, xlim: Limits) -> Coord:
        return Coord(coord.x - xlim.low, coord.y)

    def fill(self) -> None:
        down_queue = [self._orig]
        while down_queue:
            x, y = down_queue.pop()
            if self[x, y] == WATER:
                continue
            stop = self._flow_down(x, y)
            if stop is None:
                continue
            spread_queue = [stop]
            while spread_queue:
                x, y = spread_queue.pop()
                xlim = self._flow_horizontally(x, y)
                if self._contained(xlim, y):
                    s = self._fill_up(xlim, y)
                    spread_queue.append(s)
                else:
                    o = self._overflow(xlim, y)
                    down_queue.extend(o)

    def count(self, water: set[str]) -> int:
        y0 = next(i for i, row in enumerate(self._data) if CLAY in row)
        return sum(
            1
            for y in range(y0, self.height)
            for x in range(self.width)
            if self[x, y] in water
        )

    def _flow_down(self, x: int, y: int) -> Coord | None:
        for i in range(y + 1, self.height):
            if self[x, i] == CLAY or self[x, i] == WATER:
                return Coord(x, i - 1)
            if self[x, i] == FLOW:
                return None
            self[x, i] = FLOW
        return None  # Reached the bottom of the area

    def _flow_horizontally(self, x: int, y: int) -> Limits:
        def flow(start: int, step: int) -> int:
            for j in count(start, step):
                if self[j, y] == CLAY:
                    return j
                self[j, y] = FLOW
                if self[j, y + 1] == SAND:
                    return j
            assert False  # Must reach a clay wall, or a border to flow down

        return Limits(flow(x - 1, -1), flow(x + 1, 1))

    def _fill_up(self, xlim: Limits, y: int) -> Coord:
        xrange = range(xlim.low + 1, xlim.high)
        for j in xrange:
            self[j, y] = WATER
        for j in xrange:
            if self[j, y - 1] == FLOW:
                return Coord(j, y - 1)
        assert False  # Must reach a source of water

    def _overflow(self, xlim: Limits, y: int) -> list[Coord]:
        return [Coord(x, y) for x in [xlim.low, xlim.high] if self[x, y + 1] == SAND]

    def _contained(self, xlim: Limits, y: int) -> bool:
        return self[xlim.low, y] == CLAY and self[xlim.high, y] == CLAY


class Ground:
    _data: Final[WaterMap]

    def __init__(self, clay: Sequence[Coord]):
        self._data = WaterMap(Coord(500, 0), clay)

    def fill_water(self) -> None:
        self._data.fill()

    def total_water(self, dry: bool = False) -> int:
        w = {WATER} if dry else {WATER, FLOW}
        return self._data.count(w)

    def __str__(self) -> str:
        return str(self._data)


def main() -> None:
    coords = parse_data(open(0))

    ground = Ground(coords)
    ground.fill_water()

    print(f"P1: {ground.total_water(dry=False)}")
    print(f"P2: {ground.total_water(dry=True)}")


if __name__ == "__main__":
    main()
