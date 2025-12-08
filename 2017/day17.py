#!/usr/bin/env python

from collections import deque
from typing import TextIO


def parse_data(f: TextIO) -> int:
    return int(f.read())


def part1(steps: int, last: int = 2017) -> int:
    buffer = deque([0])
    for i in range(1, last + 1):
        buffer.rotate(-steps)
        buffer.append(i)
    return buffer[0]


def part2(steps: int, last: int = 50_000_000) -> int:
    v = None
    i = 0
    for n in range(1, last + 1):
        i = (i + steps) % n + 1
        # 0 always stays at i=0, so the answer will be at i=1
        if i == 1:
            v = n
    assert v is not None
    return v


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
