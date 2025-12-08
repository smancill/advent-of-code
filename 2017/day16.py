#!/usr/bin/env python

from typing import TextIO

type Programs = list[str]
type Moves = list[str]


def parse_data(f: TextIO) -> list[str]:
    return f.read().rstrip().split(",")


def dance(programs: Programs, moves: Moves) -> Programs:
    programs = programs[:]
    for m in moves:
        if m[0] == "s":
            s = int(m[1:])
            programs = programs[-s:] + programs[:-s]
        elif m[0] == "x":
            ab = m[1:].split("/")
            a, b = map(int, ab)
            programs[a], programs[b] = programs[b], programs[a]
        elif m[0] == "p":
            ab = m[1:].split("/")
            a = programs.index(ab[0])
            b = programs.index(ab[1])
            programs[a], programs[b] = programs[b], programs[a]
    return programs


def dance_until(programs: Programs, moves: Moves, repeats: int) -> Programs:
    prev = [programs[:]]
    for _ in range(repeats):
        programs = dance(programs, moves)
        if programs == prev[0]:
            return prev[repeats % len(prev)]
        prev.append(programs)
    return programs


def part1(programs: str, moves: Moves) -> str:
    return "".join(dance(list(programs), moves))


def part2(programs: str, moves: Moves) -> str:
    return "".join(dance_until(list(programs), moves, 1_000_000_000))


def main() -> None:
    programs = "abcdefghijklmnop"
    moves = parse_data(open(0))

    print(f"P1: {part1(programs, moves)}")
    print(f"P2: {part2(programs, moves)}")


if __name__ == "__main__":
    main()
