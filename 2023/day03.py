#!/usr/bin/env python

import re
from collections import defaultdict
from collections.abc import Iterator, Sequence
from math import prod
from typing import NamedTuple, TextIO

type Schematic = Sequence[str]


class Coord(NamedTuple):
    x: int
    y: int


class Position(NamedTuple):
    start: Coord
    end: Coord


def parse_data(f: TextIO) -> list[str]:
    schema = [""]
    for s in f:
        schema.append("." + s.strip() + ".")
    schema.append("")

    width = len(schema[1])
    schema[0] = width * "."
    schema[-1] = width * "."

    return schema


def get_border(pos: Position) -> list[Coord]:
    assert pos.start.y == pos.end.y

    border = []

    # top
    for i in range(pos.start.x - 1, pos.end.x + 1):
        border.append(Coord(i, pos.start.y - 1))

    # right / left
    border.append(Coord(pos.start.x - 1, pos.start.y))
    border.append(Coord(pos.end.x, pos.start.y))

    # bottom
    for i in range(pos.start.x - 1, pos.end.x + 1):
        border.append(Coord(i, pos.start.y + 1))

    return border


def get_numbers(data: Schematic) -> Iterator[tuple[int, Position]]:
    for y, row in enumerate(data):
        for match in re.finditer(r"\d+", row):
            n = int(match[0])
            start, end = Coord(match.start(), y), Coord(match.end(), y)
            yield (n, Position(start, end))


def part1(data: Schematic) -> int:
    def is_part(pos: Position) -> bool:
        border = get_border(pos)
        return any(data[j][i] != "." for i, j in border)

    return sum(n for n, pos in get_numbers(data) if is_part(pos))


def part2(data: Schematic) -> int:
    gears = defaultdict(set)
    for n, pos in get_numbers(data):
        for i, j in get_border(pos):
            if data[j][i] == "*":
                gears[i, j].add(n)

    return sum(prod(s) for s in gears.values() if len(s) == 2)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
