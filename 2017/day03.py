#!/usr/bin/env python

from collections.abc import Iterator
from itertools import count, islice
from typing import TextIO

Coord = tuple[int, int]


def parse_data(f: TextIO) -> int:
    return int(f.read())


def manhattan_distance(p1: Coord, p2: Coord) -> int:
    dx = abs(p1[0] - p2[0])
    dy = abs(p1[1] - p2[1])
    return dx + dy


def gen_spiral() -> Iterator[Coord]:
    # based on solution by u/oantolin
    # https://www.reddit.com/r/adventofcode/comments/7h7ufl/2017_day_3_solutions/dqox0fv/
    i, j = 0, 0
    yield i, j
    for s in count(1, 2):
        for ds, dx, dy in [(0, 1, 0), (0, 0, 1), (1, -1, 0), (1, 0, -1)]:
            for _ in range(s + ds):
                i += dx
                j += dy
                yield i, j


def gen_simple_grid() -> Iterator[tuple[Coord, int]]:
    return zip(gen_spiral(), count(1))


def gen_stress_grid() -> Iterator[tuple[Coord, int]]:
    def sum_neighbors(x: int, y: int) -> int:
        return sum(
            M.get((i, j), 0) for i in range(x - 1, x + 2) for j in range(y - 1, y + 2)
        )

    M = {(0, 0): 1}  # noqa: N806
    for i, j in gen_spiral():
        val = sum_neighbors(i, j)
        M[i, j] = val
        yield ((i, j), val)


def part1(target: int) -> int:
    pos = next(islice(gen_spiral(), target - 1, target))
    return manhattan_distance((0, 0), pos)


def part2(target: int) -> int:
    return next(v for _, v in gen_stress_grid() if v > target)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
