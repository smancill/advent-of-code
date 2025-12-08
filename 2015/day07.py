#!/usr/bin/env python

from collections.abc import Iterator
from typing import TextIO


def parse_data(f: TextIO) -> dict[str, list[str]]:
    def parse_instruction(line: str) -> tuple[str, list[str]]:
        operation, target = line.split(" -> ")
        return (target, operation.split())

    return dict(parse_instruction(l.rstrip()) for l in f)


class Circuit:
    _instructions: dict[str, list[str]]
    _circuit: dict[str, int]

    def __init__(self, instructions: dict[str, list[str]]):
        self._instructions = instructions
        self._circuit = {}
        for root in self._roots():
            self._calculate(root)

    def _roots(self) -> set[str]:
        roots = set(self._instructions)
        for cmd in self._instructions.values():
            match cmd:
                case [lhs, _, rhs]:
                    roots.discard(lhs)
                    roots.discard(rhs)
                case [_, rhs]:
                    roots.discard(rhs)
                case [rhs]:
                    roots.discard(rhs)
                case _:
                    raise ValueError("invalid instructions")
        return roots

    def _calculate(self, wire: str) -> int:
        if wire.isdigit():
            return int(wire)
        if wire in self._circuit:
            return self._circuit[wire]
        match self._instructions[wire]:
            case [lhs, "AND", rhs]:
                value = self._calculate(lhs) & self._calculate(rhs)
            case [lhs, "OR", rhs]:
                value = self._calculate(lhs) | self._calculate(rhs)
            case [lhs, "LSHIFT", rhs]:
                value = self._calculate(lhs) << self._calculate(rhs)
            case [lhs, "RSHIFT", rhs]:
                value = self._calculate(lhs) >> self._calculate(rhs)
            case ["NOT", rhs]:
                value = ~self._calculate(rhs) & 0xFFFF
            case [rhs]:
                value = self._calculate(rhs)
            case _:
                raise ValueError("invalid instructions")
        self._circuit[wire] = value
        return value

    def __getitem__(self, wire: str) -> int:
        return self._circuit[wire]

    def __iter__(self) -> Iterator[str]:
        return iter(self._circuit)


def part1(data: dict[str, list[str]]) -> int:
    circuit = Circuit(data)
    return circuit["a"]


def part2(data: dict[str, list[str]]) -> int:
    signal = Circuit(data)["a"]
    circuit = Circuit(data | {"b": [str(signal)]})
    return circuit["a"]


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
