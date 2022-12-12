#!/usr/bin/env python

import logging
import logging.config
from itertools import count
from typing import TextIO, TypeAlias

Deck: TypeAlias = list[int]
Winner: TypeAlias = tuple[int, Deck]


def parse_data(f: TextIO) -> tuple[Deck, Deck]:
    def parse_deck(lines: str) -> Deck:
        _, *deck = lines.splitlines()
        return [int(n) for n in deck]

    deck1, deck2 = [parse_deck(s) for s in f.read().split("\n\n")]
    return deck1, deck2


def _log_game_results(deck1: Deck, deck2: Deck) -> None:
    logging.info("== Post-game results ==")
    logging.info(f"Player 1's deck: {', '.join(str(c) for c in deck1)}")
    logging.info(f"Player 2's deck: {', '.join(str(c) for c in deck2)}")


def normal_game(deck1: Deck, deck2: Deck) -> Winner:
    while deck1 and deck2:
        c1, c2 = deck1.pop(0), deck2.pop(0)

        if c1 > c2:
            deck1.extend([c1, c2])
        else:
            deck2.extend([c2, c1])

    _log_game_results(deck1, deck2)

    return (1, deck1) if deck1 else (2, deck2)


_game_counter = 0


def recursive_game(deck1: Deck, deck2: Deck) -> Winner:
    global _game_counter
    _game_counter += 1
    game = _game_counter

    prev = set()

    while deck1 and deck2:
        key = (tuple(deck1), tuple(deck2))
        if key in prev:
            break
        prev.add(key)

        c1, c2 = deck1.pop(0), deck2.pop(0)

        if c1 <= len(deck1) and c2 <= len(deck2):
            winner, _ = recursive_game(deck1[:c1], deck2[:c2])
        else:
            winner = 1 if c1 > c2 else 2

        if winner == 1:
            deck1 += [c1, c2]
        else:
            deck2 += [c2, c1]

    if game == 1:
        _log_game_results(deck1, deck2)

    return (1, deck1) if deck1 else (2, deck2)


def score(deck: Deck) -> int:
    return sum(c * v for c, v in zip(reversed(deck), count(1)))


def part1(deck1: Deck, deck2: Deck) -> int:
    _, deck = normal_game(deck1[:], deck2[:])
    return score(deck)


def part2(deck1: Deck, deck2: Deck) -> int:
    _, deck = recursive_game(deck1[:], deck2[:])
    return score(deck)


def main() -> None:
    logging.config.fileConfig("../logging.conf")

    d1, d2 = parse_data(open(0))

    print(f"P1: {part1(d1, d2)}")
    print(f"P2: {part2(d1, d2)}")


if __name__ == "__main__":
    main()
