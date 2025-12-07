#!/usr/bin/env python

import re
from collections import Counter
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from typing import TextIO

type Point = tuple[int, int]
type Fabric = Mapping[Point, int]


@dataclass(frozen=True)
class Claim:
    id: int
    x: int
    y: int
    w: int
    h: int

    def points(self) -> Iterator[Point]:
        return ((self.x + j, self.y + i) for i in range(self.h) for j in range(self.w))


def parse_data(f: TextIO) -> tuple[list[Claim], Fabric]:
    def parse_claim(line: str) -> Claim:
        values = re.findall(r"-?\d+", line)
        return Claim(*map(int, values))

    def map_claims(claims: Sequence[Claim]) -> Fabric:
        return Counter(p for c in claims for p in c.points())

    claims = [parse_claim(l) for l in f]
    fabric = map_claims(claims)
    return claims, fabric


def unique_claim(fabric: Fabric, claim: Claim) -> bool:
    return all(fabric[p] < 2 for p in claim.points())


def part1(_: Sequence[Claim], fabric: Fabric) -> int:
    return sum(1 for v in fabric.values() if v > 1)


def part2(claims: Sequence[Claim], fabric: Fabric) -> int:
    return next(c.id for c in claims if unique_claim(fabric, c))


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(*data)}")
    print(f"P2: {part2(*data)}")


if __name__ == "__main__":
    main()
