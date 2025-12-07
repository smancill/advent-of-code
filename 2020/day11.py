#!/usr/bin/env python

import logging
import logging.config
from collections.abc import Callable, Iterator
from enum import Enum, StrEnum
from itertools import count, islice, product
from typing import Final, TextIO

type Layout = list[list[str]]


def read_data(f: TextIO) -> Layout:
    return [list(l.rstrip()) for l in f]


class Position(StrEnum):
    FLOOR = "."
    EMPTY = "L"
    OCCUPIED = "#"


class Strategy(Enum):
    ADJACENT = 0
    VISIBLE = 1


class Seats:
    _layout: Layout
    _rows: Final[int]
    _cols: Final[int]

    _update_fn: Callable[[int, int], Iterator[tuple[int, int]]]
    _tolerance: Final[int]

    def __init__(self, layout: Layout, strategy: Strategy, tolerance: int):
        self._layout = [r[:] for r in layout]
        self._rows = len(layout)
        self._cols = len(layout[0])

        match strategy:
            case Strategy.ADJACENT:
                self._update_fn = self._adjacent_seats
            case Strategy.VISIBLE:
                self._update_fn = self._visible_seats
        self._tolerance = tolerance

        if logging.getLogger().isEnabledFor(logging.INFO):
            logging.info(self)

    def update(self) -> bool:
        updated = [r[:] for r in self._layout]
        changed = False

        for i in range(self._rows):
            for j in range(self._cols):
                match (self._layout[i][j], self._count_seats(i, j)):
                    case (Position.EMPTY, 0):
                        updated[i][j] = Position.OCCUPIED
                        changed = True
                    case (Position.OCCUPIED, n) if n >= self._tolerance:
                        updated[i][j] = Position.EMPTY
                        changed = True
                    case _:
                        pass
        self._layout = updated

        if logging.getLogger().isEnabledFor(logging.INFO) and changed:
            logging.info(self)

        return not changed

    def occupied(self) -> int:
        return sum(1 for r in self._layout for s in r if s == Position.OCCUPIED)

    def _count_seats(self, r: int, c: int) -> int:
        return sum(
            1
            for i, j in self._update_fn(r, c)
            if self._layout[i][j] == Position.OCCUPIED
        )

    _directions: Final = frozenset(product(range(-1, 2), range(-1, 2))) - {(0, 0)}

    def _adjacent_seats(self, r: int, c: int) -> Iterator[tuple[int, int]]:
        for di, dj in Seats._directions:
            i, j = r + di, c + dj
            if self._is_valid(i, j) and self._layout[i][j] != Position.FLOOR:
                yield (i, j)

    def _visible_seats(self, r: int, c: int) -> Iterator[tuple[int, int]]:
        for di, dj in Seats._directions:
            it = zip(count(r, di), count(c, dj))
            for i, j in islice(it, 1, None):
                if not self._is_valid(i, j):
                    break
                if self._layout[i][j] != Position.FLOOR:
                    yield (i, j)
                    break

    def _is_valid(self, r: int, c: int) -> bool:
        return 0 <= r < self._rows and 0 <= c < self._cols

    def __str__(self) -> str:
        return "\n".join("".join(s for s in r) for r in self._layout) + "\n"


def part1(layout: Layout) -> int:
    seats = Seats(layout, Strategy.ADJACENT, tolerance=4)
    while True:
        if seats.update():
            return seats.occupied()


def part2(layout: Layout) -> int:
    seats = Seats(layout, Strategy.VISIBLE, tolerance=5)
    while True:
        if seats.update():
            return seats.occupied()


def main() -> None:
    logging.config.fileConfig("../logging.conf")

    data = read_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
