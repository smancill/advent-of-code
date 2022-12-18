#!/usr/bin/env python

from collections.abc import Sequence
from functools import cmp_to_key
from math import prod
from typing import Any, TextIO, TypeAlias, Union

Packet: TypeAlias = list[Union[int, "Packet"]]
Pair: TypeAlias = tuple[Packet, Packet]


class PacketParser:
    _current: Packet
    _stack: list[Packet]
    _val: str

    # Could be a simple eval(line)
    def parse(self, line: str) -> Packet:
        self._current = []
        self._stack = []
        self._val = ""

        for c in line[1:-1]:
            match c:
                case "[":
                    self._start_list()
                case "]":
                    self._add_number()
                    self._add_list()
                case ",":
                    self._add_number()
                case " ":
                    pass
                case d:
                    self._add_digit(d)
        self._add_number()

        return self._current

    def _start_list(self) -> None:
        self._stack.append(self._current)
        self._current = []

    def _add_list(self) -> None:
        parent = self._stack.pop()
        parent.append(self._current)
        self._current = parent

    def _add_digit(self, d: str) -> None:
        self._val += d

    def _add_number(self) -> None:
        if self._val:
            self._current.append(int(self._val))
            self._val = ""


def parse_data(f: TextIO) -> list[Any]:
    def parse_pair(lines: str) -> Pair:
        packet1, packet2 = lines.splitlines()
        parser = PacketParser()
        return parser.parse(packet1), parser.parse(packet2)

    return [parse_pair(s) for s in f.read().split("\n\n")]


def cmp(left: Packet | int, right: Packet | int) -> int:
    match left, right:
        case int(l), int(r):
            return (l > r) - (l < r)
        case list(l), list(r):
            for c in map(cmp, l, r):
                if c != 0:
                    return c
            return cmp(len(l), len(r))
        case list(l), int(r):
            return cmp(l, [r])
        case int(l), list(r):
            return cmp([l], r)
        case _:
            raise ValueError(f"({left}, {right})")


def sort(pairs: Sequence[Pair], extra: list[Packet] = []) -> list[Packet]:
    packets = [packet for pair in pairs for packet in pair] + extra
    packets = sorted(packets, key=cmp_to_key(cmp))
    return packets


def part1(data: Sequence[Pair]) -> int:
    def is_right_order(pair: Pair) -> bool:
        return cmp(*pair) == -1

    return sum(i for i, p in enumerate(data, 1) if is_right_order(p))


def part2(data: Sequence[Pair]) -> int:
    extra: list[Packet] = [[[2]], [[6]]]
    packets = sort(data, extra)

    return prod(i for i, p in enumerate(packets, 1) if p in extra)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
