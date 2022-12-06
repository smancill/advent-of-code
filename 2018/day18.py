#!/usr/bin/env python

import logging
import logging.config
from collections.abc import Sequence
from functools import cache
from typing import Final, Self, TextIO


def read_data(f: TextIO) -> list[str]:
    return f.readlines()


class Area:
    _acres: list[list[str]]
    _width: Final[int]
    _height: Final[int]

    OPEN: Final = "."
    TREES: Final = "|"
    LUMBERJACK: Final = "#"

    def __init__(self, acres: list[list[str]]):
        self._acres = acres
        self._width = len(acres[0])
        self._height = len(acres)

    @classmethod
    def parse(cls, data: Sequence[str]) -> Self:
        return cls([list(l.rstrip()) for l in data])

    def update(self) -> None:
        updated = [r[:] for r in self._acres]
        for i in range(self._height):
            for j in range(self._width):
                adj = self._adjacent_acres(i, j)
                match self._acres[i][j]:
                    case Area.OPEN:
                        if 3 <= sum(1 for a in adj if a == Area.TREES):
                            updated[i][j] = Area.TREES
                    case Area.TREES:
                        if 3 <= sum(1 for a in adj if a == Area.LUMBERJACK):
                            updated[i][j] = Area.LUMBERJACK
                    case Area.LUMBERJACK:
                        if not (Area.LUMBERJACK in adj and Area.TREES in adj):
                            updated[i][j] = Area.OPEN
        self._acres = updated

    def _adjacent_acres(self, y: int, x: int) -> list[str]:
        return [self._acres[i][j] for i, j in self._adjacent_positions(y, x)]

    @cache
    def _adjacent_positions(self, y: int, x: int) -> list[tuple[int, int]]:
        return [
            (i, j)
            for i, j in (
                (y - 1, x - 1),
                (y - 1, x),
                (y - 1, x + 1),
                (y, x - 1),
                (y, x + 1),
                (y + 1, x - 1),
                (y + 1, x),
                (y + 1, x + 1),
            )
            if 0 <= i < self._height and 0 <= j < self._width
        ]

    @property
    def value(self) -> int:
        nt = sum(1 for r in self._acres for c in r if c == Area.TREES)
        nl = sum(1 for r in self._acres for c in r if c == Area.LUMBERJACK)
        return nt * nl

    def __str__(self) -> str:
        return "\n".join("".join(r) for r in self._acres) + "\n"


def part1(data: Sequence[str]) -> int:
    area = Area.parse(data)
    if verbose := logging.getLogger().isEnabledFor(logging.DEBUG):
        logging.debug("Initial state:")
        logging.debug(area)

    for t in range(10):
        area.update()
        if verbose:
            logging.debug(f"After {t + 1} minute{'' if t == 0 else 's'}:")
            logging.debug(area)

    return area.value


def part2(data: Sequence[str], minutes: int = 1_000_000_000) -> int:
    area = Area.parse(data)

    # Loop until finding a cycle
    prev = {str(area): 0}
    m = 0
    for t in range(1, minutes + 1):
        area.update()
        s = str(area)
        if s in prev:
            c = prev[s]
            m = (minutes - t) % (t - c)
            break
        prev[s] = t
    else:
        raise ValueError("Could not find a cycle")

    # Loop the cycle until reaching the final state
    for _ in range(m):
        area.update()

    return area.value


def main() -> None:
    logging.config.fileConfig("../logging.conf")

    data = read_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
