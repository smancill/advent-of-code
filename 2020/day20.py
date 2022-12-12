#!/usr/bin/env python

import math
from collections import defaultdict
from collections.abc import Callable, Iterator, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any, Final, Generic, TextIO, TypeVar

MONSTER: Final = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
]


class Side(Enum):
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3


T = TypeVar("T")


class Container(Generic[T]):
    _data: list[list[T]]
    _height: int
    _width: int

    def __init__(self, data: Sequence[Sequence[T]]):
        assert len({len(row) for row in data}) == 1
        self._data = [list(s) for s in data]
        self._height, self._width = len(data), len(data[0])

    @property
    def data(self) -> Sequence[Sequence[T]]:
        return self._data

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    def rotate(self) -> None:
        """Rotate 90 degrees clockwise."""
        # Transpose
        n, m = self._height, self._width
        T = [[self._data[i][j] for i in range(n)] for j in range(m)]

        # Reverse each row
        self._data = [row[::-1] for row in T]

        # Adjust size
        self._height, self._width = self._width, self._height

    def flip(self) -> None:
        """Flip vertically."""
        self._data = self._data[::-1]

    def __str__(self) -> str:
        return "\n".join("".join(str(elem) for elem in row) for row in self._data)


C = TypeVar("C", bound=Container[Any])


def orientate_until(cont: C, pred: Callable[[C], bool]) -> None:
    """
    Rotate and flip until the predicate is True.

    Leave the container in the original orientation if the predicate
    was not True for any orientation.
    """
    for i in range(8):
        if pred(cont):
            return
        cont.rotate()
        if (i + 1) % 4 == 0:
            cont.flip()


class Tile(Container[str]):
    id: Final[int]

    def __init__(self, lines: Sequence[str]):
        header, *data = lines
        _, id = header.split()
        self.id = int(id.rstrip(":"))
        super().__init__(data)

    def border(self, side: Side) -> str:
        match side:
            case Side.TOP:
                return "".join(self.data[0])
            case Side.BOTTOM:
                return "".join(self.data[-1])
            case Side.LEFT:
                return "".join(r[0] for r in self.data)
            case Side.RIGHT:
                return "".join(r[-1] for r in self.data)

    def trim(self) -> None:
        self._data = [row[1:-1] for row in self._data[1:-1]]
        self._height -= 2
        self._width -= 2


class Image(Container[str]):
    def __init__(self, data: Sequence[Sequence[str]]):
        super().__init__(data)


class AssembledTiles(Container[Tile]):
    _trimmed: bool

    def __init__(self, data: Sequence[Sequence[Tile]]):
        super().__init__(data)
        self._trimmed = False

    def image(self) -> Image:
        if not self._trimmed:
            self.trim()

        composed = [
            [v for r in tr for v in r]
            for row in self.data
            for tr in self._tile_rows(row)
        ]
        return Image(composed)

    def rotate(self) -> None:
        super().rotate()
        for row in self.data:
            for t in row:
                t.rotate()

    def flip(self) -> None:
        super().flip()
        for row in self.data:
            for t in row:
                t.flip()

    def trim(self) -> None:
        for row in self.data:
            for t in row:
                t.trim()
        self._trimmed = True

    def _tile_rows(self, tiles: Sequence[Tile]) -> Iterator[tuple[Sequence[str], ...]]:
        return zip(*(t.data for t in tiles))

    def __str__(self) -> str:
        def assembled_line(tr: tuple[Sequence[str], ...]) -> str:
            return " ".join("".join(r) for r in tr)

        def assembled_row(tiles: Sequence[Tile]) -> str:
            return "\n".join(assembled_line(tr) for tr in self._tile_rows(tiles))

        return "\n\n".join(assembled_row(row) for row in self.data)


