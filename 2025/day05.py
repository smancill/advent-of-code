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

    section1, section2 = f.read().strip().split("\n\n")
    ranges = [parse_range(ln) for ln in section1.split("\n")]
    ingredients = [int(ln) for ln in section2.split("\n")]
    return (ranges, ingredients)


def part1(ranges: list[Range], ingredients: list[int]) -> int:
    def fresh(i: int) -> bool:
        return any(r.start <= i <= r.end for r in ranges)

    return sum(1 for i in ingredients if fresh(i))


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
