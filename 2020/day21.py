#!/usr/bin/env python

import re

with open("input21.txt") as f:
    foods = [re.fullmatch(r'(.*) \(contains (.*)\)\n', l).groups() for l in f]
    foods = [(set(i.split()), set(a.split(', '))) for i, a in foods]


def find_allergic_ingredients(foods):
    reduced = {}
    cand = [(a, set.intersection(*(fi for fi, fa in foods if a in fa)))
            for a in sorted(set.union(*(fa for _, fa in foods)))]

    while cand:
        a, s = cand.pop(0)
        if len(s) == 1:
            i = next(iter(s))
            reduced[i] = a
        else:
            s -= set(reduced)
            cand.append((a, s))

    return dict(sorted(reduced.items(), key=lambda t: t[1]))


def part1():
    allergic = set(find_allergic_ingredients(foods))
    return sum(len(ingredients - allergic) for ingredients, _ in foods)


def part2():
    return ','.join(find_allergic_ingredients(foods))


print(f"P1: {part1()}")
print(f"P2: {part2()}")
