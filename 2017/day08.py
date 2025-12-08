#!/usr/bin/env python

from collections import defaultdict
from operator import add, sub
from typing import TextIO


def parse_data(f: TextIO) -> list[str]:
    return [l.rstrip() for l in f.readlines()]


def execute(instructions: list[str]) -> tuple[int, int]:
    reg = defaultdict[str, int](int)
    m = 0
    for ins in instructions:
        r, op, v, _, cr, cop, cv = ins.split()
        if eval(f"reg[cr] {cop} {cv}"):
            fn = add if op == "inc" else sub
            reg[r] = fn(reg[r], int(v))
            m = max(m, reg[r])
    return (max(reg.values()), m)


def main() -> None:
    data = parse_data(open(0))

    max_end, max_all = execute(data)

    print(f"P1: {max_end}")
    print(f"P2: {max_all}")


if __name__ == "__main__":
    main()
