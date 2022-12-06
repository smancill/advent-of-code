#!/usr/bin/env python

from collections.abc import Sequence
from typing import Final, NamedTuple, TextIO, TypeAlias

N: Final = 300

Coord: TypeAlias = tuple[int, int]
Grid: TypeAlias = Sequence[Sequence[int]]


class MaxPower(NamedTuple):
    coord: Coord
    size: int
    power: int


def parse_data(f: TextIO) -> int:
    return int(f.read())


def power_level(coord: Coord, serial: int) -> int:
    x, y = coord
    rack_id = x + 10
    level = (rack_id * y + serial) * rack_id
    level = (level // 100) % 10
    return level - 5


def make_grid(serial: int) -> Grid:
    return [[power_level((x, y), serial) for x in range(N + 1)] for y in range(N + 1)]


# Optimize for fun with partial sums
# but brute force O(k^2 n^2) would do just fine for k=3
def max_power_fixed(grid: Grid, k: int = 3) -> MaxPower:
    L = (N - k) + 1
    P = [[0] * (N + 1) for _ in range(N + 1)]

    for y in range(1, N + 1):
        t = sum(grid[y][x] for x in range(1, k + 1))
        P[y][1] = t

        for x in range(2, L + 1):
            t += grid[y][x + k - 1] - grid[y][x - 1]
            P[y][x] = t

    m = MaxPower((0, 0), k, -1)
    for x in range(1, L + 1):
        t = sum(P[y][x] for y in range(1, k + 1))
        m = max(MaxPower((x, 1), k, t), m, key=lambda t: t.power)

        for y in range(2, L + 1):
            t += P[y + k - 1][x] - P[y - 1][x]
            m = max(MaxPower((x, y), k, t), m, key=lambda t: t.power)

    return m


# Brute force would be O(n^5), too much.
# Use cumulative sums to make it O(n^3).
def max_power_dial(grid: Grid, start: int = 1, end: int = N) -> MaxPower:
    C = [[0] * (N + 1) for _ in range(N + 1)]
    for y in range(1, N + 1):
        for x in range(1, N + 1):
            C[y][x] = grid[y][x] + C[y - 1][x] + C[y][x - 1] - C[y - 1][x - 1]

    m = MaxPower((0, 0), 0, -1)
    for k in range(start, end + 1):
        for y in range(k, N + 1):
            for x in range(k, N + 1):
                p = C[y][x] - C[y - k][x] - C[y][x - k] + C[y - k][x - k]
                if p > m.power:
                    m = MaxPower((x - k + 1, y - k + 1), k, p)
    return m


def part1(grid: Grid) -> MaxPower:
    return max_power_fixed(grid, 3)


def part2(grid: Grid) -> MaxPower:
    return max_power_dial(grid)


def main() -> None:
    data = parse_data(open(0))
    grid = make_grid(data)

    print(f"P1: {part1(grid)}")
    print(f"P2: {part2(grid)}")


if __name__ == "__main__":
    main()
