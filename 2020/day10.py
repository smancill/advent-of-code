#!/usr/bin/env python

from collections import defaultdict
from collections.abc import Sequence
from typing import TextIO


def parse_data(f: TextIO) -> list[int]:
    jolts = sorted(int(l) for l in f)
    jolts = [0] + jolts + [jolts[-1] + 3]
    return jolts


def part1(jolts: Sequence[int]) -> int:
    diffs = {1: 0, 3: 0}
    for i in range(1, len(jolts)):
        diffs[jolts[i] - jolts[i - 1]] += 1
    return diffs[1] * diffs[3]


def part2(jolts: Sequence[int]) -> int:
    diffs = defaultdict(lambda: 0)
    diffs[0] = 1
    for i in range(0, len(jolts) - 1):
        # For each reachable number, accumulate the ways to reach it
        for j in range(i + 1, len(jolts)):
            if jolts[j] - jolts[i] > 3:
                break
            diffs[jolts[j]] += diffs[jolts[i]]
    return diffs[jolts[-1]]


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
