#!/usr/bin/env python

from functools import reduce

with open("input06.txt") as f:
    data = [[set(p) for p in g.split()]
            for g in f.read().split("\n\n")]


def part1():
    def n_answers(g):
        return len(reduce(lambda a, b: set.union(a, b), g))

    return sum(n_answers(group) for group in data)


def part2():
    def n_answers(g):
        return len(reduce(lambda a, b: set.intersection(a, b), g))

    return sum(n_answers(group) for group in data)


print(f"P1: {part1()}")
print(f"P2: {part2()}")
