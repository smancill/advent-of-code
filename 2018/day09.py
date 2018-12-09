#!/usr/bin/env python3

from collections import defaultdict, deque
from itertools import cycle

with open("input09.txt") as f:
    words = f.read().split()
    players = int(words[0])
    marbles = int(words[6])


def marble_mania(n_players, n_marbles):
    circle = deque([0])
    score = defaultdict(int)

    plays = zip(cycle(range(1, n_players + 1)), range(1, n_marbles + 1))
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


winner1 = marble_mania(players, marbles)
winner2 = marble_mania(players, marbles * 100)

print(f"P1: {winner1[1]}")
print(f"P2: {winner2[1]}")
