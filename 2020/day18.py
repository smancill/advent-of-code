#!/usr/bin/env python

from collections.abc import Callable, Mapping, Sequence
from typing import Final, TextIO

type Order = Mapping[str, int]
type Operator = Callable[[int, int], int]


operator_order_1: Final[Order] = {"(": 30, "*": 20, "+": 20}
operator_order_2: Final[Order] = {"(": 30, "*": 10, "+": 20}

operator_fn: Final[Mapping[str, Operator]] = {
    "+": lambda a, b: a + b,
    "*": lambda a, b: a * b,
}


def read_data(f: TextIO) -> list[str]:
    return f.readlines()


def eval_rpn(rpn: str) -> int:
    stack = []
    for c in rpn:
        if c.isnumeric():
            stack.append(int(c))
        else:
            b, a = stack.pop(), stack.pop()
            fn = operator_fn[c]
            stack.append(fn(a, b))
    return stack.pop()


def tokenize(expr: str) -> list[str]:
    return expr.replace("(", " ( ").replace(")", " ) ").split()


# See <https://en.wikipedia.org/wiki/Shunting-yard_algorithm>
def to_rpn(expr: str, order: Order) -> str:
    rpn = ""
    ops: list[str] = []

    for token in tokenize(expr):
        if token.isnumeric():
            rpn += token
        elif token in order:
            while ops and order[token] <= order[ops[-1]] and ops[-1] != "(":
                rpn += ops.pop()
            ops.append(token)
        elif token == "(":
            ops.append(token)
        elif token == ")":
            while ops and ops[-1] != "(":
                rpn += ops.pop()
            if ops[-1] == "(":
                ops.pop()

    while ops:
        rpn += ops.pop()

    return rpn


def part1(data: Sequence[str]) -> int:
    return sum(eval_rpn(to_rpn(expr, operator_order_1)) for expr in data)


def part2(data: Sequence[str]) -> int:
    return sum(eval_rpn(to_rpn(expr, operator_order_2)) for expr in data)


def main() -> None:
    data = read_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
