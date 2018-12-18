#!/usr/bin/env python3

import re

from itertools import count
from collections import defaultdict


with open("input16.txt") as f:
    data = [l.strip() for l in f]


def wrap(op):
    def fn(regs, a, b, c):
        regs[c] = op(regs, a, b)
    return fn


ops = {
    'addr': wrap(lambda r, a, b: r[a] + r[b]),
    'addi': wrap(lambda r, a, b: r[a] + b),
    'mulr': wrap(lambda r, a, b: r[a] * r[b]),
    'muli': wrap(lambda r, a, b: r[a] * b),
    'banr': wrap(lambda r, a, b: r[a] & r[b]),
    'bani': wrap(lambda r, a, b: r[a] & b),
    'borr': wrap(lambda r, a, b: r[a] | r[b]),
    'bori': wrap(lambda r, a, b: r[a] | b),
    'setr': wrap(lambda r, a, b: r[a]),
    'seti': wrap(lambda r, a, b: a),
    'gtir': wrap(lambda r, a, b: 1 if a > r[b] else 0),
    'gtri': wrap(lambda r, a, b: 1 if r[a] > b else 0),
    'gtrr': wrap(lambda r, a, b: 1 if r[a] > r[b] else 0),
    'eqir': wrap(lambda r, a, b: 1 if a == r[b] else 0),
    'eqri': wrap(lambda r, a, b: 1 if r[a] == b else 0),
    'eqrr': wrap(lambda r, a, b: 1 if r[a] == r[b] else 0),
}

opcodes = defaultdict(set)


def read_samples():
    for i in count(0, 4):
        case = data[i:i+4]
        if not case[0].startswith('Before'):
            break

        ins = list(map(int, re.findall(r'\d+', case[1])))
        inputs = list(map(int, re.findall(r'\d+', case[0])))
        outputs = list(map(int, re.findall(r'\d+', case[2])))

        yield ins, inputs, outputs


def read_test_program():
    i = 0
    # skip experiment data
    while True:
        exp = data[i]
        if not exp:
            break
        i += 4
    # skip empty lines
    while True:
        line = data[i]
        if line:
            break
        i += 1

    return (list(map(int, l.split())) for l in data[i:])


def reduce_opcodes():
    global opcodes

    queue = set(ops)
    while queue:
        for k, v in opcodes.items():
            if len(v) == 1:
                (r, ) = v
                if r not in queue:
                    continue
                break
        for k, v in opcodes.items():
            if len(v) > 1 and r in v:
                v.remove(r)
        queue.remove(r)

    opcodes = {k: v.pop() for k, v in opcodes.items()}


def part1():
    total = 0
    for ins, inputs, outputs in read_samples():
        matches = 0
        for n, fn in ops.items():
            regs = inputs[:]
            fn(regs, *ins[1:])
            if regs == outputs:
                opcodes[ins[0]].add(n)
                matches += 1
        if matches >= 3:
            total += 1
    return total


def part2():
    reduce_opcodes()
    regs = [0] * 4
    for ins in read_test_program():
        fn = ops[opcodes[ins[0]]]
        fn(regs, *ins[1:])
    return regs[0]


print(f"P1: {part1()}")
print(f"P2: {part2()}")
