#!/usr/bin/env python3

N = 300
SERIAL = int(open("input11.txt").read().strip())


def power_level(y, x):
    rack_id = x + 10
    level = (rack_id * y + SERIAL) * rack_id
    level = (level // 100) % 10
    return level - 5


# Optimize for fun with partial sums
# but brute force O(k^2 n^2) would do just fine for k=3
def max_fuel(grid, s):
    L = N - s + 1

    partial = [[0] * (N + 1) for _ in range(N+1)]
    for j in range(1, N+1):
        t = sum(grid[i, j] for i in range(1, s+1))
        partial[1][j] = t

        for i in range(2, L+1):
            t += grid[i+s-1, j] - grid[i-1, j]
            partial[i][j] = t

    m = (-1e6, 0, 0)  # fuel, y, x
    for i in range(1, L+1):
        t = sum(partial[i][j] for j in range(1, s+1))
        m = max((t, -i, -1), m)

        for j in range(2, L+1):
            t += partial[i][j+s-1] - partial[i][j-1]
            m = max((t, i, j), m)

    return m[1], m[2], m[0]


# Brute force would be O(n^5), too much.
# Use cumulative sums to make it O(n^3).
def max_fuel_dial(grid, start=1, end=N):
    C = [[0] * (N + 1) for _ in range(N+1)]
    for i in range(1, N+1):
        for j in range(1, N+1):
            C[i][j] = grid[i, j] + C[i-1][j] + C[i][j-1] - C[i-1][j-1]

    m = (-1e4, 0, 0, 0)  # fuel, size, y, x
    for s in range(start, end+1):
        for i in range(s, N+1):
            for j in range(s, N+1):
                f = C[i][j] - C[i][j-s] - C[i-s][j] + C[i-s][j-s]
                if f > m[0]:
                    m = (f, s, i-s+1, j-s+1)

    return m[2], m[3], m[1], m[0]


grid = {(i, j): power_level(i, j)
        for i in range(1, N + 1)
        for j in range(1, N + 1)}

y, x, _ = max_fuel(grid, 3)
print(f"P1: {x},{y}")

y, x, s, _ = max_fuel_dial(grid)
print(f"P2: {x},{y},{s}")
