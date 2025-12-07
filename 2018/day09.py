#!/usr/bin/env python

from collections import defaultdict, deque
from itertools import cycle
from typing import TextIO


def parse_data(f: TextIO) -> tuple[int, int]:
    words = f.read().split()
    players = int(words[0])
    marbles = int(words[6])
    return players, marbles


def marble_mania(players: int, marbles: int) -> tuple[int, int]:
    circle = deque([0])
    score = defaultdict[int, int](int)

    plays = zip(cycle(range(1, players + 1)), range(1, marbles + 1))
    for player, marble in plays:
        # keep current marble in the last position
        if marble % 23 == 0:
            circle.rotate(7)
            score[player] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)

    return max(score.items(), key=lambda e: e[1])


def part1(players: int, marbles: int) -> int:
    _, score = marble_mania(players, marbles)
    return score


def part2(players: int, marbles: int) -> int:
    _, score = marble_mania(players, marbles * 100)
    return score


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(*data)}")
    print(f"P2: {part2(*data)}")


if __name__ == "__main__":
    main()
