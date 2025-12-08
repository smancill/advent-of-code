#!/usr/bin/env python

from collections import deque
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from functools import reduce
from typing import Final, TextIO

MATCH: Final = {"(": ")", "[": "]", "{": "}", "<": ">"}


@dataclass
class Line:
    valid: bool
    stack: list[str]


def read_data(f: TextIO) -> list[str]:
    return [ln.strip() for ln in f]


def parse_lines(data: Sequence[str]) -> Iterator[Line]:
    def parse(line: str) -> Line:
        stack = deque[str]()
        for c in line:
            if c in MATCH:
                stack.append(c)
            else:
                o = stack.pop()
                if c != MATCH[o]:
                    return Line(False, [c])
        return Line(True, [MATCH[c] for c in reversed(stack)])

    return (parse(ln) for ln in data)


def part1(data: Sequence[str]) -> int:
    points = {")": 3, "]": 57, "}": 1197, ">": 25137}

    def score(line: Line) -> int:
        return points[line.stack[0]]

    return sum(score(ln) for ln in parse_lines(data) if not ln.valid)


def part2(data: Sequence[str]) -> int:
    points = {")": 1, "]": 2, "}": 3, ">": 4}

    def score(line: Line) -> int:
        return reduce(lambda a, b: a * 5 + points[b], line.stack, 0)

    scores = [score(ln) for ln in parse_lines(data) if ln.valid]
    return sorted(scores)[len(scores) // 2]


def main() -> None:
    data = read_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
