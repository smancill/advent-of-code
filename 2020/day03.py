#!/usr/bin/env python

import itertools
import math

with open("input03.txt") as f:
    data = [l.strip() for l in f]

slopes = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]


def count_trees(dx, dy):
    w = len(data[0])
    # assuming it will exactly end at the last row
    iy = range(0, len(data), dy)
    ix = itertools.count(0, dx)
    return sum(1 for y, x in zip(iy, ix) if data[y][x % w] == '#')


def part1():
    return count_trees(*slopes[1])


def part2():
    return math.prod(count_trees(*slope) for slope in slopes)


print(f"P1: {part1()}")
print(f"P1: {part2()}")
