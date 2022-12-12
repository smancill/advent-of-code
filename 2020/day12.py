#!/usr/bin/env python

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Final, Self, TextIO, TypeAlias

Column: TypeAlias = tuple[int, int]
Rotation: TypeAlias = tuple[Column, Column]
Instruction: TypeAlias = tuple[str, int]


rotation: Final[Mapping[int, Rotation]] = {
    0: ((1, 0), (0, 1)),
    90: ((0, 1), (-1, 0)),
    180: ((-1, 0), (0, -1)),
    270: ((0, -1), (1, 0)),
}

unit: Final[Mapping[str, Column]] = {
    "E": (1, 0),
    "N": (0, 1),
    "W": (-1, 0),
    "S": (0, -1),
}


def parse_data(f: TextIO) -> list[Instruction]:
    def parse_instruction(line: str) -> Instruction:
        action, value = line[0], line[1:]
        return action, int(value)

    return [parse_instruction(l) for l in f]


@dataclass
class Vector:
    x: int
    y: int

    def rotate(self, angle: int) -> None:
        u, v = rotation[angle % 360]
        self.x, self.y = self.x * u[0] + self.y * v[0], self.x * u[1] + self.y * v[1]

    def __add__(self, other: Any) -> Self:
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: Any) -> Self:
        self.x, self.y = self.x + other.x, self.y + other.y
        return self

    def __mul__(self, factor: int) -> Self:
        return Vector(factor * self.x, factor * self.y)

    def __rmul__(self, factor: int) -> Self:
        return self.__mul__(factor)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


def _dist(v: Vector) -> int:
    return abs(v.x) + abs(v.y)


def _unit_vector(direction: str) -> Vector:
    return Vector(*unit[direction])


def part1(data: Sequence[Instruction]) -> int:
    position = Vector(0, 0)
    direction = _unit_vector("E")

    for action, value in data:
        match action:
            case "N" | "S" | "E" | "W":
                position += value * _unit_vector(action)
            case "L":
                direction.rotate(value)
            case "R":
                direction.rotate(-value)
            case "F":
                position += value * direction
            case _:
                assert False

    return _dist(position)


def part2(data: Sequence[Instruction]) -> int:
    position = Vector(0, 0)
    waypoint = Vector(10, 1)

    for action, value in data:
        match action:
            case "N" | "S" | "E" | "W":
                waypoint += value * _unit_vector(action)
            case "L":
                waypoint.rotate(value)
            case "R":
                waypoint.rotate(-value)
            case "F":
                position += value * waypoint
            case _:
                assert False

    return _dist(position)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
