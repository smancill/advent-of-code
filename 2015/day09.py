#!/usr/bin/env python

from collections import defaultdict
from collections.abc import Sequence
from itertools import pairwise, permutations
from typing import TextIO

type Distances = dict[str, dict[str, int]]


def parse_data(f: TextIO) -> Distances:
    distances = defaultdict[str, dict[str, int]](dict)
    for line in f:
        source, _, dest, _, distance = line.split()
        distances[source][dest] = int(distance)
        distances[dest][source] = int(distance)
    return distances


def total_distance(distances: Distances, trip: Sequence[str]) -> int:
    return sum(distances[a][b] for a, b in pairwise(trip))


def part1(distances: Distances) -> int:
    return min(total_distance(distances, trip) for trip in permutations(distances))


def part2(distances: Distances) -> int:
    return max(total_distance(distances, trip) for trip in permutations(distances))


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
