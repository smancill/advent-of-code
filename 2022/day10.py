#!/usr/bin/env python

from collections import deque
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from itertools import count
from typing import TextIO


@dataclass(frozen=True)
class Instruction:
    name: str
    duration: int
    value: int


@dataclass
class Running:
    timer: int
    value: int


def parse_data(f: TextIO) -> list[Instruction]:
    def parse_instruction(line: str) -> Instruction:
        tokens = line.split()
        match tokens:
            case ["noop"]:
                return Instruction("noop", 1, 0)
            case ["addx", v]:
                return Instruction("addx", 2, int(v))
            case _:
                raise ValueError(line)

    return [parse_instruction(l) for l in f]


def cycles(instructions: Sequence[Instruction]) -> Iterator[tuple[int, int]]:
    reg = 1
    running = None
    queue = deque(instructions)
    for cycle in count(1):
        if not running:
            if not queue:
                break
            instr = queue.popleft()
            running = Running(instr.duration, instr.value)

        yield (cycle, reg)

        if running:
            running.timer -= 1
            if running.timer == 0:
                reg += running.value
                running = None


def part1(data: Sequence[Instruction]) -> int:
    return sum(c * r for c, r in cycles(data) if (c - 20) % 40 == 0)


def part2(data: Sequence[Instruction]) -> str:
    width = 40
    crt = ""
    for cycle, reg in cycles(data):
        x = (cycle - 1) % width
        if reg - 1 <= x <= reg + 1:
            crt += "#"
        else:
            crt += "."
        if x == width - 1:
            crt += "\n"
    return crt


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2:\n{part2(data)}", end="")


if __name__ == "__main__":
    main()
