#!/usr/bin/env python

import itertools
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from typing import Final, NewType, Self, TextIO, TypeAlias, TypeVar

JetPattern = NewType("JetPattern", str)

T = TypeVar("T")
Enumeration: TypeAlias = Iterator[tuple[int, T]]


ROCK: Final = "#"
EMPTY: Final = "."

ROCKS: Final[Sequence[Sequence[str]]] = [
    [
        "####",
    ],
    [
        ".#.",
        "###",
        ".#.",
    ],
    [
        "..#",
        "..#",
        "###",
    ],
    [
        "#",
        "#",
        "#",
        "#",
    ],
    [
        "##",
        "##",
    ],
]


def parse_data(f: TextIO) -> JetPattern:
    return JetPattern(f.read().strip())


@dataclass(frozen=True)
class Coord:
    x: int
    y: int


@dataclass(frozen=True)
class Rock:
    data: Sequence[Sequence[str]]

    @classmethod
    def make(cls, data: Sequence[str]) -> Self:
        return cls([list(line) for line in data])

    @property
    def width(self) -> int:
        return len(self.data[0])

    @property
    def height(self) -> int:
        return len(self.data)


class Tunnel:
    _data: Final[list[list[str]]]
    _jets: Final[Enumeration[str]]
    _rocks: Final[Enumeration[Rock]]

    WIDTH: Final = 7
    DELTA: Final = 3

    def __init__(self, jets: JetPattern):
        self._data = []
        self._jets = itertools.cycle(enumerate(jets))
        self._rocks = itertools.cycle(enumerate([Rock.make(r) for r in ROCKS]))

    def falling_rocks(self, n: int) -> int:
        state: dict[tuple[int, ...], int] = {}
        cache: dict[int, int] = {}

        top = -1
        for k in range(1, n + 1):
            # add rock
            top, i, j = self._add_rock(top)

            # detect cycle
            key = (i, j, *self._state_at_top(top))
            if key in state:
                prev = state[key]
                top = self._calculate_top(top, (k, prev, n), cache)
                break
            state[key] = k
            cache[k] = top

        return top + 1

    def _add_rock(self, top: int) -> tuple[int, int, int]:
        i, rock = next(self._rocks)
        current = self._orig(top, rock)
        self._expand(current)
        while True:
            # Effect of jet
            j, jet = next(self._jets)
            new = self._push(current, jet)
            if self._can_move_to(new, rock):
                current = new
            # Fall down
            new = self._fall(current)
            if not self._can_move_to(new, rock):
                self._rest(current, rock)
                break
            current = new
        top = max(top, current.y)
        return top, i, j

    def _orig(self, top: int, r: Rock) -> Coord:
        x, y = 2, top + Tunnel.DELTA + r.height
        return Coord(x, y)

    def _expand(self, orig: Coord) -> None:
        delta = orig.y - (len(self._data) - 1)
        if delta > 0:
            self._data.extend(["."] * Tunnel.WIDTH for _ in range(delta))

    def _can_move_to(self, c: Coord, r: Rock) -> bool:
        return self._inside_walls(c, r) and not (
            self._overlap(c, r) or self._at_bottom(c, r)
        )

    def _overlap(self, c: Coord, r: Rock) -> bool:
        for i in range(r.height):
            for j in range(r.width):
                if r.data[i][j] == ROCK and self._data[c.y - i][c.x + j] == ROCK:
                    return True
        return False

    def _rest(self, c: Coord, r: Rock) -> None:
        for i in range(r.height):
            for j in range(r.width):
                if r.data[i][j] == ROCK:
                    self._data[c.y - i][c.x + j] = ROCK

    def _state_at_top(self, top: int) -> tuple[int, ...]:
        def delta(j: int) -> int:
            it = (i for i in reversed(range(top + 1)) if self._data[i][j] == ROCK)
            i = next(it, 0)
            return top - i

        return tuple(delta(j) for j in range(Tunnel.WIDTH))

    def _calculate_top(
        self, top: int, cycle_info: tuple[int, int, int], cache: dict[int, int]
    ) -> int:
        current, prev, total = cycle_info
        period = current - prev
        cycles = (total - prev) // period
        rest = (total - prev) % period
        delta_top = top - cache[prev]
        return cache[prev] + cycles * delta_top + (cache[prev + rest] - cache[prev])

    @staticmethod
    def _push(c: Coord, j: str) -> Coord:
        match j:
            case "<":
                return Coord(c.x - 1, c.y)
            case ">":
                return Coord(c.x + 1, c.y)
            case _:
                raise ValueError("invalid jet: {_}")

    @staticmethod
    def _fall(c: Coord) -> Coord:
        return Coord(c.x, c.y - 1)

    @staticmethod
    def _inside_walls(c: Coord, r: Rock) -> bool:
        return c.x >= 0 and c.x + r.width - 1 < Tunnel.WIDTH

    @staticmethod
    def _at_bottom(c: Coord, r: Rock) -> bool:
        return c.y - (r.height - 1) < 0

    def __str__(self) -> str:
        rows = ["|" + "".join(row) + "|" for row in reversed(self._data)]
        bottom = "+" + "-" * 7 + "+"
        return "\n".join(rows + [bottom])


def part1(data: JetPattern) -> int:
    tunnel = Tunnel(data)
    return tunnel.falling_rocks(2022)


def part2(data: JetPattern) -> int:
    tunnel = Tunnel(data)
    return tunnel.falling_rocks(1_000_000_000_000)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
