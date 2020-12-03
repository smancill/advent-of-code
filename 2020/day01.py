#!/usr/bin/env python

import itertools
import math

with open("input01.txt") as f:
    data = [int(i) for i in f]


def find_entries(n):
    for entries in itertools.combinations(data, n):
        if sum(entries) == 2020:
            return math.prod(entries)


print(f"P1: {find_entries(2)}")
print(f"P2: {find_entries(3)}")
