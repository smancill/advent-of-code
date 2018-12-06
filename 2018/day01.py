#!/usr/bin/env python3

from itertools import accumulate, cycle

data = [int(l) for l in open("input01.txt")]

print(f"P1: {sum(data)}")

freqs = {0}
for f in accumulate(cycle(data)):
    if f in freqs:
        print(f"P2: {f}")
        break
    freqs.add(f)
