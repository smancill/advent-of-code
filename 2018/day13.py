#!/usr/bin/env python

from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Final, TextIO

type Coord = tuple[int, int]
type Tracks = Mapping[Coord, str]


cart_to_track: Final[Mapping[str, str]] = {
    "<": "-",
    ">": "-",
    "v": "|",
    "^": "|",
}

delta: Final[Mapping[str, Coord]] = {
    ">": (1, 0),
    "<": (-1, 0),
    "v": (0, 1),
    "^": (0, -1),
}

turn_intersection: Final[Mapping[str, str]] = {
    ">": "^>v",
    "<": "v<^",
    "v": ">v<",
    "^": "<^>",
}

turn_curve: Final[Mapping[str, Mapping[str, str]]] = {
    "/": {">": "^", "^": ">", "<": "v", "v": "<"},
    "\\": {">": "v", "^": "<", "<": "^", "v": ">"},
}


@dataclass
class Cart:
    _position: Coord
    _direction: str
    _turn: int = 0

    @property
    def position(self) -> Coord:
        return self._position

    @property
    def direction(self) -> str:
        return self._direction

    def advance(self) -> None:
        cx, cy = self._position
        dx, dy = delta[self._direction]
        self._position = cx + dx, cy + dy

    def take_intersection(self) -> None:
        self._direction = turn_intersection[self._direction][self._turn]
        self._turn = (self._turn + 1) % 3

    def take_curve(self, curve: str) -> None:
        self._direction = turn_curve[curve][self._direction]


def read_data(f: TextIO) -> list[str]:
    return [l.rstrip() for l in f]


def parse_data(data: Sequence[str]) -> tuple[Tracks, list[Cart]]:
    tracks = {}
    carts = []

    for y in range(len(data)):
        for x in range(len(data[y])):
            c = data[y][x]
            if c in cart_to_track:
                carts.append(Cart((x, y), c))
                tracks[x, y] = cart_to_track[c]
            else:
                tracks[x, y] = c

    return tracks, carts


def move_carts(tracks: Tracks, carts: Sequence[Cart]) -> None:
    for c in carts:
        c.advance()
        t = tracks[c.position]
        if t == "+":
            c.take_intersection()
        elif t == "/" or t == "\\":
            c.take_curve(t)


def crashes(carts: Sequence[Cart]) -> list[Coord]:
    ct = Counter(c.position for c in carts)
    return [p for p, n in ct.most_common() if n > 1]


def part1(data: Sequence[str]) -> Coord:
    tracks, carts = parse_data(data)
    while True:
        move_carts(tracks, carts)
        for p in crashes(carts):
            return p


def part2(data: Sequence[str]) -> Coord:
    tracks, carts = parse_data(data)
    while True:
        move_carts(tracks, carts)
        for p in crashes(carts):
            carts = [c for c in carts if c.position != p]
        if len(carts) == 1:
            return carts[0].position


def main() -> None:
    data = read_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
