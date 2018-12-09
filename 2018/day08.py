#!/usr/bin/env python3

from collections import deque

with open("input08.txt") as f:
    data = [int(l) for l in f.read().split()]


def parse1(tree):
    nc = tree.popleft()
    nm = tree.popleft()

    mc = [parse1(tree) for _ in range(nc)]
    me = [tree.popleft() for _ in range(nm)]

    return sum(mc) + sum(me)


def parse2(tree):
    nc = tree.popleft()
    nm = tree.popleft()

    mc = {i+1: parse2(tree) for i in range(nc)}
    me = [tree.popleft() for _ in range(nm)]

    if nc == 0:
        return sum(me)
    return sum(mc.get(i, 0) for i in me)


print(f"P1: {parse1(deque(data))}")
print(f"P2: {parse2(deque(data))}")
