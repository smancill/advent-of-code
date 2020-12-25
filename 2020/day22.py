#!/usr/bin/env python

from itertools import count

with open("input22.txt") as f:
    deck1, deck2 = [[int(c) for c in d.splitlines()[1:]]
                    for d in f.read().split('\n\n')]


def normal_game(deck1, deck2):
    while deck1 and deck2:
        c1, c2 = deck1.pop(0), deck2.pop(0)
        if c1 > c2:
            deck1.extend([c1, c2])
        else:
            deck2.extend([c2, c1])

    return (1, deck1) if deck1 else (2, deck2)


def recursive_game(deck1, deck2):
    prev = set()

    while deck1 and deck2:
        key = (tuple(deck1), tuple(deck2))
        if key in prev:
            return (1, deck1)
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

    return (1, deck1) if deck1 else (2, deck2)


def score(deck):
    return sum(c * v for c, v in zip(reversed(deck), count(1)))


def part1():
    _, deck = normal_game(deck1[:], deck2[:])
    return score(deck)


def part2():
    _, deck = recursive_game(deck1[:], deck2[:])
    return score(deck)


print(f"P1: {part1()}")
print(f"P2: {part2()}")
