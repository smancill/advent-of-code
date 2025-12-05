#!/usr/bin/env python

from typing import NamedTuple, TextIO


class Range(NamedTuple):
    """Inclusive range."""

    start: int
    end: int


def parse_data(f: TextIO) -> tuple[list[Range], list[int]]:
    def parse_range(ln: str) -> Range:
        s, e = map(int, ln.split("-"))
        return Range(s, e)

    part1, part2 = f.read().strip().split("\n\n")
    ranges = [parse_range(ln) for ln in part1.split("\n")]
    ingred = [int(ln) for ln in part2.split("\n")]
    return (ranges, ingred)


def part1(ranges: list[Range], ingredients: list[int]) -> int:
    def is_fresh(i: int) -> bool:
        return any(r.start <= i <= r.end for r in ranges)

    return sum(1 for i in ingredients if is_fresh(i))


def part2(ranges: list[Range]) -> int:
    total, last = 0, 0

    for r in sorted(ranges):
        if last >= r.end:
            continue

        if last >= r.start:
            start, end = last + 1, r.end
        else:
            start, end = r.start, r.end

        total += end - start + 1
        last = end

    return total


def main() -> None:
    ranges, ingredients = parse_data(open(0))

    print(f"P1: {part1(ranges, ingredients)}")
    print(f"P2: {part2(ranges)}")


if __name__ == "__main__":
    main()
