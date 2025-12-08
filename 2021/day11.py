#!/usr/bin/env python

from collections.abc import Iterable, Iterator
from itertools import count, product
from typing import TextIO

type Coord = tuple[int, int]
type Area = dict[Coord, int]

DELTAS = set(product((-1, 0, 1), repeat=2)) - {(0, 0)}


def parse_data(f: TextIO) -> Area:
    area = {}
    for y, row in enumerate(f):
        for x, energy in enumerate(row.strip()):
            area[x, y] = int(energy)
    return area


def adjacents(area: Area, pos: Coord) -> Iterator[Coord]:
    adj = [(pos[0] + i, pos[1] + j) for i, j in DELTAS]
    return (p for p in adj if p in area)


def show(area: Area) -> None:
    mi = max(i for i, _ in area)
    mj = max(j for _, j in area)
    for i in range(mi + 1):
        for j in range(mj + 1):
            n = area[(i, j)]
            print(n, end="")
        print()


def flash(data: Area) -> int:
    def visit(positions: Iterable[Coord]) -> None:
        for p in positions:
            data[p] += 1
            if data[p] > 9:
                queue.add(p)

    queue = set[Coord]()
    visit(data)
    count = 0
    while queue:
        pos = queue.pop()
        data[pos] = 0
        count += 1
        visit(p for p in adjacents(data, pos) if data[p] != 0)
    return count


def part1(area: Area, steps: int = 100) -> int:
    return sum(flash(area) for _ in range(steps))


def part2(area: Area) -> int:
    size = len(area)
    for i in count(1):
        if flash(area) == size:
            return i
    raise AssertionError


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data.copy())}")
    print(f"P2: {part2(data.copy())}")


if __name__ == "__main__":
    main()
