#!/usr/bin/env python

import itertools
import re
from collections import Counter
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from typing import Final, TextIO

RACE_DURATION: Final = 2503


@dataclass(frozen=True)
class Reindeer:
    name: str
    speed: int
    time: int
    rest: int


def parse_data(f: TextIO) -> list[Reindeer]:
    def parse_reindeer(line: str) -> Reindeer:
        name, stats = line.split(maxsplit=1)
        speed, time, rest = map(int, re.findall(r"\d+", stats))
        return Reindeer(name, speed, time, rest)

    return [parse_reindeer(l) for l in f]


def distance(deer: Reindeer, duration: int) -> Iterator[int]:
    steps = [deer.speed] * deer.time + [0] * deer.rest
    distance = itertools.accumulate(itertools.cycle(steps))
    return itertools.islice(distance, duration)


def part1(deers: Sequence[Reindeer], duration: int = RACE_DURATION) -> int:
    def final_distance(deer: Reindeer) -> int:
        *_, final = distance(deer, duration)
        return final

    return max(final_distance(deer) for deer in deers)


def part2(deers: Sequence[Reindeer], duration: int = RACE_DURATION) -> int:
    def distance(deer: Reindeer) -> Iterator[tuple[str, int]]:
        global distance
        return zip(itertools.repeat(deer.name), distance(deer, duration))

    scores: Counter[str] = Counter()
    for distances in zip(*map(distance, deers), strict=True):
        top = max(d for _, d in distances)
        leaders = [s for s, d in distances if d == top]
        scores.update(leaders)

    return max(scores.values())


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
