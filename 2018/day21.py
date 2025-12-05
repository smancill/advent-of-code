#!/usr/bin/env python

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


def execute_program(data: Sequence[str], part1: bool = True) -> int:
    ip, prog = read_program(data)

    # Initial value of registers
    regs = [0] * N

    # get important registers
    main, opt = prog[5][-1], prog[26][-1]

    seen = set()
    prev = 0

    while 0 <= regs[ip] < len(prog):
        # intersect instruction for halt condition
        if regs[ip] == 28:
            val = regs[main]
            if part1:
                return val
            if val in seen:
                return prev
            seen.add(val)
            prev = val
            regs[ip] = 5
        # optimize loop in instructions 17-27
        elif regs[ip] == 17:
            regs[opt] //= 256
            regs[ip] = 7
        # execute instruction normally
        else:
            op, a, b, c = prog[regs[ip]]
            fn = opcodes_fn[op]
            fn(regs, a, b, c)

        regs[ip] += 1

    raise AssertionError


def main() -> None:
    data = read_data(open(0))

    print(f"P1: {execute_program(data, part1=True)}")
    print(f"P2: {execute_program(data, part1=False)}")


if __name__ == "__main__":
    main()
