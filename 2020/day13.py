#!/usr/bin/env python

import itertools
import math
from collections.abc import Sequence
from typing import TextIO


def parse_data(f: TextIO) -> tuple[int, list[str]]:
    line1, line2 = f.readlines()
    estimate = int(line1)
    schedule = line2.strip().split(",")
    return estimate, schedule


def part1(estimate: int, schedule: Sequence[str]) -> int:
    buses = [int(bus) for bus in schedule if bus != "x"]
    earlier = min((bus - estimate % bus, bus) for bus in buses)
    return earlier[0] * earlier[1]


def part2(_: int, schedule: Sequence[str]) -> int:
    buses = [(i, int(bus)) for i, bus in enumerate(schedule) if bus != "x"]
    # t = a × n + b,  n ∈ Z,  a = LCM(buses IDs)
    (_, a), b = buses[0], 0
    for i, bus in buses[1:]:
        b = next(k + b for k in itertools.count(0, a) if (k + b + i) % bus == 0)
        a = math.lcm(a, bus)
    return b


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(*data)}")
    print(f"P2: {part2(*data)}")


if __name__ == "__main__":
    main()
