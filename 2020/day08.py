#!/usr/bin/env python

with open("input08.txt") as f:
    data = [[op, int(arg)] for op, arg in (ins.split() for ins in f)]


def run(prog):
    n = len(prog)
    visited = [False] * n
    ip = 0
    acc = 0

    while True:
        if visited[ip]:
            break
        visited[ip] = True

        op, arg = prog[ip]
        if op == 'acc':
            ip += 1
            acc += arg
        elif op == 'jmp':
            ip += arg
        elif op == 'nop':
            ip += 1

        if ip == n:
            break

    return ip, acc


def part1():
    return run(data)[1]


def part2():
    n = len(data)
    for i in range(len(data)):
        op = data[i][0]
        if op == 'nop':
            data[i][0] = 'jmp'
        elif op == 'jmp':
            data[i][0] = 'nop'
        else:
            continue
        ip, acc = run(data)
        if ip == n:
            return acc
        data[i][0] = op


print(f"P1: {part1()}")
print(f"P2: {part2()}")
