#!/usr/bin/env python

import re
from string import ascii_lowercase
from typing import Final, TextIO


def parse_data(f: TextIO) -> str:
    return f.read().strip()


def _rule1(password: str) -> bool:
    return any(password[i : i + 3] in ascii_lowercase for i in range(len(password) - 2))


def _rule2(password: str) -> bool:
    return all(c not in password for c in "ilo")


def _rule3(password: str) -> bool:
    return len(re.findall(r"([a-z])\1", password)) >= 2


_rules: Final = [_rule1, _rule2, _rule3]


def is_valid(password: str) -> bool:
    return all(rule(password) for rule in _rules)


def new_password(password: str) -> str:
    def increase() -> str:
        return re.sub(
            r"([a-y])(z*)$",
            lambda m: chr(ord(m[1]) + 1) + "a" * len(m[2]),
            password,
        )

    def optimize_search() -> str:
        return re.sub(r"([ilo])(.*)", lambda m: m[1] + "z" * len(m[2]), password)

    password = optimize_search()
    while True:
        password = increase()
        if is_valid(password):
            return password
        password = optimize_search()


def main() -> None:
    old = parse_data(open(0))

    new1 = new_password(old)
    new2 = new_password(new1)

    print(f"P1: {new1}")
    print(f"P2: {new2}")


if __name__ == "__main__":
    main()
