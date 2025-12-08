#!/usr/bin/env python

from collections.abc import Sequence
from typing import TextIO

type Signals = list[str]
type Digits = list[str]
type Entry = tuple[Signals, Digits]


def parse_data(f: TextIO) -> list[Entry]:
    def parse_entry(entry: str) -> Entry:
        signals, digits = entry.split(" | ")
        return (signals.split(), digits.split())

    return [parse_entry(l) for l in f.readlines()]


def decode_entry(signals: Signals, digits: Digits) -> int:
    wires = {len(s): set(s) for s in signals if len(s) in (2, 4)}
    number = ""
    for digit in digits:
        segments = set(digit)
        match len(segments), len(segments & wires[2]), len(segments & wires[4]):
            case 2, _, _:
                number += "1"
            case 3, _, _:
                number += "7"
            case 4, _, _:
                number += "4"
            case 5, 2, _:
                number += "3"
            case 5, 1, 3:
                number += "5"
            case 5, 1, 2:
                number += "2"
            case 6, 2, 4:
                number += "9"
            case 6, 2, 3:
                number += "0"
            case 6, 1, _:
                number += "6"
            case 7, _, _:
                number += "8"
            case _:
                raise AssertionError
    return int(number)


def part1(data: Sequence[Entry]) -> int:
    def count_known(digits: Digits) -> int:
        return sum(1 for d in digits if len(d) in (2, 3, 4, 7))

    return sum(count_known(digits) for _, digits in data)


def part2(data: Sequence[Entry]) -> int:
    return sum(decode_entry(s, d) for s, d in data)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
