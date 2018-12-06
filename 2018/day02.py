#!/usr/bin/env python3

from collections import Counter
from itertools import combinations

with open("input02.txt") as f:
    data = [l.strip() for l in f]


def part1(data):
    with2 = 0
    with3 = 0
    for l in data:
        freqs = Counter(l)
        if 2 in freqs.values():
            with2 += 1
        if 3 in freqs.values():
            with3 += 1
    return with2 * with3


def part2(data):
    for x, y in combinations(data, 2):
        common = [a for a, b in zip(x, y) if a == b]
        if len(common) == len(x) - 1:
            return ''.join(common)


print(f"P1: {part1(data)}")
print(f"P2: {part2(data)}")
