#!/usr/bin/env python

import math
import re

with open("input16.txt") as f:
    fields, ticket, nearby = f.read().split('\n\n')

    def parse_field(line):
        tokens = re.match(r'(.+): (\d+)-(\d+) or (\d+)-(\d+)', line).groups()
        return tokens[0], tuple(map(int, tokens[1:]))

    def read_ticket(ticket):
        return list(map(int, ticket.split(',')))

    fields = {n: r for n, r in (parse_field(l) for l in fields.splitlines())}
    ticket = read_ticket(ticket.splitlines()[1])
    nearby = [read_ticket(l) for l in nearby.splitlines()[1:]]


def in_range(r, v):
    return r[0] <= v <= r[1] or r[2] <= v <= r[3]


def is_valid_value(v):
    return any(in_range(r, v) for r in fields.values())


def part1():
    return sum(v for t in nearby for v in t if not is_valid_value(v))


def part2():
    # filter valid tickets
    valid = [t for t in nearby if all(is_valid_value(v) for v in t)]

    # collect the fields that match the values in every position
    candidates = {
        i: {f for f, r in fields.items() if all(in_range(r, t[i]) for t in valid)}
        for i in range(len(ticket))
    }

    # reduce every set of candidates to a single field
    names = {}
    while candidates:
        # find the position with a single candidate
        i = next(i for i, s in candidates.items() if len(s) == 1)
        # set the field for the position
        names[i] = candidates[i].pop()
        # remove the field from all other candidates
        del candidates[i]
        for j in candidates:
            candidates[j].discard(names[i])

    return math.prod(v for i, v in enumerate(ticket)
                     if names[i].startswith('departure'))


print(f"P1: {part1()}")
print(f"P2: {part2()}")
