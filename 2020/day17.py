#!/usr/bin/env python

from collections import Counter
from itertools import product


def parse_input(ndim):
    with open("input17.txt") as f:
        u = [0] * (ndim - 2)
        return {(x, y, *u)
                for x, r in enumerate(f) for y, c in enumerate(r) if c == '#'}


def simulate(ndim, cycles=6):
    active = parse_input(ndim)
    deltas = set(product((-1, 0, 1), repeat=ndim)) - {(0,) * ndim}

    for _ in range(cycles):
        neighbors = Counter(
            tuple(i + j for i, j in zip(c, d)) for c in active for d in deltas
        )
        active = set.union(
            {c for c in active if neighbors[c] in (2, 3)},
            {c for c in set(neighbors) - active if neighbors[c] == 3},
        )

    return len(active)


print(f"P1: {simulate(ndim=3)}")
print(f"P2: {simulate(ndim=4)}")
