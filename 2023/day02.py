#!/usr/bin/env python

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from math import prod
from typing import TextIO

type Play = Counter[str]


@dataclass(frozen=True)
class Game:
    id: int
    plays: list[Play]


def parse_data(f: TextIO) -> list[Game]:
    def parse_id(s: str) -> int:
        _, id = s.split()
        return int(id)

    def parse_cubes(s: str) -> Play:
        colors = [c.split() for c in s.split(", ")]
        return Counter({c: int(n) for n, c in colors})

    def parse_plays(s: str) -> list[Play]:
        return [parse_cubes(p) for p in s.split("; ")]

    def parse_game(s: str) -> Game:
        game, plays = s.split(": ")
        return Game(parse_id(game), parse_plays(plays))

    return [parse_game(s) for s in f]


def part1(data: Sequence[Game]) -> int:
    limit = Counter(red=12, green=13, blue=14)

    def check_game(game: Game) -> bool:
        return all(p <= limit for p in game.plays)

    return sum(game.id for game in data if check_game(game))


def part2(data: Sequence[Game]) -> int:
    def min_cubes(game: Game) -> dict[str, int]:
        total = Counter(red=0, green=0, blue=0)
        for play in game.plays:
            total |= play  # max(total[k], play[k])
        return total

    def power(game: Game) -> int:
        cubes = min_cubes(game)
        return prod(n for n in cubes.values())

    return sum(power(game) for game in data)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
