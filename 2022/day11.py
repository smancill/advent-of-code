#!/usr/bin/env python

import math
import operator
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, replace
from typing import Final, TextIO

type WorryLevelFn = Callable[[int, int], int]

operators: Final[Mapping[str, WorryLevelFn]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
}


@dataclass
class Operation:
    op: WorryLevelFn
    arg: int | None = None

    def __call__(self, old: int) -> int:
        return self.op(old, old if self.arg is None else self.arg)


@dataclass
class Monkey:
    id: int
    items: list[int]
    op: Operation
    divisor: int
    targets: tuple[int, int]
    inspected: int = 0

    def target(self, item: int) -> int:
        idx = 0 if item % self.divisor == 0 else 1
        return self.targets[idx]

    def worry_level(self, item: int) -> int:
        return self.op(item)

    def receive(self, item: int) -> None:
        self.items.append(item)


def parse_data(f: TextIO) -> list[Monkey]:
    def parse_id(line: str) -> int:
        _, id = line.rstrip(":").split()
        return int(id)

    def parse_items(line: str) -> list[int]:
        _, items = line.split(": ")
        return [int(i) for i in items.split(", ")]

    def parse_op(line: str) -> Operation:
        tokens = line.strip().removeprefix("Operation:").split()
        match tokens:
            case ["new", "=", "old", op, "old"]:
                return Operation(operators[op])
            case ["new", "=", "old", op, val]:
                return Operation(operators[op], int(val))
            case _:
                raise ValueError(line)

    def parse_divisor(line: str) -> int:
        *_, div = line.split()
        return int(div)

    def parse_targets(lines: list[str]) -> tuple[int, int]:
        *_, m1 = lines[0].split()
        *_, m2 = lines[1].split()
        return int(m1), int(m2)

    def parse_monkey(lines: list[str]) -> Monkey:
        id = parse_id(lines[0])
        items = parse_items(lines[1])
        op = parse_op(lines[2])
        div = parse_divisor(lines[3])
        targets = parse_targets(lines[4:])
        return Monkey(id, items, op, div, targets)

    return [parse_monkey(s.splitlines()) for s in f.read().split("\n\n")]


def inspection(
    monkeys: list[Monkey], *, rounds: int = 20, relief: Callable[[int], int]
) -> int:
    for _ in range(rounds):
        for monkey in monkeys:
            for item in monkey.items:
                item = monkey.worry_level(item)
                item = relief(item)
                target = monkey.target(item)
                monkeys[target].receive(item)
                monkey.inspected += 1
            monkey.items = []

    m1, m2, *_ = sorted(monkeys, key=lambda m: m.inspected, reverse=True)
    return m1.inspected * m2.inspected


def part1(data: Sequence[Monkey]) -> int:
    monkeys = [replace(m, items=list(m.items)) for m in data]
    return inspection(monkeys, rounds=20, relief=lambda w: w // 3)


def part2(data: Sequence[Monkey]) -> int:
    monkeys = [replace(m, items=list(m.items)) for m in data]
    divisor = math.prod(m.divisor for m in data)
    return inspection(monkeys, rounds=10000, relief=lambda w: w % divisor)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
