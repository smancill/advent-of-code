#!/usr/bin/env python

from typing import TextIO


def parse_data(f: TextIO) -> str:
    return f.read().rstrip()


def captcha(number: str, step: int) -> int:
    digits = [int(d) for d in number]
    pairs = zip(digits, digits[step:] + digits[:step], strict=True)
    return sum(i for i, j in pairs if i == j)


def part1(data: str) -> int:
    return captcha(data, 1)


def part2(data: str) -> int:
    return captcha(data, len(data) // 2)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
