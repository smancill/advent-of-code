#!/usr/bin/env python

import math
import collections

TOP, RIGHT, BOTTOM, LEFT = 't', 'r', 'b', 'l'

SIDES = [TOP, RIGHT, BOTTOM, LEFT]

MONSTER = [
    '                  # ',
    '#    ##    ##    ###',
    ' #  #  #  #  #  #   ',
]


def orientate_until(img, cond):
    for n in range(8):
        if cond(img):
            break
        img.rotate()
        if n == 3:
            img.flip()


class RawImage:

    def __init__(self, data):
        self.data = [''.join(r) for r in data]

    def rotate(self):
        """ Rotate 90 degress. """

        # Transpose
        t = []
        for i in range(len(self.data)):
            t.append([])
            for j in range(len(self.data[0])):
                t[i].append(self.data[j][i])

        # Reverse each row
        self.data = [''.join(reversed(r)) for r in t]

    def flip(self):
        """ Flip vertically. """
        self.data = self.data[::-1]

    def __str__(self):
        return '\n'.join(self.data)


class Tile(RawImage):

    def __init__(self, data):
        super().__init__(data[1:])
        self.id = int(data[0].split()[1][:-1])

    def border(self, side):
        if side == TOP:
            return self.data[0]
        elif side == RIGHT:
            return ''.join(r[-1] for r in self.data)
        elif side == BOTTOM:
            return self.data[-1]
        elif side == LEFT:
            return ''.join(r[0] for r in self.data)


class ImageAssembler:

    def assemble(self, tiles):
        assembled = []

        self._map_adj(tiles)
        prev = self._top_corner(tiles)
        row = [prev]
        while True:
            sides = (BOTTOM, TOP) if len(row) == 0 else (RIGHT, LEFT)
            adj = self._find_adj(prev, sides)
            row.append(adj)
            if not self._has_adj(adj, RIGHT):
                assembled.append(row)
                if not self._has_adj(adj, BOTTOM):
                    break
                prev = row[0]
                row = []
            else:
                prev = adj

        return assembled

    def show(tiles):
        for tr in tiles:
            for i in range(len(tr[0].data)):
                print(' '.join(t.data[i] for t in tr))
            print()

    def _map_adj(self, tiles):
        self._adj = collections.defaultdict(set)
        for t in tiles.values():
            for s in SIDES:
                b = t.border(s)
                for k in (b, b[::-1]):
                    self._adj[k].add(t.id)

    def _top_corner(self, tiles):
        def count_adj(t):
            return sum(1 for s in SIDES if self._has_adj(t, s))

        def top_corner(t):
            return all(not self._has_adj(t, b) for b in (LEFT, TOP))

        corner = next(t for t in tiles.values() if count_adj(t) == 2)
        orientate_until(corner, top_corner)
        return corner

    def _find_adj(self, tile, sides):
        border = tile.border(sides[0])
        cand = self._adj[border] - {tile.id}
        adj = tiles[cand.pop()]
        orientate_until(adj, lambda t: border == t.border(sides[1]))
        return adj

    def _has_adj(self, tile, side):
        return len(self._adj[tile.border(side)]) > 1


class Image(RawImage):

    def __init__(self, tiles):
        super().__init__(''.join(t.data[i][1:-1] for t in tr)
                         for tr in tiles for i in range(1, len(tr[0].data) - 1))

    def find_monsters(self, monster):
        def to_bin(s):
            return int(s.translate(str.maketrans('#. ', '100')), 2)

        n_monsters = 0
        mr, mc = len(monster), len(monster[0])
        monster = [to_bin(r) for r in monster]

        for i in range(len(self.data) - mr + 1):
            for j in range(len(self.data[0]) - mc + 1):
                area = [to_bin(self.data[x][j:j+mc]) for x in range(i, i + mr)]
                if all(area[x] & monster[x] == monster[x] for x in range(mr)):
                    n_monsters += 1

        return n_monsters


with open("input20.txt") as f:
    tiles = [Tile(t.splitlines()) for t in f.read().strip().split('\n\n')]
    tiles = {t.id: t for t in tiles}

assembled = ImageAssembler().assemble(tiles)
img = Image(assembled)


def part1():
    corners = [(0, 0), (0, -1), (-1, 0), (-1, -1)]
    return math.prod(assembled[i][j].id for i, j in corners)


def part2():
    def count_waters(d):
        return sum(1 for r in d for v in r if v == '#')

    def find_monsters():
        def wrapped(img):
            n[0] = img.find_monsters(MONSTER)
            return n[0] > 0
        return wrapped

    n = [0]
    orientate_until(img, find_monsters())

    return count_waters(img.data) - n[0] * count_waters(MONSTER)


print(f"P1: {part1()}")
print(f"P2: {part2()}")
