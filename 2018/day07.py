#!/usr/bin/env python3

from string import ascii_uppercase
from collections import defaultdict

with open("input07.txt") as f:
    data = [l.strip() for l in f]


def get_steps(data):
    steps = defaultdict(set)
    req = defaultdict(set)

    for l in data:
        w = l.split()
        f, t = w[1], w[7]
        steps[f].add(t)
        req[t].add(f)

    return steps, req


def part1(data):
    steps, req = get_steps(data)

    queue = {c for c in steps if not req[c]}
    order = []

    while queue:
        c = sorted(queue)[0]
        queue.remove(c)
        order.append(c)

        for i in steps[c]:
            req[i].remove(c)
            if not req[i]:
                queue.add(i)

    return ''.join(order)


def part2(data, workers=5, base_dur=60):
    steps, req = get_steps(data)

    queue = {c for c in steps if not req[c]}
    jobs = set()

    duration = {c: base_dur + (ord(c) - ord('A') + 1) for c in ascii_uppercase}
    start = {}
    t = 0

    while True:
        finished = {j for j in jobs if t - start[j] == duration[j]}
        jobs = jobs.difference(finished)

        for c in finished:
            for i in steps[c]:
                req[i].remove(c)
                if not req[i]:
                    queue.add(i)

        while queue and len(jobs) < workers:
            c = sorted(queue)[0]
            queue.remove(c)
            jobs.add(c)
            start[c] = t

        if not jobs:
            break

        t += 1

    return t


print(f"P1: {part1(data)}")
print(f"P2: {part2(data)}")
