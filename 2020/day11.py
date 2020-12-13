#!/usr/bin/env python

import itertools

FLOOR = '.'
EMPTY = 'L'
OCCUPIED = '#'

DIRECTIONS = set(itertools.product(range(-1, 2), range(-1, 2))) - {(0, 0)}


def read_layout():
    with open("input11.txt") as f:
        return [list(l.strip()) for l in f]


def show_layout(layout):
    for r in layout:
        print(''.join(r))
    print()


def valid_pos(m, x, y):
    return 0 <= x < len(m) and 0 <= y < len(m[x])


def n_occupied(layout):
    return sum(1 for r in layout for s in r if s == OCCUPIED)


def update(layout, fn, tolerance):
    prev = [[s for s in r] for r in layout]
    changed = False

    for x in range(len(layout)):
        for y in range(len(layout[0])):
            n = sum(1 for d in DIRECTIONS if fn(prev, x, y, *d) == OCCUPIED)
            if prev[x][y] == EMPTY:
                if n == 0:
                    layout[x][y] = OCCUPIED
                    changed = True
            elif prev[x][y] == OCCUPIED:
                if n >= tolerance:
                    layout[x][y] = EMPTY
                    changed = True

    return not changed


def part1():
    def find_seat(layout, x, y, dx, dy):
        x, y = x + dx, y + dy
        if valid_pos(layout, x, y):
            return layout[x][y]

    layout = read_layout()
    while True:
        if update(layout, find_seat, 4):
            return n_occupied(layout)


def part2():
    def find_seat(layout, x, y, dx, dy):
        pos = zip(itertools.count(x, dx), itertools.count(y, dy))
        for i, j in itertools.islice(pos, 1, None):
            if not valid_pos(layout, i, j):
                return None
            if layout[i][j] in (EMPTY, OCCUPIED):
                return layout[i][j]

    layout = read_layout()
    while True:
        if update(layout, find_seat, 5):
            return n_occupied(layout)


print(f"P1: {part1()}")
print(f"P2: {part2()}")
