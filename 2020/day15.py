#!/usr/bin/env python

with open("input15.txt") as f:
    data = [int(i) for i in f.read().split(',')]


def find_number(turns):
    prev = {n: i + 1 for i, n in enumerate(data)}
    last = data[-1]
    for i in range(len(data), turns):
        prev[last], last = i, i - prev[last] if last in prev else 0
    return last


print(f"P1: {find_number(2020)}")
print(f"P2: {find_number(30000000)}")
