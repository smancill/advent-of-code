#!/usr/bin/env python

ORDER = {'(': 30, '*': 20, '+': 20}

OP = {
    '+': lambda a, b: a + b,
    '*': lambda a, b: a * b,
}

with open("input18.txt") as f:
    data = [e.replace('(', ' ( ').replace(')', ' ) ').split()
            for e in f.readlines()]


def eval_rpn(rpn):
    s = []
    for c in rpn:
        if c.isnumeric():
            s.append(int(c))
        else:
            b, a = s.pop(), s.pop()
            s.append(OP[c](a, b))
    return s.pop()


# See <https://en.wikipedia.org/wiki/Shunting-yard_algorithm>
def to_rpn(exp, order=ORDER):
    rpn = ""
    ops = []

    for c in exp:
        if c.isnumeric():
            rpn += c
        elif c in order:
            while ops and order[ops[-1]] > order[c] and ops[-1] != '(':
                rpn += ops.pop()
            ops.append(c)
        elif c == '(':
            ops.append(c)
        elif c == ')':
            while ops and ops[-1] != '(':
                rpn += ops.pop()
            if ops[-1] == '(':
                ops.pop()

    while ops:
        rpn += ops.pop()

    return rpn


def part1():
    return sum(eval_rpn(to_rpn(exp)) for exp in data)


def part2():
    order = ORDER | {'*': 10}
    return sum(eval_rpn(to_rpn(exp, order)) for exp in data)


print(f"P1: {part1()}")
print(f"P2: {part2()}")
