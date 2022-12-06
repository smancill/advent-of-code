#!/usr/bin/env python

from typing import TextIO


def parse_data(f: TextIO) -> str:
    return f.read().rstrip()


def detect_marker(data: str, size: int) -> int:
    def marker_at(i: int) -> bool:
        return len(set(data[i : i + size])) == size

    return next(i + size for i in range(len(data) - size) if marker_at(i))


def part1(data: str) -> int:
    return detect_marker(data, 4)


def part2(data: str) -> int:
    return detect_marker(data, 14)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
