#!/usr/bin/env python3

from collections import defaultdict

with open("input20.txt") as f:
    regex = f.read().strip()


dist = {(0, 0): 0}
doors = defaultdict(set)


# This is not necessary to solve the problem
# but implemented anyway as exercise
def show():
    x0, x1 = min(x for x, _ in dist), max(x for x, _ in dist)
    y0, y1 = min(y for _, y in dist), max(y for _, y in dist)

    h = 2 * (x1 - x0 + 1) + 1
    w = 2 * (y1 - y0 + 1) + 1

    room_map = [['#'] * w for _ in range(h)]

    def map_row(i):
        x = (i - x0) * 2 + 1
        for j in range(y0, y1+1):
            y = (j - y0) * 2 + 1
            room_map[x][y] = '.' if (i, j) != (0, 0) else 'X'
            room_map[x][y+1] = '|' if (i, j+1) in doors[i, j] else '#'

    def map_sep(i):
        x = (i - x0) * 2 + 1
        for j in range(y0, y1+1):
            y = (j - y0) * 2 + 1
            room_map[x+1][y] = '-' if (i+1, j) in doors[i, j] else '#'

    for i in range(x0, x1):
        map_row(i)
        map_sep(i)
    map_row(x1)

    print('\n'.join(''.join(r) for r in room_map))


def move(p, m):
    if m == 'N':
        n = p[0] - 1, p[1]
    elif m == 'W':
        n = p[0], p[1] - 1
    elif m == 'E':
        n = p[0], p[1] + 1
    elif m == 'S':
        n = p[0] + 1, p[1]

    d = dist[p] + 1
    if n not in dist or dist[n] > d:
        dist[n] = d

    doors[p].add(n)
    doors[n].add(p)

    return n


def parse():
    pos = {(0, 0)}

    stack = []
    start = set()
    end = set()

    for c in regex[1:-1]:
        if c == '(':
            stack.append((start, end))
            start = pos
            end = set()
        elif c == '|':
            end.update(pos)
            pos = start
        elif c == ')':
            pos.update(end)
            start, end = stack.pop()
        else:
            pos = {move(p, c) for p in pos}


parse()

print(f"P1: {max(dist.values())}")
print(f"P2: {sum(1 for x in dist.values() if x >= 1000)}")
