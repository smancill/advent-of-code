#!/usr/bin/env python

import re
from collections.abc import Sequence
from typing import Final, TextIO, TypeAlias

Field: TypeAlias = tuple[str, str]
Passport: TypeAlias = Sequence[Field]


def parse_data(f: TextIO) -> list[Passport]:
    def parse_field(t: str) -> Field:
        n, v = t.split(":")
        return (n, v)

    def parse_passport(p: str) -> Passport:
        return [parse_field(t) for t in p.split()]

    return [parse_passport(p) for p in f.read().split("\n\n")]


# Originally a set of field ids for Part 1, updated to dict for Part 2
valid_fields: Final = {
    "byr": "19[2-9][0-9]|200[0-2]",
    "iyr": "201[0-9]|2020",
    "eyr": "202[0-9]|2030",
    "hgt": "(?:1[5-8][0-9]|19[0-3])cm|(?:5[9]|6[0-9]|7[0-6])in",
    "hcl": "#[0-9a-f]{6}",
    "ecl": "amb|blu|brn|gry|grn|hzl|oth",
    "pid": "[0-9]{9}",
    "cid": ".*",
}


def is_valid_basic(passport: Passport) -> bool:
    missing = set(valid_fields) - {"cid"} - {f for f, _ in passport}
    return not missing


def is_valid_full(passport: Passport) -> bool:
    return is_valid_basic(passport) and all(
        re.fullmatch(valid_fields[f], v) for f, v in passport
    )


def part1(passports: Sequence[Passport]) -> int:
    return sum(1 for p in passports if is_valid_basic(p))


def part2(passports: Sequence[Passport]) -> int:
    return sum(1 for p in passports if is_valid_full(p))


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
