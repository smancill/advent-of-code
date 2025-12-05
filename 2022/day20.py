#!/usr/bin/env python

from collections.abc import Sequence
from typing import TextIO, TypeAlias

Coord: TypeAlias = tuple[int, int, int]


def parse_data(f: TextIO) -> list[int]:
    return [int(l) for l in f]


def decrypt(encrypted: Sequence[int], key: int, iterations: int) -> Coord:
    # Use indices to ensure unique positions, because of duplicated numbers
    numbers = [key * n for n in encrypted]
    indices = list(range(len(numbers)))

    # Mix
    initial = indices[:]
    for _ in range(iterations):
        for i in initial:
            current = indices.index(i)
            target = (current + numbers[i]) % (len(indices) - 1)
            indices.pop(current)
            indices.insert(target, i)

    # Find coords
    zero = indices.index(numbers.index(0))
    selected = [(zero + k) % len(indices) for k in [1000, 2000, 3000]]
    x, y, z = [numbers[indices[i]] for i in selected]

    return (x, y, z)


def part1(encrypted: Sequence[int]) -> int:
    coords = decrypt(encrypted, key=1, iterations=1)
    return sum(coords)


def part2(encrypted: Sequence[int]) -> int:
    coords = decrypt(encrypted, key=811_589_153, iterations=10)
    return sum(coords)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
