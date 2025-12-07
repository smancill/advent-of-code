#!/usr/bin/env python

from collections.abc import Mapping, Set
from enum import IntEnum
from heapq import heappop, heappush
from io import StringIO
from typing import Final, NamedTuple, TextIO

type Coord = tuple[int, int]


class RegionType(IntEnum):
    ROCKY = 0
    WET = 1
    NARROW = 2


class Tool(IntEnum):
    TORCH = 0
    GEAR = 1
    NEITHER = 2


tools_for_region: Final[Mapping[RegionType, Set[Tool]]] = {
    RegionType.ROCKY: {Tool.GEAR, Tool.TORCH},
    RegionType.WET: {Tool.GEAR, Tool.NEITHER},
    RegionType.NARROW: {Tool.TORCH, Tool.NEITHER},
}

regions_for_tool: Final[Mapping[Tool, Set[RegionType]]] = {
    Tool.TORCH: {RegionType.ROCKY, RegionType.NARROW},
    Tool.GEAR: {RegionType.ROCKY, RegionType.WET},
    Tool.NEITHER: {RegionType.WET, RegionType.NARROW},
}


def parse_data(f: TextIO) -> tuple[int, Coord]:
    data = [l.split()[-1] for l in f]
    depth = int(data[0])
    tx, ty = map(int, data[1].split(","))
    return depth, (tx, ty)


class Region:
    erosion: Final[int]
    type: Final[RegionType]

    def __init__(self, geo_index: int, depth: int):
        self.erosion = (geo_index + depth) % 20183
        self.type = RegionType(self.erosion % 3)

    @property
    def risk(self) -> int:
        return self.type

    def __str__(self) -> str:
        match self.type:
            case RegionType.ROCKY:
                return "."
            case RegionType.WET:
                return "="
            case RegionType.NARROW:
                return "|"


class Cave:
    type RegionMap = list[list[Region]]

    _data: Final[RegionMap]
    _target: Final[Coord]

    def __init__(self, depth: int, target: Coord, *, extend: int = 200):
        # 'extend' value chosen after trial and error for input data
        width, height = target[0] + extend, target[1] + extend

        self._data = Cave._init_regions((width, height, depth), target)
        self._target = target

    @staticmethod
    def _init_regions(dimensions: tuple[int, int, int], target: Coord) -> RegionMap:
        width, height, depth = dimensions
        placeholder = Region(0, 0)

        regions = [[placeholder] * width for _ in range(height)]

        # Init top-left corner
        regions[0][0] = Region(0, depth)

        # Init top row
        for x in range(1, width):
            geo_index = x * 16807
            regions[0][x] = Region(geo_index, depth)

        # Init left column
        for y in range(1, height):
            geo_index = y * 48271
            regions[y][0] = Region(geo_index, depth)

        # Init rest of regions, including target
        for y in range(1, height):
            for x in range(1, width):
                if (x, y) == target:
                    regions[y][x] = Region(0, depth)
                    continue
                left, top = regions[y][x - 1], regions[y - 1][x]
                geo_index = left.erosion * top.erosion
                regions[y][x] = Region(geo_index, depth)

        return regions

    @property
    def target(self) -> Coord:
        return self._target

    @property
    def mouth(self) -> Coord:
        return (0, 0)

    @property
    def width(self) -> int:
        return len(self._data[0])

    @property
    def height(self) -> int:
        return len(self._data)

    @property
    def risk(self) -> int:
        return sum(
            self[x, y].risk
            for y in range(self.target[1] + 1)
            for x in range(self.target[0] + 1)
        )

    def __getitem__(self, pos: Coord) -> Region:
        return self._data[pos[1]][pos[0]]

    def __str__(self) -> str:
        buf = StringIO()
        for y in range(self.height):
            for x in range(self.width):
                match (x, y):
                    case (0, 0):
                        buf.write("M")
                    case self.target:
                        buf.write("T")
                    case _:
                        buf.write(str(self._data[y][x]))
            buf.write("\n")
        return buf.getvalue()


def _dist(c1: Coord, c2: Coord) -> int:
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])


def _reachable_regions(cave: Cave, pos: Coord, tool: Tool) -> list[Coord]:
    px, py = pos
    return [
        (x, y)
        for x, y in ((px, py - 1), (px, py + 1), (px - 1, py), (px + 1, py))
        if (x >= 0 and y >= 0) and cave[x, y].type in regions_for_tool[tool]
    ]


def _switch_tools(cave: Cave, pos: Coord, tool: Tool) -> list[Tool]:
    return [t for t in tools_for_region[cave[pos].type] if t != tool]


def rescue(cave: Cave) -> int:
    class Move(NamedTuple):
        heuristic: int
        time: int
        position: Coord
        tool: Tool

    queue: list[Move] = []
    visited: dict[tuple[Coord, Tool], int] = {}

    heappush(queue, Move(0, 0, cave.mouth, Tool.TORCH))
    while queue:
        _, time, pos, tool = heappop(queue)

        current = pos, tool
        if current == (cave.target, Tool.TORCH):
            return time
        if current in visited and visited[current] <= time:
            continue
        visited[current] = time

        # Try reachable regions
        for p in _reachable_regions(cave, pos, tool):
            cost = time + 1
            heur = cost + _dist(cave.target, p)
            heappush(queue, Move(heur, cost, p, tool))

        # Try switching tool
        for t in _switch_tools(cave, pos, tool):
            cost = time + 7
            heur = cost + _dist(cave.target, pos)
            heappush(queue, Move(heur, cost, pos, t))

    raise AssertionError


def part1(cave: Cave) -> int:
    return cave.risk


def part2(cave: Cave) -> int:
    return rescue(cave)


def main() -> None:
    data = parse_data(open(0))
    cave = Cave(*data)

    print(f"P1: {part1(cave)}")
    print(f"P2: {part2(cave)}")


if __name__ == "__main__":
    main()
