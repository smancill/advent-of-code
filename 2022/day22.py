#!/usr/bin/env python

import re
from functools import partial
from typing import Callable, TextIO, TypeAlias

Coord: TypeAlias = tuple[int, int]
Grid: TypeAlias = list[str]
Moves: TypeAlias = list[int | str]


def parse_data(f: TextIO) -> tuple[Grid, Moves]:
    def parse_grid(data: list[str]) -> Grid:
        # Add an "empty border" around the grid to ensure
        # all visited coordinates exist
        width = max(len(r) for r in data)
        grid = []
        grid.append(" " * (width + 2))
        for row in data:
            if len(row) < width:
                row += " " * (width - len(row))
            grid.append(" " + row + " ")
        grid.append(" " * (width + 2))
        return grid

    def parse_moves(line: str) -> Moves:
        return [m if m in "LR" else int(m) for m in re.findall(r"\d+|[RL]", line)]

    *grid_data, _, moves_data = f.read().splitlines()

    return parse_grid(grid_data), parse_moves(moves_data)


def _wrap2D(grid: Grid, pos: Coord, facing: Coord) -> Coord:
    x, y = pos
    dx, dy = facing
    match dx, dy:
        case (0, 1):
            y = next(i for i in range(len(grid)) if grid[i][x] != " ")
        case (0, -1):
            y = next(i for i in reversed(range(len(grid))) if grid[i][x] != " ")
        case (1, 0):
            x = next(j for j in range(len(grid[y])) if grid[y][j] != " ")
        case (-1, 0):
            x = next(j for j in reversed(range(len(grid[y]))) if grid[y][j] != " ")
    return x, y


class PathFinder:
    _grid: Grid
    _moves: Moves
    _wrap: Callable[[Coord, Coord], Coord]

    def __init__(self, grid: Grid, moves: Moves):
        self._grid = grid
        self._moves = moves
        self._wrap = partial(_wrap2D, self._grid)

    def traverse(self) -> tuple[Coord, Coord]:
        x, y = self._orig()
        dx, dy = (1, 0)
        for move in self._moves:
            match move:
                case int(d):
                    x, y = self._advance((x, y), (dx, dy), d)
                case "L":
                    dx, dy = dy, -dx
                case "R":
                    dx, dy = -dy, dx
                case _:
                    raise ValueError(f"invalid move: {move}")
        return (x, y), (dx, dy)

    def _orig(self) -> Coord:
        return next((j, 1) for j, c in enumerate(self._grid[1]) if c != " ")

    def _advance(self, pos: Coord, facing: Coord, dist: int) -> Coord:
        x, y = pos
        dx, dy = facing
        for _ in range(dist):
            nx, ny = x + dx, y + dy
            if self._grid[ny][nx] == " ":
                nx, ny = self._wrap((nx, ny), (dx, dy))
            if self._grid[ny][nx] == "#":
                break
            x, y = nx, ny
        return x, y


def password(grid: Grid, moves: Moves) -> int:
    def facing_points(dx: int, dy: int) -> int:
        return [(1, 0), (0, 1), (-1, 0), (0, -1)].index((dx, dy))

    path_finder = PathFinder(grid, moves)
    (x, y), (dx, dy) = path_finder.traverse()
    return 1000 * y + 4 * x + facing_points(dx, dy)


def part1(grid: Grid, moves: Moves) -> int:
    return password(grid, moves)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(*data)}")


if __name__ == "__main__":
    main()
