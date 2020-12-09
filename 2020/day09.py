#!/usr/bin/env python

from itertools import combinations

with open("input09.txt") as f:
    data = [int(l) for l in f]

S = 25


def is_valid(i):
    return any(a + b == data[i] for a, b in combinations(data[i-S:i+1], 2))


def part1():
    return next(data[i] for i in range(S, len(data)) if not is_valid(i))


def part2():
    inv = part1()
    for i in range(len(data)):
        j = i + 1
        sum = data[i]
        while True:
            sum += data[j]
            if sum == inv:
                sub = data[i:j+1]
                return min(sub) + max(sub)
            elif sum > inv:
                break
            else:
                j += 1


print(f"P1: {part1()}")
print(f"P2: {part2()}")
