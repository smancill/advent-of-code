#!/usr/bin/env python

from collections.abc import Sequence
from typing import Literal, TextIO

type Bit = Literal["1", "0"]
type Binary = str


def parse_data(f: TextIO) -> list[Binary]:
    return [ln.strip() for ln in f]


def dec(binary: Binary) -> int:
    return int("".join(binary), 2)


def count_bits(binaries: Sequence[Binary], i: int) -> tuple[Bit, Bit]:
    total = len(binaries)
    ones = sum(int(x[i]) for x in binaries)
    zeros = total - ones
    if ones >= zeros:
        return ("1", "0")
    return ("0", "1")


def part1(numbers: Sequence[Binary]) -> int:
    size = len(numbers[0])
    g_rate = ""
    e_rate = ""
    for i in range(size):
        g_bit, e_bit = count_bits(numbers, i)
        g_rate += g_bit
        e_rate += e_bit
    return dec(g_rate) * dec(e_rate)


def part2(numbers: Sequence[Binary]) -> int:
    def find_rating(k: int) -> Binary:
        size = len(numbers[0])
        cand = numbers
        for i in range(size):
            b = count_bits(cand, i)[k]
            cand = [n for n in cand if n[i] == b]
            if len(cand) == 1:
                break
        assert len(cand) == 1
        return cand[0]

    o_rating = find_rating(0)
    c_rating = find_rating(1)

    return dec(o_rating) * dec(c_rating)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
