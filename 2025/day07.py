#!/usr/bin/env python

from collections.abc import Sequence
from typing import NamedTuple, TextIO


def parse_data(f: TextIO) -> list[str]:
    return [ln.strip() for ln in f]


class Result(NamedTuple):
    splits: int
    timelines: int


def manifold(diagram: Sequence[str]) -> Result:
    width = len(diagram[0])
    start = diagram[0].find("S")

    beams = {start}
    splits = 0
    timelines = [0] * width
    timelines[start] = 1

    for row in diagram[1:]:
        splitters = {i for i, c in enumerate(row) if c == "^"}
        hits = beams & splitters

        if hits:
            free = beams - hits
            branches = {i - 1 for i in hits} | {i + 1 for i in hits}
            beams = free | branches

            splits += len(hits)

            current = [0] * width
            for i in hits:
                current[i - 1] += timelines[i]
                current[i + 1] += timelines[i]
            for i in free:
                current[i] += timelines[i]
            timelines = current

    return Result(splits, sum(timelines))


def part1(result: Result) -> int:
    return result.splits


def part2(result: Result) -> int:
    return result.timelines


def main() -> None:
    data = parse_data(open(0))
    result = manifold(data)

    print(f"P1: {part1(result)}")
    print(f"P2: {part2(result)}")


if __name__ == "__main__":
    main()
