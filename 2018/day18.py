#!/usr/bin/env python3

from itertools import count

OPEN = '.'
TREES = '|'
LUMBERJACK = '#'


def read_acres():
    with open("input18.txt") as f:
        return [list(l.strip()) for l in f]


def show(acres):
    for r in acres:
        print(''.join(r))
    print()


def adj(acres, x, y):
    x0, x1 = max(0, x - 1), min(len(acres), x + 2)
    y0, y1 = max(0, y - 1), min(len(acres[x]), y + 2)
    return [acres[i][j]
            for i in range(x0, x1) for j in range(y0, y1)
            if (i, j) != (x, y)]


def update(acres):
    prev = [[i for i in r] for r in acres]

    for i in range(len(acres)):
        for j in range(len(acres[i])):
            a = adj(prev, i, j)
            if prev[i][j] == OPEN:
                n = sum(1 for k in a if k == TREES)
                if n >= 3:
                    acres[i][j] = TREES
            elif prev[i][j] == TREES:
                n = sum(1 for k in a if k == LUMBERJACK)
                if n >= 3:
                    acres[i][j] = LUMBERJACK
            elif prev[i][j] == LUMBERJACK:
                if not (LUMBERJACK in a and TREES in a):
                    acres[i][j] = OPEN


def value(acres):
    nt = sum(1 for r in acres for c in r if c == TREES)
    nl = sum(1 for r in acres for c in r if c == LUMBERJACK)
    return nt * nl


def part1():
    acres = read_acres()
    for t in range(10):
        update(acres)
    return value(acres)


def part2(minutes=1000000000):
    acres = read_acres()
    prev = {str(acres): 0}

    # Loop until finding a cycle
    for t in count(1):
        update(acres)
        s = str(acres)
        if s in prev:
            c = prev[s]
            m = (minutes - c) % (t - c)
            break
        prev[s] = t

    # Loop the cycle until reaching the final state
    for i in range(m):
        update(acres)

    return value(acres)


print(f"P1: {part1()}")
print(f"P2: {part2()}")
