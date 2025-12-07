#!/usr/bin/env python

import re
from collections.abc import Callable, Iterator, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import TextIO

type Coord = tuple[int, int]


class Action(Enum):
    TURN_ON = 0
    TURN_OFF = 1
    TOGGLE = 2


@dataclass(frozen=True)
class Instruction:
    action: Action
    corners: tuple[Coord, Coord]


def parse_data(f: TextIO) -> list[Instruction]:
    def parse_action(action: str) -> Action:
        match action:
            case "turn on":
                return Action.TURN_ON
            case "turn off":
                return Action.TURN_OFF
            case "toggle":
                return Action.TOGGLE
            case _:
                raise ValueError(f"invalid action: {action}")

    def parse_coord(coord: str) -> Coord:
        x, y = map(int, coord.split(","))
        return (x, y)

    def parse_instruction(line: str) -> Instruction:
        if m := re.match(r"(.*) (\d+,\d+) through (\d+,\d+)", line):
            action = parse_action(m.group(1))
            c0, c1 = map(parse_coord, m.group(2, 3))
            return Instruction(action, (c0, c1))
        raise ValueError(f"invalid instruction: {line}")

    return [parse_instruction(l) for l in f]


class Lights:
    _data: list[list[int]]
    _actions: dict[Action, Callable[[int], int]]

    def __init__(self, actions: Mapping[Action, Callable[[int], int]]):
        self._data = [[0] * 1000 for _ in range(1000)]
        self._actions = dict(actions)

    def process(self, instructions: Sequence[Instruction]) -> None:
        for ins in instructions:
            fn = self._actions[ins.action]
            for x, y in self._box(ins):
                self._data[y][x] = fn(self._data[y][x])

    def brightness(self) -> int:
        return sum(c for r in self._data for c in r)

    @staticmethod
    def _box(ins: Instruction) -> Iterator[Coord]:
        (x0, y0), (x1, y1) = ins.corners
        return ((x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1))


def part1(instructions: Sequence[Instruction]) -> int:
    actions = {
        Action.TURN_ON: lambda x: x | 1,
        Action.TURN_OFF: lambda x: x & 0,
        Action.TOGGLE: lambda x: x ^ 1,
    }

    lights = Lights(actions)
    lights.process(instructions)
    return lights.brightness()


def part2(instructions: Sequence[Instruction]) -> int:
    actions = {
        Action.TURN_ON: lambda x: x + 1,
        Action.TURN_OFF: lambda x: x - 1 if x else 0,
        Action.TOGGLE: lambda x: x + 2,
    }

    lights = Lights(actions)
    lights.process(instructions)
    return lights.brightness()


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
