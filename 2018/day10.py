#!/usr/bin/env python3

import re

from itertools import count

# list of [x, y, vx, vy]
points = [list(map(int, re.findall(r'-?\d+', l)))
          for l in open("input10.txt")]

for t in count(1):
    for p in points:
        p[0] += p[2]
        p[1] += p[3]

    x0, x1 = min(p[0] for p in points), max(p[0] for p in points)
    y0, y1 = min(p[1] for p in points), max(p[1] for p in points)

    # heuristic: message should fit in a small bounding box
    # minimum height found after running the program a few times
    if y1 - y0 <= 10:
        grid = {(p[1], p[0]): '#' for p in points}
        print(f"After {t} seconds:")
        for i in range(y0, y1 + 1):
            for j in range(x0, x1 + 1):
                print(grid.get((i, j), ' '), end='')
            print()
        print()
        break
