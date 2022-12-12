#!/usr/bin/env python

from collections.abc import Sequence
from typing import TextIO, TypeAlias

Instruction: TypeAlias = tuple[str, int]


def parse_data(f: TextIO) -> list[Instruction]:
    return [(op, int(arg)) for op, arg in [ins.split() for ins in f]]


def run(prog: Sequence[Instruction]) -> tuple[int, int]:
    n = len(prog)
    visited = [False] * n
    ip = 0
    acc = 0

    while True:
        if visited[ip]:
            break
        visited[ip] = True

        op, arg = prog[ip]
        match op:
            case "acc":
                ip += 1
                acc += arg
            case "jmp":
                ip += arg
            case "nop":
                ip += 1
            case _:
                assert False

        if ip == n:
            break

    return ip, acc


def part1(prog: Sequence[Instruction]) -> int:
    _, acc = run(prog)
    return acc


def part2(prog: Sequence[Instruction]) -> int:
    prog = list(prog)
    n = len(prog)
    for i in range(len(prog)):
        op, arg = prog[i]
        match op:
            case "nop":
                prog[i] = ("jmp", arg)
            case "jmp":
                prog[i] = ("nop", 0)
            case _:
                continue
        ip, acc = run(prog)
        if ip == n:
            return acc
        prog[i] = (op, arg)

    assert False


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
