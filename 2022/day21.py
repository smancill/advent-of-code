#!/usr/bin/env python

from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace
from types import MappingProxyType
from typing import Final, TextIO


@dataclass(frozen=True)
class Operation:
    lhs: str
    rhs: str
    op: str


type Operator = Callable[[int, int], int]
type Action = int | Operation


operators: Final = MappingProxyType(
    {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a // b,
    }
)


def parse_data(f: TextIO) -> dict[str, Action]:
    def parse_monkey(line: str) -> tuple[str, Action]:
        name, action = line.split(":")
        match action.split():
            case [m1, op, m2]:
                return name, Operation(m1, m2, op)
            case [n]:
                return name, int(n)
            case _:
                raise ValueError(line)

    return dict(parse_monkey(l) for l in f)


class Evaluator:
    _tree: Final[Mapping[str, Action]]
    _operators: Final[Mapping[str, Operator]]

    def __init__(self, tree: Mapping[str, Action], operators: Mapping[str, Operator]):
        self._tree = tree
        self._operators = operators

    def eval(self, node: str = "root") -> int:
        match self._tree[node]:
            case int(x):
                return x
            case Operation(lhs, rhs, op):
                return self._operators[op](self.eval(lhs), self.eval(rhs))
            case other:
                raise ValueError(f"invalid action: {other}")


def part1(data: Mapping[str, Action]) -> int:
    evaluator = Evaluator(data, operators)
    return evaluator.eval()


def part2(data: Mapping[str, Action]) -> int:
    # Use cmp() function as the new "root" operator.
    # The root eval of numbers near the wanted number X will be either:
    #
    #  X-3       X       X+3
    #   1  1  1  0 -1 -1 -1
    #
    # or:
    #
    #  X-3       X       X+3
    #  -1 -1 -1  0  1  1  1
    #
    # This will allow to use binary searh to find the wanted number.

    def cmp(a: int, b: int) -> int:
        return (a > b) - (a < b)

    def eval(x: int) -> int:
        tree["humn"] = x
        return evaluator.eval()

    root = data["root"]
    assert isinstance(root, Operation)

    tree = dict(data) | {"root": replace(root, op="=")}
    evaluator = Evaluator(tree, operators | {"=": cmp})

    # Find search boundaries.
    target = 1
    result = eval(target)
    lower = result

    # Eval until the cmp() result changes
    while result == lower:
        target *= 10
        result = eval(target)
    low = target // 10
    high = target
    upper = result

    # Find target value using binary search.
    #
    # Example: T is left of X, so (R := eval(T)) == L.
    # For next iteration: l = T
    #
    #   l              T     X        h
    #   1  1  1  1  1  1  1  0 -1 -1 -1
    #     L=1          R         U=-1
    #
    # Example: T is right of X, so (R := eval(T)) == U.
    # For next iteration: h = T
    #
    #   l        X     T              h
    #   1  1  1  0 -1 -1 -1 -1 -1 -1 -1
    #     L=1          R         U=-1
    #
    while result != 0:
        target = (high + low) // 2
        result = eval(target)
        if result == lower:
            low = target
        elif result == upper:
            high = target

    return target


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
