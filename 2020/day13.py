#!/usr/bin/env python

import itertools
import math

with open("input13.txt") as f:
    estimate = int(f.readline())
    buses = [(i, int(b)) for i, b in enumerate(f.readline().strip().split(','))
             if b != 'x']


def part1():
    earlier = min((bus - estimate % bus, bus) for _, bus in buses)
    return earlier[0] * earlier[1]


def part2():
    # t = a × n + b,  n ∈ Z,  a = LCM(buses IDs)
    a, b = buses[0][1], 0
    for i, bus in buses[1:]:
        b = next(k + b for k in itertools.count(0, a) if (k + b + i) % bus == 0)
        a = math.lcm(a, bus)
    return b


print(f"P1: {part1()}")
print(f"P2: {part2()}")
