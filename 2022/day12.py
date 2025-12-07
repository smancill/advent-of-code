#!/usr/bin/env python

import heapq
from collections.abc import Iterator, Sequence
from typing import TextIO

type Coord = tuple[int, int]


class HeightMap:
    _data: list[list[str]]

    def __init__(self, data: list[list[str]]):
        self._data = [r[:] for r in data]

    @property
    def width(self) -> int:
        return len(self._data[0])

    @property
    def height(self) -> int:
        return len(self._data)

    def reachable(self, coord: Coord) -> list[Coord]:
        x, y = coord
        adjacent = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
        return [c for c in adjacent if self._in_map(c) and self._can_climb(coord, c)]

    def _in_map(self, coord: Coord) -> bool:
        return 0 <= coord[0] < self.width and 0 <= coord[1] < self.height

    def _can_climb(self, coord: Coord, adj: Coord) -> bool:
        return self._elevation(adj) - self._elevation(coord) <= 1

    def _elevation(self, coord: Coord) -> int:
        return ord(self._data[coord[1]][coord[0]])

    def __getitem__(self, coord: Coord) -> str:
        return self._data[coord[1]][coord[0]]


def parse_data(f: TextIO) -> tuple[HeightMap, Coord, Coord]:
    def find_location(t: str) -> Coord:
        w, h = len(data[0]), len(data)
        return next((x, y) for x, y in _coords(w, h) if data[y][x] == t)

    data = [list(l.rstrip()) for l in f]

    sx, sy = find_location("S")
    data[sy][sx] = "a"

    tx, ty = find_location("E")
    data[ty][tx] = "z"

    return HeightMap(data), (sx, sy), (tx, ty)


def _coords(width: int, height: int) -> Iterator[Coord]:
    return ((x, y) for y in range(height) for x in range(width))


def min_distance(heights: HeightMap, start: Sequence[Coord], target: Coord) -> int:
    visited = {}
    queue = [(0, c) for c in start]
    heapq.heapify(queue)

    while queue:
        dist, current = heapq.heappop(queue)

        if current == target:
            visited[current] = dist
            break

        if current in visited:
            continue
        visited[current] = dist

        for coord in heights.reachable(current):
            heapq.heappush(queue, (dist + 1, coord))

    return visited[target]


def part1(heights: HeightMap, current: Coord, target: Coord) -> int:
    start = [current]
    return min_distance(heights, start, target)


def part2(heights: HeightMap, _: Coord, target: Coord) -> int:
    start = [c for c in _coords(heights.width, heights.height) if heights[c] == "a"]
    return min_distance(heights, start, target)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(*data)}")
    print(f"P2: {part2(*data)}")


if __name__ == "__main__":
    main()
