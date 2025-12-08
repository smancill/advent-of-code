#!/usr/bin/env python

from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from itertools import count
from typing import TextIO

BOARD_SIZE = 5


@dataclass
class Number:
    value: int
    marked: bool = False


class Board:
    _id: int
    _numbers: list[list[Number]]

    def __init__(self, id: int, numbers: Sequence[str]):
        self._id = id
        self._numbers = [[Number(int(n)) for n in rank.split()] for rank in numbers]

    def mark(self, value: int) -> bool:
        for rank in self._numbers:
            for n in rank:
                if n.value == value:
                    n.marked = True
                    return True
        return False

    def bingo(self) -> bool:
        def in_rank(i: int) -> bool:
            return all(self._numbers[i][j].marked for j in range(BOARD_SIZE))

        def in_file(j: int) -> bool:
            return all(self._numbers[i][j].marked for i in range(BOARD_SIZE))

        r = any(in_rank(i) for i in range(BOARD_SIZE))
        f = any(in_file(j) for j in range(BOARD_SIZE))

        return r or f

    def score(self) -> int:
        return sum(n.value for rank in self._numbers for n in rank if not n.marked)

    def clear(self) -> None:
        for rank in self._numbers:
            for v in rank:
                v.marked = False

    def __str__(self) -> str:
        out = ""
        for rank in self._numbers:
            out += " ".join(f"{n.value:2d}" for n in rank) + "\n"
        return out


def parse_data(f: TextIO) -> tuple[list[int], set[Board]]:
    def parse_numbers(numbers: str) -> list[int]:
        return [int(i) for i in numbers.split(",")]

    def parse_boards(boards: list[str]) -> set[Board]:
        ids = count(1)
        return {Board(next(ids), b.splitlines()) for b in boards}

    numbers, *boards = f.read().split("\n\n")
    return (parse_numbers(numbers), parse_boards(boards))


def play_bingo(
    boards: set[Board], numbers: list[int]
) -> Iterator[tuple[int, set[Board]]]:
    playing = set(boards)
    for b in playing:
        b.clear()
    for n in numbers:
        winners = set()
        for b in playing:
            b.mark(n)
            if b.bingo():
                winners.add(b)
        if winners:
            playing -= winners
            yield (n, winners)


def score(number: int, winners: set[Board]) -> int:
    assert len(winners) == 1
    board = next(iter(winners))
    return board.score() * number


def part1(boards: set[Board], numbers: list[int]) -> int:
    last, winners = next(play_bingo(boards, numbers))

    return score(last, winners)


def part2(boards: set[Board], numbers: list[int]) -> int:
    last, winners = 0, set[Board]()
    for last, winners in play_bingo(boards, numbers):  # noqa: B007
        pass
    return score(last, winners)


def main() -> None:
    numbers, boards = parse_data(open(0))

    print(f"P1: {part1(boards, numbers)}")
    print(f"P2: {part2(boards, numbers)}")


if __name__ == "__main__":
    main()
