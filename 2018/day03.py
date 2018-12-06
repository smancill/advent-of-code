#!/usr/bin/env python3

import re

from collections import defaultdict, namedtuple

Claim = namedtuple('Claim', ['id', 'x', 'y', 'w', 'h'])

with open("input03.txt") as f:
    claims = [Claim(*map(int, re.findall(r'-?\d+', l))) for l in f]


def map_claims(claims):
    fabric = defaultdict(int)
    for c in claims:
        for i in range(c.w):
            for j in range(c.h):
                fabric[c.x+i, c.y+j] += 1
    return fabric


def unique_claim(fabric, claim):
    for i in range(claim.w):
        for j in range(claim.h):
            if fabric[claim.x+i, claim.y+j] > 1:
                return False
    return True


fabric = map_claims(claims)

total = sum(1 for v in fabric.values() if v > 1)
print(f"P1: {total}")

for c in claims:
    if unique_claim(fabric, c):
        print(f"P2: {c.id}")
        break
