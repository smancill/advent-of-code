#!/usr/bin/env python

from typing import NamedTuple, TextIO


class RepeatedConfig(NamedTuple):
    banks: list[int]
    cycle: int
    loop_size: int


def parse_data(f: TextIO) -> list[int]:
    return [int(l) for l in f.read().split()]


def reallocate(banks: list[int]) -> RepeatedConfig:
    n = len(banks)
    configs = {tuple(banks): 0}

    def most_blocks() -> tuple[int, int]:
        return max(enumerate(banks), key=lambda k: (k[1], -k[0]))

    def redistribute() -> None:
        i, m = most_blocks()
        banks[i] = 0
        for j in range(i + 1, i + 1 + m):
            banks[j % n] += 1

    cycles = 0
    while True:
        redistribute()
        cycles += 1
        key = tuple(banks)
        if key in configs:
            return RepeatedConfig(banks, cycles, cycles - configs[key])
        configs[key] = cycles


def main() -> None:
    data = parse_data(open(0))
    repeated = reallocate(data)

    print(f"P1: {repeated.cycle}")
    print(f"P2: {repeated.loop_size}")


if __name__ == "__main__":
    main()
