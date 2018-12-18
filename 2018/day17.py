#!/usr/bin/env python3

import re

from itertools import count


with open("input17.txt") as f:
    data = f.readlines()


def print_scan(area):
    for r in area:
        print(''.join(r))


def read_scan(data):
    clay = []
    for line in data:
        m = re.match(r'x=(\d+), y=(\d+)..(\d+)', line)
        if m:
            x, y0, y1 = map(int, [m.group(i) for i in [1, 2, 3]])
            for y in range(y0, y1 + 1):
                clay.append((x, y))
        m = re.match(r'y=(\d+), x=(\d+)..(\d+)', line)
        if m:
            y, x0, x1 = map(int, [m.group(i) for i in [1, 2, 3]])
            for x in range(x0, x1 + 1):
                clay.append((x, y))

    x0, x1 = min(i[0] for i in clay), max(i[0] for i in clay)
    y0, y1 = min(i[1] for i in clay), max(i[1] for i in clay)

    # Extra columns because water may flow left/rigth of min/max veins
    x0, x1 = x0 - 1, x1 + 1

    sy, sx = (0, 500 - x0)

    area = [['.'] * (x1 - x0 + 1) for _ in range((y1 + 1) + 1)]

    area[sy][sx] = '+'
    for x, y in clay:
        area[y][x - x0] = '#'

    return area, (sy, sx), (y0, y1)


def fill_tiles(area, spring):
    down_queue = [spring]

    while down_queue:
        y, x = down_queue.pop()
        if area[y][x] == '~':
            continue

        spread_queue = []

        # flow down
        for i in range(y + 1, len(area)):
            if area[i][x] == '#' or area[i][x] == '~':
                spread_queue.append((i-1, x))
                break
            if area[i][x] == '|':
                break
            area[i][x] = '|'

        while spread_queue:
            y, x = spread_queue.pop()

            # flow left
            for j in count(x-1, -1):
                if area[y][j] == '#':
                    lx = j
                    break
                area[y][j] = '|'
                if area[y+1][j] == '.':
                    lx = j
                    break

            # flow right
            for j in count(x+1):
                if area[y][j] == '#':
                    rx = j
                    break
                area[y][j] = '|'
                if area[y+1][j] == '.':
                    rx = j
                    break

            # if contained between clay, fill and flow up
            if area[y][lx] == '#' and area[y][rx] == '#':
                for j in range(lx + 1, rx):
                    area[y][j] = '~'
                for j in range(lx + 1, rx):
                    if area[y-1][j] == '|':
                        spread_queue.append((y-1, j))
                        break
                continue

            # if not contained, flow down by the borders
            if area[y+1][lx] == '.':
                down_queue.append((y, lx))
            if area[y+1][rx] == '.':
                down_queue.append((y, rx))


def count_tiles(area, ylim, dry=False):
    w = '~' if dry else '~|'
    return sum(1 for i in range(ylim[0], ylim[1]+1) for c in area[i] if c in w)


area, spring, ylim = read_scan(data)
fill_tiles(area, spring)

print(f"P1: {count_tiles(area, ylim)}")
print(f"P2: {count_tiles(area, ylim, dry=True)}")
