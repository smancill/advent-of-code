#!/usr/bin/env python

from collections import defaultdict
from collections.abc import Sequence
from string import ascii_uppercase
from typing import TextIO, TypeAlias

Graph: TypeAlias = dict[str, set[str]]


def read_data(f: TextIO) -> list[str]:
    return [l.rstrip() for l in f]


def parse_steps(data: Sequence[str]) -> tuple[Graph, Graph]:
    steps = defaultdict(set)
    deps = defaultdict(set)

    for line in data:
        w = line.split()
        p, s = w[1], w[7]
        steps[p].add(s)
        deps[s].add(p)

    return steps, deps


def part1(data: Sequence[str]) -> str:
    steps, deps = parse_steps(data)

    order = []
    queue = {s for s in steps if s not in deps}

    while queue:
        # Get a new available step
        c = sorted(queue)[0]
        queue.remove(c)

        # Mark step as completed
        order.append(c)

        # Remove completed step from requirements
        # Add ready steps to the queue
        for s in steps[c]:
            deps[s].remove(c)
            if not deps[s]:
                queue.add(s)

    return "".join(order)


def part2(data: Sequence[str], workers: int = 5, base_dur: int = 60) -> int:
    steps, deps = parse_steps(data)

    queue = {s for s in steps if s not in deps}
    jobs: set[str] = set()

    duration = {c: base_dur + (ord(c) - ord("A") + 1) for c in ascii_uppercase}
    start: dict[str, int] = {}
    t = 0

    while True:
        # Process completed steps
        completed = {j for j in jobs if t - start[j] == duration[j]}
        jobs -= completed

        # Remove completed step from requirements
        # Add ready steps to the queue
        for c in completed:
            for s in steps[c]:
                deps[s].remove(c)
                if not deps[s]:
                    queue.add(s)

        # Start as many jobs as available workers
        while queue and len(jobs) < workers:
            c = sorted(queue)[0]
            queue.remove(c)
            jobs.add(c)
            start[c] = t

        # If there are no jobs runnings, all steps were completed
        if not jobs:
            break

        t += 1

    return t


def main() -> None:
    data = read_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
