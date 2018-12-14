#!/usr/bin/env python3

with open("input14.txt") as f:
    data = f.read().strip()


class ScoreBoard:

    def __init__(self):
        self.scores = [3, 7]
        self.elf1 = 0
        self.elf2 = 1

    def add_scores(self):
        score1 = self.scores[self.elf1]
        score2 = self.scores[self.elf2]

        total = score1 + score2
        if total >= 10:
            self.scores.extend([total // 10, total % 10])
        else:
            self.scores.append(total)

        self.elf1 = (self.elf1 + score1 + 1) % len(self.scores)
        self.elf2 = (self.elf2 + score2 + 1) % len(self.scores)


def part1(data):
    board = ScoreBoard()
    n = int(data)
    m = n + 10

    while len(board.scores) < m:
        board.add_scores()

    return ''.join(map(str, board.scores[n:m]))


def part2(data):
    board = ScoreBoard()
    recipes = [int(d) for d in data]
    n = len(recipes)

    while board.scores[-n:] != recipes and board.scores[-n-1:-1] != recipes:
        board.add_scores()

    if board.scores[-n:] == recipes:
        return len(board.scores) - n
    return len(board.scores) - n - 1


print(f"P1: {part1(data)}")
print(f"P2: {part2(data)}")
