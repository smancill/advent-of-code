#!/usr/bin/env python

from collections.abc import Callable, Sequence
from functools import reduce
from itertools import groupby
from operator import add, mul
from typing import Final, TextIO

type Numbers = list[int]
type TransformFn = Callable[[Sequence[str]], list[Numbers]]
type BinaryFn = Callable[[int, int], int]


FN: Final = {"+": add, "*": mul}


def parse_data(f: TextIO) -> list[str]:
    # Remove newline
    return [ln[:-1] for ln in f]


def numbers(row: str) -> Numbers:
    return list(map(int, row.split()))


def operators(row: str) -> list[BinaryFn]:
    return [FN[op] for op in row.split()]


def solve(data: Sequence[str], transform: TransformFn) -> int:
    num = transform(data[:-1])
    ops = operators(data[-1])
    return sum(reduce(o, n) for o, n in zip(ops, num, strict=True))


def part1(data: Sequence[str]) -> int:
    def transpose(rows: Sequence[str]) -> list[Numbers]:
        num = [numbers(r) for r in rows]
        return [list(t) for t in zip(*num, strict=True)]

    return solve(data, transpose)


def part2(data: Sequence[str]) -> int:
    def rotate(rows: Sequence[str]) -> list[Numbers]:
        col = ["".join(c).strip() for c in zip(*rows, strict=True)]
        rot = [" ".join(g) for _, g in groupby(col, lambda c: bool(c))]
        return [numbers(r) for r in rot if r]

    return solve(data, rotate)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
