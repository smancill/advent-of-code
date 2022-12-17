#!/usr/bin/env python

from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import Self, TextIO


class Direction(StrEnum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"


@dataclass(frozen=True)
class Motion:
    direction: Direction
    distance: int


def parse_data(f: TextIO) -> list[Motion]:
    def parse_step(line: str) -> Motion:
        d, v = line.split()
        return Motion(Direction(d), int(v))

    return [parse_step(l) for l in f]


@dataclass
class Coord:
    x: int
    y: int

    def __iadd__(self, o: Self | tuple[int, int]) -> Self:
        match o:
            case Coord(x, y) | (x, y):
                self.x += x
                self.y += y
                return self
            case _:
                raise TypeError(f"unsupported type: {type(o)}")


class Rope:
    _knots: list[Coord]

    def __init__(self, knots: int = 2):
        assert knots > 1
        self._knots = [Coord(0, 0) for _ in range(knots)]

    @property
    def head(self) -> Coord:
        return self._knots[0]

    @property
    def tail(self) -> Coord:
        return self._knots[-1]

    def move(self, direction: Direction) -> None:
        self._knots[0] += self._step(direction)
        for i in range(1, len(self._knots)):
            self._move_tail(self._knots[i - 1], self._knots[i])

    @staticmethod
    def _step(direction: Direction) -> tuple[int, int]:
        match direction:
            case Direction.UP:
                return (0, 1)
            case Direction.DOWN:
                return (0, -1)
            case Direction.LEFT:
                return (-1, 0)
            case Direction.RIGHT:
                return (1, 0)

    @staticmethod
    def _move_tail(head: Coord, tail: Coord) -> None:
        dx, dy = head.x - tail.x, head.y - tail.y
        match (dx, dy):
            case ((-1 | 0 | 1), (-1 | 0 | 1)):
                pass
            case ((-2 | 2), (-1 | 0 | 1)):
                tail += (dx // 2, dy)
            case ((-1 | 0 | 1), (-2 | 2)):
                tail += (dx, dy // 2)
            case ((-2 | 2), (-2 | 2)):
                tail += (dx // 2, dy // 2)
            case _:
                raise ValueError(f"{head=}, {tail=}")


def _count_visited(rope: Rope, motions: Sequence[Motion]) -> int:
    visited = set()
    for motion in motions:
        for _ in range(motion.distance):
            rope.move(motion.direction)
            visited.add((rope.tail.x, rope.tail.y))
    return len(visited)


def part1(data: Sequence[Motion]) -> int:
    return _count_visited(Rope(), data)


def part2(data: Sequence[Motion]) -> int:
    return _count_visited(Rope(10), data)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
