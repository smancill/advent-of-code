#!/usr/bin/env python

import re

with open("input04.txt") as f:
    data = [[i.split(":") for i in pp.split()]
            for pp in f.read().split("\n\n")]


# Originally a set of field ids for Part 1, updated to dict for Part 2
valid_fields = {
    'byr': '19[2-9][0-9]|200[0-2]',
    'iyr': '201[0-9]|2020',
    'eyr': '202[0-9]|2030',
    'hgt': '(?:1[5-8][0-9]|19[0-3])cm|(?:5[9]|6[0-9]|7[0-6])in',
    'hcl': '#[0-9a-f]{6}',
    'ecl': 'amb|blu|brn|gry|grn|hzl|oth',
    'pid': '[0-9]{9}',
    'cid': '.*',
}


def is_valid_basic(passport):
    missing = set(valid_fields) - set(f for f, _ in passport)
    return not missing or missing == {"cid"}


def is_valid_full(passport):
    return (is_valid_basic(passport)
            and all(re.fullmatch(valid_fields[f], v) for f, v in passport))


def part1():
    return sum(1 for passport in data if is_valid_basic(passport))


def part2():
    return sum(1 for passport in data if is_valid_full(passport))


print(f"P1: {part1()}")
print(f"P2: {part2()}")
