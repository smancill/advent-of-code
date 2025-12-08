#!/usr/bin/env python

from typing import TextIO


def parse_data(f: TextIO) -> str:
    return f.read().rstrip()


def process_stream(stream: str) -> tuple[int, int]:
    level = 0
    score = 0
    garbage = False
    ignore = False
    removed = 0
    for c in stream:
        if ignore:
            ignore = False
        elif c == "!":
            ignore = True
        elif garbage:
            if c == ">":
                garbage = False
            else:
                removed += 1
        elif c == "<":
            garbage = True
        elif c == "{":
            level += 1
            score += level
        elif c == "}":
            level -= 1
    return (score, removed)


def part1(data: str) -> int:
    return process_stream(data)[0]


def part2(data: str) -> int:
    return process_stream(data)[1]


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
