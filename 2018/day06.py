#!/usr/bin/env python3

from collections import Counter

with open("input06.txt") as f:
    coords = [tuple(map(int, l.split(','))) for l in f]


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


N = {}
T = {}

# Select bounding box
x0 = min(x for x, _ in coords)
x1 = max(x for x, _ in coords)
y0 = min(y for _, y in coords)
y1 = max(y for _, y in coords)

for i in range(y0, y1 + 1):
    for j in range(x0, x1 + 1):
        md = {(x, y): dist((y, x), (i, j)) for x, y in coords}
        c, d = min(md.items(), key=lambda i: i[1])
        ct = Counter(md.values())
        N[i, j] = c if ct[d] == 1 else None
        T[i, j] = sum(md.values())

# The areas of coords in the border of bounding box are infinite
exc = {None}
exc = exc.union({N[y0, k] for k in range(x0, x1 - x0 + 1)})
exc = exc.union({N[y1, k] for k in range(x0, x1 - x0 + 1)})
exc = exc.union({N[k, x0] for k in range(y0, y1 - y0 + 1)})
exc = exc.union({N[k, x1] for k in range(y0, y1 - y0 + 1)})

areas = Counter([v for v in N.values() if v not in exc])
print(f"P1: {areas.most_common()[0][1]}")

area = [i for i in T.items() if i[1] < 10000]
print(f"P2: {len(area)}")
