#!/usr/bin/env python

from dataclasses import dataclass, field
from typing import TextIO


def read_data(f: TextIO) -> str:
    return f.read().rstrip()


@dataclass
class ScoreBoard:
    scores: list[int] = field(default_factory=lambda: [3, 7])
    elf1: int = 0
    elf2: int = 1

    def add_scores(self) -> None:
        score1 = self.scores[self.elf1]
        score2 = self.scores[self.elf2]

        total = score1 + score2
        if total >= 10:
            self.scores.extend(divmod(total, 10))
        else:
            self.scores.append(total)

        self.elf1 = (self.elf1 + score1 + 1) % len(self.scores)
        self.elf2 = (self.elf2 + score2 + 1) % len(self.scores)


def part1(data: str) -> str:
    board = ScoreBoard()
    n = int(data)
    m = n + 10

    while len(board.scores) < m:
        board.add_scores()

    return "".join(map(str, board.scores[n:m]))


def part2(data: str) -> int:
    board = ScoreBoard()
    recipes = [int(d) for d in data]
    n = len(recipes)

    while board.scores[-n:] != recipes and board.scores[-n - 1 : -1] != recipes:
        board.add_scores()

    if board.scores[-n:] == recipes:
        return len(board.scores) - n
    return len(board.scores) - n - 1


def main() -> None:
    data = read_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
