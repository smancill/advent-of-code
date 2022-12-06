#!/usr/bin/env python

import logging
import logging.config
from collections.abc import Callable, Sequence
from typing import Final, TextIO, TypeAlias

N: Final = 6

Registers: TypeAlias = list[int]
Instruction: TypeAlias = tuple[str, int, int, int]

OpCodeFn: TypeAlias = Callable[[Registers, int, int, int], None]


def _wrap(op: Callable[[Registers, int, int], int]) -> OpCodeFn:
    def fn(regs: Registers, a: int, b: int, c: int) -> None:
        regs[c] = op(regs, a, b)

    return fn


opcodes_fn: dict[str, OpCodeFn] = {
    "addr": _wrap(lambda r, a, b: r[a] + r[b]),
    "addi": _wrap(lambda r, a, b: r[a] + b),
    "mulr": _wrap(lambda r, a, b: r[a] * r[b]),
    "muli": _wrap(lambda r, a, b: r[a] * b),
    "banr": _wrap(lambda r, a, b: r[a] & r[b]),
    "bani": _wrap(lambda r, a, b: r[a] & b),
    "borr": _wrap(lambda r, a, b: r[a] | r[b]),
    "bori": _wrap(lambda r, a, b: r[a] | b),
    "setr": _wrap(lambda r, a, b: r[a]),
    "seti": _wrap(lambda r, a, b: a),
    "gtir": _wrap(lambda r, a, b: 1 if a > r[b] else 0),
    "gtri": _wrap(lambda r, a, b: 1 if r[a] > b else 0),
    "gtrr": _wrap(lambda r, a, b: 1 if r[a] > r[b] else 0),
    "eqir": _wrap(lambda r, a, b: 1 if a == r[b] else 0),
    "eqri": _wrap(lambda r, a, b: 1 if r[a] == b else 0),
    "eqrr": _wrap(lambda r, a, b: 1 if r[a] == r[b] else 0),
}


def read_data(f: TextIO) -> list[str]:
    return f.readlines()


def read_program(data: Sequence[str]) -> tuple[int, list[Instruction]]:
    def parse_instruction(line: str) -> Instruction:
        op, *args = line.split()
        a, b, c = map(int, args)
        return (op, a, b, c)

    ip = int(data[0].split()[-1])
    ins = [parse_instruction(l) for l in data[1:]]

    return ip, ins


def execute_program(
    data: Sequence[str], *, reg0: int = 0, optimize: bool = False
) -> Registers:
    """To run the part 2 version set reg0 to 1 and optimize to True."""
    debug = logging.getLogger().isEnabledFor(logging.DEBUG)

    # Initial value of registers
    regs = [0] * N
    regs[0] = reg0

    ip, prog = read_program(data)

    while 0 <= regs[ip] < len(prog):
        if optimize and regs[ip] == 1:
            # get main register used by the program (user-defined)
            C = prog[4][-2]

            # Running Part 2 seems that it won't finish anytime soon.
            # Fix by intersecting and optimizing loop in instructions 1-16
            # The full program could be decompiled but the other instructions run
            # fast enough.
            #
            # Original loop:
            # for rA in 1..rC do
            #     for rB in 1..rC do
            #         if rA * rB == rC then
            #             r0 += rA
            n = regs[C]
            factors = set(
                f
                for i in range(1, int(n**0.5) + 1)
                for f in [i, n // i]
                if n % i == 0
            )
            regs[0] = sum(factors)
            regs[ip] = 256
        else:
            if debug:
                prev = regs[:]

            # execute instruction normally
            op, a, b, c = prog[regs[ip]]
            fn = opcodes_fn[op]
            fn(regs, a, b, c)

            if debug:
                logging.debug(f"ip={prev[ip]} {prev} {op} {a} {b} {c} {regs}")

        regs[ip] += 1

    return regs


def part1(data: Sequence[str]) -> int:
    regs = execute_program(data)
    return regs[0]


def part2(data: Sequence[str]) -> int:
    regs = execute_program(data, reg0=1, optimize=True)
    return regs[0]


def main() -> None:
    logging.config.fileConfig("../logging.conf")

    data = read_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
