#!/usr/bin/env python

from collections import defaultdict
from collections.abc import Mapping, Set
from typing import Final, NamedTuple, TextIO, TypeAlias

Coord: TypeAlias = tuple[int, int]


def parse_data(f: TextIO) -> str:
    return f.read().strip()


class Room:
    _dist: Final[dict[Coord, int]]
    _doors: Final[dict[Coord, set[Coord]]]

    def __init__(self, regex: str):
        self._dist = {(0, 0): 0}
        self._doors = defaultdict(set)
        self._parse(regex)

    @property
    def dist(self) -> Mapping[Coord, int]:
        return self._dist

    @property
    def doors(self) -> Mapping[Coord, Set[Coord]]:
        return self._doors

    def _parse(self, regex: str) -> None:
        class Group(NamedTuple):
            start: set[Coord]
            end: set[Coord]

        positions = {(0, 0)}
        groups = []

        for c in regex[1:-1]:
            if c == "(":
                groups.append(Group(positions, set()))
            elif c == "|":
                group = groups[-1]
                group.end.update(positions)
                positions = group.start
            elif c == ")":
                group = groups.pop()
                positions.update(group.end)
            else:
                positions = {self._move(p, c) for p in positions}

    def _move(self, pos: Coord, move: str) -> Coord:
        x, y = pos
        match move:
            case "N":
                dest = (x, y - 1)
            case "W":
                dest = (x - 1, y)
            case "E":
                dest = (x + 1, y)
            case "S":
                dest = (x, y + 1)
            case _:
                raise ValueError(f"Invalid {move=}")

        n = self._dist[pos] + 1
        if dest not in self._dist or self._dist[dest] > n:
            self._dist[dest] = n

        self._doors[pos].add(dest)
        self._doors[dest].add(pos)

        return dest

    # This is not necessary to solve the problem
    # but implemented anyway as exercise
    def __str__(self) -> str:
        x0, x1 = min(x for x, _ in self.dist), max(x for x, _ in self.dist)
        y0, y1 = min(y for _, y in self.dist), max(y for _, y in self.dist)

        w = (x1 - x0 + 1) * 2 + 1
        h = (y1 - y0 + 1) * 2 + 1

        room_map = [["#"] * w for _ in range(h)]

        def map_row(y: int) -> None:
            i = (y - y0) * 2 + 1
            for x in range(x0, x1 + 1):
                j = (x - x0) * 2 + 1
                room, adj = (x, y), (x + 1, y)
                room_map[i][j] = "." if room != (0, 0) else "X"
                room_map[i][j + 1] = "|" if adj in self.doors[room] else "#"

        def map_sep(y: int) -> None:
            i = (y - y0) * 2 + 1
            for x in range(x0, x1 + 1):
                j = (x - x0) * 2 + 1
                room, adj = (x, y), (x, y + 1)
                room_map[i + 1][j] = "-" if adj in self.doors[room] else "#"

        for y in range(y0, y1):
            map_row(y)
            map_sep(y)
        map_row(y1)

        return "\n".join("".join(r) for r in room_map)


def part1(room: Room) -> int:
    return max(room.dist.values())


def part2(room: Room) -> int:
    return sum(1 for x in room.dist.values() if x >= 1000)


def main() -> None:
    data = parse_data(open(0))
    room = Room(data)

    print(f"P1: {part1(room)}")
    print(f"P2: {part2(room)}")


if __name__ == "__main__":
    main()
