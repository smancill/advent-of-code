#!/usr/bin/env python

import re
from collections.abc import Iterator, Sequence
from typing import TextIO


def read_data(f: TextIO) -> list[str]:
    return f.readlines()


def _to_binary(i: int) -> str:
    return f"{i:>036b}"


def parse_mask(line: str) -> str:
    if match := re.search(r"[X01]+", line):
        return match[0]
    raise ValueError(line)


def parse_write(line: str) -> tuple[int, int]:
    if match := re.match(r"mem\[(\d+)] = (\d+)", line):
        addr, val = map(int, match.group(1, 2))
        return addr, val
    raise ValueError(line)


def part1(data: Sequence[str]) -> int:
    def apply_mask(mask: str, n: str) -> int:
        n = "".join(b if m == "X" else m for b, m in zip(n, mask))
        return int(n, 2)

    mem = {}

    for line in data:
        if line.startswith("mask"):
            mask = parse_mask(line)
        else:
            addr, value = parse_write(line)
            mem[addr] = apply_mask(mask, _to_binary(value))

    return sum(mem.values())


def part2(data: Sequence[str]) -> int:
    def apply_mask(mask: str, addr: str) -> Iterator[int]:
        addr = "".join(b if m == "0" else m for b, m in zip(addr, mask))
        return gen_address(addr)

    def gen_address(addr: str) -> Iterator[int]:
        queue = {addr}
        while queue:
            item = queue.pop()
            if "X" in item:
                queue.add(item.replace("X", "0", 1))
                queue.add(item.replace("X", "1", 1))
            else:
                yield int(item, 2)

    mem = {}

    for line in data:
        if line.startswith("mask"):
            mask = parse_mask(line)
        else:
            addr, value = parse_write(line)
            for a in apply_mask(mask, _to_binary(addr)):
                mem[a] = value

    return sum(mem.values())


def main() -> None:
    data = read_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
