#!/usr/bin/env python

from typing import TextIO


def parse_data(f: TextIO) -> list[str]:
    return [l.rstrip() for l in f.readlines()]


def no_duplicates(password: str) -> bool:
    words = password.split()
    return len(set(words)) == len(words)


def no_anagrams(password: str) -> bool:
    def sort_letters(word: str) -> str:
        return "".join(sorted(word))

    words = password.split()
    unique = set(map(sort_letters, words))

    return len(unique) == len(words)


def part1(passwords: list[str]) -> int:
    return sum(1 for pw in passwords if no_duplicates(pw))


def part2(passwords: list[str]) -> int:
    return sum(1 for pw in passwords if no_anagrams(pw))


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
