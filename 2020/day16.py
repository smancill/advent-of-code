#!/usr/bin/env python

import math
import re
from collections.abc import Mapping, Sequence
from typing import TextIO, TypeAlias

Range: TypeAlias = tuple[int, int]
Fields: TypeAlias = Mapping[str, Sequence[Range]]
Ticket: TypeAlias = Sequence[int]


def parse_data(f: TextIO) -> tuple[Fields, Ticket, list[Ticket]]:
    def parse_field(line: str) -> tuple[str, list[Range]]:
        if match := re.match(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)", line):
            name, *limits = match.groups()
            a, b, c, d = map(int, limits)
            return name, [(a, b), (c, d)]
        raise ValueError(line)

    def parse_ticket(line: str) -> Ticket:
        return list(map(int, line.split(",")))

    sections = [s.splitlines() for s in f.read().split("\n\n")]

    fields = dict(parse_field(l) for l in sections[0])
    ticket = parse_ticket(sections[1][1])
    nearby = [parse_ticket(l) for l in sections[2][1:]]

    return fields, ticket, nearby


def _is_in_range(r: Sequence[Range], v: int) -> bool:
    return any(a <= v <= b for a, b in r)


def _is_valid_value(fields: Fields, v: int) -> bool:
    return any(_is_in_range(r, v) for r in fields.values())


def find_fields(
    fields: Fields, ticket: Ticket, nearby: Sequence[Ticket]
) -> dict[int, str]:
    # filter valid tickets
    valid = [t for t in nearby if all(_is_valid_value(fields, v) for v in t)]

    # collect the fields that match the values in every position
    candidates = {
        i: {f for f, r in fields.items() if all(_is_in_range(r, t[i]) for t in valid)}
        for i in range(len(ticket))
    }

    # reduce every set of candidates to a single field
    names = {}
    while candidates:
        # find the position with a single candidate
        i = next(i for i, s in candidates.items() if len(s) == 1)
        # set the field for the position
        names[i] = candidates[i].pop()
        # remove the field from all other candidates
        del candidates[i]
        for j in candidates:
            candidates[j].discard(names[i])

    return names


def part1(fields: Fields, _: Ticket, nearby: Sequence[Ticket]) -> int:
    return sum(v for t in nearby for v in t if not _is_valid_value(fields, v))


def part2(fields: Fields, ticket: Ticket, nearby: Sequence[Ticket]) -> int:
    names = find_fields(fields, ticket, nearby)
    return math.prod(
        v for i, v in enumerate(ticket) if names[i].startswith("departure")
    )


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(*data)}")
    print(f"P2: {part2(*data)}")


if __name__ == "__main__":
    main()
