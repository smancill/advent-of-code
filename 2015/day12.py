#!/usr/bin/env python

import json
from typing import TextIO


def parse_data(f: TextIO) -> str:
    return f.read().strip()


def sum_numbers(data: str, ignore: str = "") -> int:
    total = 0
    stack = [json.loads(data)]
    while stack:
        match stack.pop():
            case dict(d):
                if ignore in (v := d.values()):
                    continue
                stack.extend(v)
            case list(l):
                stack.extend(l)
            case str():
                continue
            case int(v):
                total += v
            case o:
                raise ValueError(o)
    return total


def part1(data: str) -> int:
    return sum_numbers(data)


def part2(data: str, ignore: str = "red") -> int:
    return sum_numbers(data, ignore)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
