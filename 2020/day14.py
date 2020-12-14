#!/usr/bin/env python

import re

with open("input14.txt") as f:
    data = f.readlines()


def read_mask(line):
    return re.search(r'[X01]+', line)[0]


def read_value(line):
    return tuple(map(int, re.findall(r'mem\[(\d+)] = (\d+)', line)[0]))


def part1():
    def apply_mask(mask, n):
        n = f'{n:>036b}'
        n = ''.join(b if m == 'X' else m for b, m in zip(n, mask))
        return int(n, 2)

    mem = {}

    for line in data:
        if line.startswith('mask'):
            mask = read_mask(line)
        else:
            addr, value = read_value(line)
            mem[addr] = apply_mask(mask, value)

    return sum(mem.values())


def part2():
    def apply_mask(mask, addr):
        addr = f'{addr:>036b}'
        addr = ''.join(b if m == '0' else m for b, m in zip(addr, mask))
        return gen_address(addr)

    def gen_address(addr):
        queue = {addr}
        while queue:
            item = queue.pop()
            if 'X' in item:
                queue.add(item.replace('X', '0', 1))
                queue.add(item.replace('X', '1', 1))
            else:
                yield int(item, 2)

    mem = {}

    for line in data:
        if line.startswith('mask'):
            mask = read_mask(line)
        else:
            addr, value = read_value(line)
            for a in apply_mask(mask, addr):
                mem[a] = value

    return sum(mem.values())


print(f"P1: {part1()}")
print(f"P2: {part2()}")
