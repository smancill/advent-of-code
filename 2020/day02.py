#!/usr/bin/env python

import collections
import re

Policy = collections.namedtuple('Policy', 'c l h')

with open("input02.txt") as f:
    data = [re.split(r'[: -]', l) for l in f]
    data = [(Policy(l[2], int(l[0]), int(l[1])), l[4]) for l in data]


def part1():
    def is_valid(pw, pol):
        return pol.l <= pw.count(pol.c) <= pol.h

    return sum(1 for pol, pw in data if is_valid(pw, pol))


def part2():
    def is_valid(pw, pol):
        return (pw[pol.l-1] == pol.c) != (pw[pol.h-1] == pol.c)

    return sum(1 for pol, pw in data if is_valid(pw, pol))


print(f"P1: {part1()}")
print(f"P2: {part2()}")
