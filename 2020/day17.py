#!/usr/bin/env python

import itertools
from collections import Counter
from collections.abc import Sequence
from typing import TextIO, TypeAlias

Coord: TypeAlias = tuple[int, ...]


def read_data(f: TextIO) -> list[str]:
    return f.readlines()


def _parse_active(slice: Sequence[str], ndim: int) -> set[Coord]:
    u = [0] * (ndim - 2)
    n, m = len(slice), len(slice[0])
    return {(x, y, *u) for y in range(n) for x in range(m) if slice[y][x] == "#"}


def _shift_coord(coord: Coord, delta: Coord) -> Coord:
    return tuple(i + j for i, j in zip(coord, delta, strict=True))


def simulate(slice: Sequence[str], *, ndim: int, cycles: int = 6) -> int:
    active = _parse_active(slice, ndim)
    deltas = frozenset(itertools.product((-1, 0, 1), repeat=ndim)) - {(0,) * ndim}

    for _ in range(cycles):
        # Heuristic: only consider active nodes plus all their neighbors,
        # instead of all the possible cubes in the n-dim volume occupied by
        # active cubes

        # Reverse count how many active cubes are near every cube
        # that is a neighbor of an active cube
        neighbors = Counter(_shift_coord(c, d) for c in active for d in deltas)
        inactive = set(neighbors) - active

        # Apply rules
        still_active = {c for c in active if neighbors[c] in (2, 3)}
        become_active = {c for c in inactive if neighbors[c] == 3}

        # Switch state
        active = still_active | become_active

    return len(active)


def part1(data: Sequence[str]) -> int:
    return simulate(data, ndim=3)


def part2(data: Sequence[str]) -> int:
    return simulate(data, ndim=4)


def main() -> None:
    data = read_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
