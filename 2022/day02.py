#!/usr/bin/env python

from collections.abc import Mapping, Sequence
from enum import Enum
from typing import Final, TextIO


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Result(Enum):
    LOSE = 0
    DRAW = 3
    WIN = 6


type Round = tuple[str, str]


ROUND_RESULT: Final[Mapping[tuple[Shape, Shape], Result]] = {
    (Shape.ROCK, Shape.ROCK): Result.DRAW,
    (Shape.ROCK, Shape.PAPER): Result.WIN,
    (Shape.ROCK, Shape.SCISSORS): Result.LOSE,
    (Shape.PAPER, Shape.ROCK): Result.LOSE,
    (Shape.PAPER, Shape.PAPER): Result.DRAW,
    (Shape.PAPER, Shape.SCISSORS): Result.WIN,
    (Shape.SCISSORS, Shape.ROCK): Result.WIN,
    (Shape.SCISSORS, Shape.PAPER): Result.LOSE,
    (Shape.SCISSORS, Shape.SCISSORS): Result.DRAW,
}


def parse_data(f: TextIO) -> list[Round]:
    def parse_round(line: str) -> Round:
        c1, c2 = line.split()
        return c1, c2

    return [parse_round(l) for l in f]


def _to_shape(s: str) -> Shape:
    match s:
        case "A" | "X":
            return Shape.ROCK
        case "B" | "Y":
            return Shape.PAPER
        case "C" | "Z":
            return Shape.SCISSORS
        case _:
            raise ValueError(s)


def _to_result(s: str) -> Result:
    match s:
        case "X":
            return Result.LOSE
        case "Y":
            return Result.DRAW
        case "Z":
            return Result.WIN
        case _:
            raise ValueError(s)


def part1(rounds: Sequence[Round]) -> int:
    def outcome(r: Round) -> int:
        c1, c2 = map(_to_shape, r)
        return c2.value + ROUND_RESULT[c1, c2].value

    return sum(outcome(r) for r in rounds)


def part2(rounds: Sequence[Round]) -> int:
    choice = {(r, c1): c2 for (c1, c2), r in ROUND_RESULT.items()}

    def outcome(r: Round) -> int:
        c1, exp = _to_shape(r[0]), _to_result(r[1])
        return choice[exp, c1].value + exp.value

    return sum(outcome(r) for r in rounds)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
