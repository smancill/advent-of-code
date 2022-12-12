#!/usr/bin/env python

from collections.abc import Sequence
from typing import TextIO


def parse_data(f: TextIO) -> list[int]:
    # Boarding passes are actually binary numbers,
    # described in a fancy way
    to_binary = str.maketrans('FBLR', '0101')

    def parse_pass(line: str) -> int:
        bp = line.strip().translate(to_binary)
        return int(bp, 2)

    return [parse_pass(l) for l in f]


def part1(seats: Sequence[int]) -> int:
    return max(seats)


def part2(seats: Sequence[int]) -> int:
    # All seats are occupied sequentially except one somewhere in between,
    # so the sum of all the numbers in the expected sequence
    # minus the sum of all the scanned numbers
    # will give the one missing seat number
    all_seats = range(min(seats), max(seats) + 1)
    return sum(all_seats) - sum(seats)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
