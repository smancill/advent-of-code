#!/usr/bin/env python

from collections import deque
from collections.abc import Sequence
from typing import TextIO


def parse_data(f: TextIO) -> list[int]:
    return [int(i) for i in f.read().split()]


def parse1(tree: deque[int]) -> int:
    nc = tree.popleft()
    nm = tree.popleft()

    mc = [parse1(tree) for _ in range(nc)]
    me = [tree.popleft() for _ in range(nm)]

    return sum(mc) + sum(me)


def parse2(tree: deque[int]) -> int:
    nc = tree.popleft()
    nm = tree.popleft()

    mc = {i + 1: parse2(tree) for i in range(nc)}
    me = [tree.popleft() for _ in range(nm)]

    if nc == 0:
        return sum(me)
    return sum(mc.get(i, 0) for i in me)


def part1(data: Sequence[int]) -> int:
    return parse1(deque(data))


def part2(data: Sequence[int]) -> int:
    return parse2(deque(data))


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
