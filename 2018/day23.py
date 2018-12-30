#!/usr/bin/env python3

import re

with open("input23.txt") as f:
    data = [tuple(map(int, re.findall(r'-?\d+', l))) for l in f]


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def part1(data):
    best = max(data, key=lambda x: x[3])
    return sum(1 for d in data if dist(d[:3], best[:3]) <= best[3])


print(f"P1: {part1(data)}")
