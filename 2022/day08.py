#!/usr/bin/env python

from collections.abc import Sequence
from math import prod
from typing import Final, TextIO


class Trees:
    _data: Final[list[list[int]]]

    def __init__(self, data: Sequence[Sequence[int]]):
        self._data = [list(row) for row in data]

    @property
    def width(self) -> int:
        return len(self._data[0])

    @property
    def height(self) -> int:
        return len(self._data)

    def __getitem__(self, pos: tuple[int, int]) -> int:
        return self._data[pos[1]][pos[0]]


def parse_data(f: TextIO) -> Trees:
    return Trees([[int(c) for c in l.strip()] for l in f])


def _views_from(trees: Trees, x: int, y: int) -> list[list[int]]:
    return [
        [trees[x, i] for i in reversed(range(0, y))],
        [trees[x, i] for i in range(y + 1, trees.height)],
        [trees[j, y] for j in reversed(range(0, x))],
        [trees[j, y] for j in range(x + 1, trees.width)],
    ]


def visible_from_outside(trees: Trees, x: int, y: int) -> bool:
    def visible_from(view: list[int]) -> bool:
        return all(t < trees[x, y] for t in view)

    return any(visible_from(view) for view in _views_from(trees, x, y))


def scenic_score(trees: Trees, x: int, y: int) -> int:
    def visible_trees(view: list[int]) -> int:
        count = 0
        for t in view:
            count += 1
            if t >= trees[x, y]:
                break
        return count

    return prod(visible_trees(view) for view in _views_from(trees, x, y))


def part1(trees: Trees) -> int:
    border = 2 * trees.height + 2 * trees.width - 4
    interior = sum(
        1
        for y in range(1, trees.height - 1)
        for x in range(1, trees.width - 1)
        if visible_from_outside(trees, x, y)
    )
    return border + interior


def part2(trees: Trees) -> int:
    return max(
        scenic_score(trees, x, y)
        for y in range(trees.height)
        for x in range(trees.width)
    )


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
