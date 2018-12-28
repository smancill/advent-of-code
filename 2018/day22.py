#!/usr/bin/env python3

from heapq import heappush, heappop

with open("input22.txt") as f:
    data = [l.split()[-1] for l in f]
    depth = int(data[0])
    target = tuple(map(int, data[1].split(',')))

ROCKY, WET, NARROW = 0, 1, 2
TORCH, GEAR, NEITHER = 0, 1, 2


class Region:
    def __init__(self, geo_idx, depth):
        self.ero_level = (geo_idx + depth) % 20183
        self.risk_level = self.ero_level % 3


def map_cave(depth, target):
    tx, ty = target
    mx, my = tx + 200, ty + 200  # may need adjustment if input changes

    cave = [[None] * mx for _ in range(my)]

    for i in range(1, my):
        gi = i * 48271
        cave[i][0] = Region(gi, depth)

    for j in range(1, mx):
        gi = j * 16807
        cave[0][j] = Region(gi, depth)

    for i in range(1, my):
        for j in range(1, mx):
            gi = cave[i-1][j].ero_level * cave[i][j-1].ero_level
            cave[i][j] = Region(gi, depth)

    cave[0][0] = Region(0, depth)
    cave[ty][tx] = Region(0, depth)

    return cave


def show(cave, target):
    regions = {ROCKY: '.', WET: '=', NARROW: '|'}

    tx, ty = target
    for i in range(0, ty + 1):
        for j in range(0, tx + 1):
            if (i, j) == (0, 0):
                print('M', end='')
            elif (i, j) == (ty, tx):
                print('T', end='')
            else:
                print(regions[cave[i][j].risk_level], end='')
        print()


def risk_level(cave, target):
    return sum(cave[i][j].risk_level
               for i in range(0, target[1] + 1)
               for j in range(0, target[0] + 1))


def rescue(cave, target):
    tools = {
        ROCKY: (GEAR, TORCH),
        WET: (GEAR, NEITHER),
        NARROW: (TORCH, NEITHER)
    }
    regions = {
        TORCH: (ROCKY, NARROW),
        GEAR: (ROCKY, WET),
        NEITHER: (WET, NARROW)
    }

    def dist(y, x):
        return abs(ty - y) + abs(tx - x)

    tx, ty = target
    queue = [(0, 0, 0, 0, TORCH)]  # (heuristic, time, y, x, tool)
    visited = dict()

    while queue:
        _, time, y, x, tool = heappop(queue)
        best = y, x, tool

        if best == (ty, tx, TORCH):
            return time

        if best in visited and visited[best] <= time:
            continue

        visited[best] = time

        # Try reachable regions
        for i, j in [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]:
            if i < 0 or j < 0:
                continue
            if cave[i][j].risk_level in regions[tool]:
                cost = time + 1
                heur = cost + dist(i, j)
                heappush(queue, (heur, cost, i, j, tool))

        # Try switching tool
        for t in tools[cave[y][x].risk_level]:
            if t != tool:
                cost = time + 7
                heur = cost + dist(y, x)
                heappush(queue, (heur, cost, y, x, t))


cave = map_cave(depth, target)

print(f"P1: {risk_level(cave, target)}")
print(f"P2: {rescue(cave, target)}")
