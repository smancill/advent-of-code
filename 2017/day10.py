#!/usr/bin/env python

from functools import reduce
from operator import xor
from typing import TextIO


def parse_data(f: TextIO) -> str:
    return f.read().rstrip()


def core_algorithm(lengths: list[int], size: int = 256, rounds: int = 64) -> list[int]:
    numbers = list(range(size))
    pos = 0
    skip = 0
    for _ in range(rounds):
        for length in lengths:
            idx = [(pos + i) % size for i in range(length)]
            val = [numbers[i] for i in idx]
            for i, v in zip(idx, reversed(val), strict=True):
                numbers[i] = v
            pos += (length + skip) % size
            skip += 1
    return numbers


def knot_hash(data: str) -> str:
    lengths = [ord(c) for c in data] + [17, 31, 73, 47, 23]
    numbers = core_algorithm(lengths)
    output = [reduce(xor, numbers[i : i + 16]) for i in range(0, 256, 16)]
    return "".join(f"{x:02x}" for x in output)


def part1(data: str, n: int = 256) -> int:
    lengths = [int(v) for v in data.split(",")]
    numbers = core_algorithm(lengths, n, 1)
    return numbers[0] * numbers[1]


def part2(data: str) -> str:
    return knot_hash(data)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
