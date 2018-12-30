#!/usr/bin/env python3

import re

with open("input25.txt") as f:
    points = [tuple(map(int, re.findall(r'-?\d+', l))) for l in f]


def dist(a, b):
    return (abs(a[0] - b[0]) + abs(a[1] - b[1]) +
            abs(a[2] - b[2]) + abs(a[3] - b[3]))


def find_constelation(points, orig):
    group = set()
    queue = {orig}
    while queue:
        current = queue.pop()
        if current in group:
            continue
        group.add(current)
        for p in points[:]:
            if dist(current, p) <= 3:
                queue.add(p)
                points.remove(p)
    return group


def find_constelations(points):
    constelations = []
    queue = set(points)
    while queue:
        orig = queue.pop()
        const = find_constelation(points, orig)
        queue -= const
        constelations.append(const)
    return constelations


constelations = find_constelations(points)

print(len(constelations))
