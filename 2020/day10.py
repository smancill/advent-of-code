#!/usr/bin/env python

from collections import defaultdict

with open("input10.txt") as f:
    jolts = sorted(int(l) for l in f)
    jolts = [0] + jolts + [jolts[-1] + 3]


def part1():
    diffs = {1: 0, 3: 0}
    for i in range(1, len(jolts)):
        diffs[jolts[i] - jolts[i-1]] += 1
    return diffs[1] * diffs[3]


def part2():
    diffs = defaultdict(lambda: 0)
    diffs[0] = 1
    for i in range(0, len(jolts)-1):
        # For each reachable number, accumulate the ways to reach it
        for j in range(i+1, len(jolts)):
            if jolts[j] - jolts[i] > 3:
                break
            diffs[jolts[j]] += diffs[jolts[i]]
    return diffs[jolts[-1]]


print(f"P1: {part1()}")
print(f"P2: {part2()}")
