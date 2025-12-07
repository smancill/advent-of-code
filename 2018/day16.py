#!/usr/bin/env python

import re
from collections import defaultdict
from collections.abc import Callable, Iterator, Sequence
from itertools import count
from typing import TextIO

type Registers = list[int]
type Instruction = tuple[int, int, int, int]
type Sample = tuple[Instruction, Registers, Registers]

type OpCodeFn = Callable[[Registers, int, int, int], None]

type OpCodesCandidates = dict[int, set[str]]
type OpCodes = dict[int, str]


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
    return [l.rstrip() for l in f]


def read_samples(data: Sequence[str]) -> Iterator[Sample]:
    def parse_ints(line: str) -> list[int]:
        return list(map(int, re.findall(r"\d+", line)))

    def parse_sample(sample: Sequence[str]) -> Sample:
        inputs = parse_ints(sample[0])
        op, a, b, c = parse_ints(sample[1])
        outputs = parse_ints(sample[2])
        assert len(inputs) == 4 and len(outputs) == 4
        return (op, a, b, c), inputs, outputs

    for i in count(0, 4):
        sample = data[i : i + 4]
        if not sample[0].startswith("Before"):
            break
        yield parse_sample(sample)


def read_program(data: Sequence[str]) -> Iterator[Instruction]:
    i = 0
    while data[i]:  # skip sample data
        i += 4
    while not data[i]:  # skip empty lines
        i += 1

    def parse_instruction(line: str) -> Instruction:
        op, a, b, c = map(int, line.split())
        return (op, a, b, c)

    return (parse_instruction(l) for l in data[i:])


def _process_samples(data: Sequence[str]) -> tuple[int, OpCodesCandidates]:
    total = 0
    opcodes = defaultdict(set)

    def process(sample: Sample) -> None:
        (op, a, b, c), inputs, outputs = sample
        matches = 0
        for name, fn in opcodes_fn.items():
            regs = inputs[:]
            fn(regs, a, b, c)
            if regs == outputs:
                opcodes[op].add(name)
                matches += 1
        if matches >= 3:
            nonlocal total
            total += 1

    for sample in read_samples(data):
        process(sample)

    return total, opcodes


def _reduce_opcodes(data: Sequence[str]) -> OpCodes:
    _, opcodes = _process_samples(data)
    queue = set(opcodes_fn)
    while queue:
        # Find an opcode with a single function
        name = None
        for _, candidates in opcodes.items():
            if len(candidates) == 1:
                (name,) = candidates
                if name not in queue:
                    # Already reduced
                    continue
                break
        assert name is not None
        # Remove the found opcode function from other opcodes
        for _, candidates in opcodes.items():
            if len(candidates) > 1 and name in candidates:
                candidates.remove(name)
        queue.remove(name)

    return {k: v.pop() for k, v in opcodes.items()}


def execute_program(data: Sequence[str]) -> Registers:
    opcodes = _reduce_opcodes(data)
    regs = [0] * 4
    for op, a, b, c in read_program(data):
        fn = opcodes_fn[opcodes[op]]
        fn(regs, a, b, c)
    return regs


def part1(data: Sequence[str]) -> int:
    total, _ = _process_samples(data)
    return total


def part2(data: Sequence[str]) -> int:
    regs = execute_program(data)
    return regs[0]


def main() -> None:
    data = read_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
