#!/usr/bin/env python3

from collections import Counter


with open("input13.txt") as f:
    data = [l.rstrip() for l in f]

D = {'>': (0, 1), '<': (0, -1), 'v': (1, 0), '^': (-1, 0)}

TS = {'>': '^', '^': '>', '<': 'v', 'v': '<'}
TB = {'>': 'v', '^': '<', '<': '^', 'v': '>'}
TI = {'>': '^>v', '<': 'v<^', 'v': '>v<', '^': '<^>'}


class Cart:
    def __init__(self, pos, dir):
        self.pos = pos
        self.dir = dir
        self.turn = 0


def parse(data):
    tracks = []
    carts = []
    for i in range(len(data)):
        row = []
        for j in range(len(data[i])):
            c = data[i][j]
            if c in '<>v^':
                carts.append(Cart((i, j), c))
                p = {'<': '-', '>': '-', 'v': '|', '^': '|'}
                row.append(p[c])
            else:
                row.append(c)
        tracks.append(row)
    return tracks, carts


def show(tracks):
    for i in range(len(tracks)):
        print(''.join(tracks[i]))


def move(tracks, carts):
    for c in carts:
        cy, cx = c.pos
        dy, dx = D[c.dir]
        ny, nx = cy + dy, cx + dx
        np = tracks[ny][nx]

        c.pos = ny, nx
        if np == '+':
            c.dir = TI[c.dir][c.turn]
            c.turn = (c.turn + 1) % 3
        elif np == '/':
            c.dir = TS[c.dir]
        elif np == '\\':
            c.dir = TB[c.dir]


def crashes(carts):
    ct = Counter(c.pos for c in carts)
    return [i[0] for i in ct.most_common() if i[1] > 1]


def coords(point):
    return f"{point[1]},{point[0]}"


def part1():
    tracks, carts = parse(data)
    while True:
        move(tracks, carts)
        for p in crashes(carts):
            return coords(p)


def part2():
    tracks, carts = parse(data)
    while carts:
        move(tracks, carts)
        for p in crashes(carts):
            carts = [c for c in carts if c.pos != p]
        if len(carts) == 1:
            return coords(carts[0].pos)


print(f"P1: {part1()}")
print(f"P2: {part2()}")
