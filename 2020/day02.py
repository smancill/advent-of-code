#!/usr/bin/env python

import re
from collections.abc import Sequence
from dataclasses import dataclass
from typing import NewType, TextIO


@dataclass(frozen=True)
class Policy:
    char: str
    low: int
    high: int


Password = NewType("Password", str)

type Entry = tuple[Password, Policy]


def parse_data(f: TextIO) -> list[Entry]:
    def parse_policy(tokens: list[str]) -> Policy:
        l, h, c = tokens
        return Policy(c, int(l), int(h))

    data = [re.split(r"[: -]", l) for l in f]
    return [(Password(pw), parse_policy(pol)) for *pol, _, pw in data]


def part1(data: Sequence[Entry]) -> int:
    def is_valid(pw: Password, pol: Policy) -> bool:
        return pol.low <= pw.count(pol.char) <= pol.high

    return sum(1 for pw, pol in data if is_valid(pw, pol))


def part2(data: Sequence[Entry]) -> int:
    def is_valid(pw: Password, pol: Policy) -> bool:
        return (pw[pol.low - 1] == pol.char) != (pw[pol.high - 1] == pol.char)

    return sum(1 for pw, pol in data if is_valid(pw, pol))


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