class ImageAssembler:
    _adj: dict[str, set[Tile]]

    def assemble(self, tiles: Mapping[int, Tile]) -> AssembledTiles:
        self._adj = self._map_adj(tiles)

        assembled = []
        prev = self._top_corner(tiles)
        row = [prev]
        while True:
            sides = self._adj_sides(row)
            current = self._find_adj(prev, sides)
            row.append(current)
            if self._last_row_tile(current):
                assembled.append(row)
                if self._last_assembled_tile(current):
                    break
                prev = row[0]
                row = []
            else:
                prev = current

        return AssembledTiles(assembled)

    @staticmethod
    def _map_adj(tiles: Mapping[int, Tile]) -> dict[str, set[Tile]]:
        adj: dict[str, set[Tile]] = defaultdict(set)
        for t in tiles.values():
            for s in Side:
                b = t.border(s)
                for k in (b, b[::-1]):
                    adj[k].add(t)
        return adj

    def _find_adj(self, tile: Tile, sides: tuple[Side, Side]) -> Tile:
        border = tile.border(sides[0])
        cand = self._adj[border] - {tile}
        adj = cand.pop()
        orientate_until(adj, lambda t: border == t.border(sides[1]))
        return adj

    def _has_adj(self, tile: Tile, side: Side) -> bool:
        return len(self._adj[tile.border(side)]) > 1

    def _top_corner(self, tiles: Mapping[int, Tile]) -> Tile:
        def count_adj(t: Tile) -> int:
            return sum(1 for s in Side if self._has_adj(t, s))

        def top_corner(t: Tile) -> bool:
            return all(not self._has_adj(t, b) for b in (Side.LEFT, Side.TOP))

        corner = next(t for t in tiles.values() if count_adj(t) == 2)
        orientate_until(corner, top_corner)
        return corner

    def _adj_sides(self, row: list[Tile]) -> tuple[Side, Side]:
        return (Side.RIGHT, Side.LEFT) if row else (Side.BOTTOM, Side.TOP)

    def _last_row_tile(self, tile: Tile) -> bool:
        return not self._has_adj(tile, Side.RIGHT)

    def _last_assembled_tile(self, tile: Tile) -> bool:
        return not self._has_adj(tile, Side.BOTTOM)


@dataclass(frozen=True)
class MonsterLocations:
    image: Image
    locations: list[tuple[int, int]]

    def water_roughness(self) -> int:
        return sum(1 for row in self.image.data for v in row if v == "#")


class MonsterFinder:
    _monster: Image

    def __init__(self) -> None:
        self._monster = Image(MONSTER)

    def find(self, img: Image) -> MonsterLocations | None:
        monsters = None

        def predicate(img: Image) -> bool:
            nonlocal monsters
            return (monsters := self._find(img)) is not None

        orientate_until(img, predicate)
        return monsters

    def _find(self, img: Image) -> MonsterLocations | None:
        locations = []
        for i in range(img.height - self._monster.height + 1):
            for j in range(img.width - self._monster.width + 1):
                if self._has_monster(img, i, j):
                    locations.append((i, j))

        if not locations:
            return None

        data = [list(row) for row in img.data]
        for i, j in locations:
            self._mark_monster(data, i, j)

        return MonsterLocations(Image(data), locations)

    def _has_monster(self, img: Image, y: int, x: int) -> bool:
        for i in range(self._monster.height):
            for j in range(self._monster.width):
                match (img.data[y + i][x + j], self._monster.data[i][j]):
                    case (".", "#"):
                        return False
                    case ("#", "#") | (("#" | "."), " "):
                        continue
                    case t:
                        raise ValueError(f"Invalid data: {t}")
        return True

    def _mark_monster(self, data: list[list[str]], y: int, x: int) -> None:
        for i in range(self._monster.height):
            for j in range(self._monster.width):
                if self._monster.data[i][j] == "#":
                    data[y + i][x + j] = "O"


def parse_data(f: TextIO) -> dict[int, Tile]:
    tiles = [Tile(t.splitlines()) for t in f.read().strip().split("\n\n")]
    return {t.id: t for t in tiles}


def part1(assembled: AssembledTiles) -> int:
    corners = [(0, 0), (0, -1), (-1, 0), (-1, -1)]
    return math.prod(assembled.data[i][j].id for i, j in corners)


def part2(img: Image) -> int:
    monsters = MonsterFinder().find(img)
    assert monsters is not None
    return monsters.water_roughness()


def main() -> None:
    tiles = parse_data(open(0))

    assembled = ImageAssembler().assemble(tiles)
    img = assembled.image()

    print(f"P1: {part1(assembled)}")
    print(f"P2: {part2(img)}")


if __name__ == "__main__":
    main()
