#!/usr/bin/env python

from collections.abc import Sequence
from typing import TextIO

Command = tuple[str, int]


def parse_data(f: TextIO) -> list[Command]:
    return [(a, int(d)) for a, d in (l.split() for l in f)]


def run_commands(commands: Sequence[Command], use_aim: bool) -> int:
    x = y = u = 0
    for cmd, val in commands:
        match cmd:
            case "forward":
                x += val
                if use_aim:
                    u += y * val
            case "down":
                y += val
            case "up":
                y -= val
    return x * u if use_aim else x * y


def part1(data: Sequence[Command]) -> int:
    return run_commands(data, False)


def part2(data: Sequence[Command]) -> int:
    return run_commands(data, True)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
