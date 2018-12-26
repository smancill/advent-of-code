#!/usr/bin/env python3

with open("input21.txt") as f:
    data = f.readlines()


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


def read_program():
    ip = int(data[0].split()[-1])

    ins = []
    for l in data[1:]:
        t = l.split()
        i = [t[0]] + list(map(int, t[1:]))
        ins.append(i)

    return ip, ins


def run(part1=True):
    regs = [0] * 6
    ip, prog = read_program()

    # get important registers
    main, opt = prog[5][-1], prog[26][-1]

    seen = set()
    prev = None

    while 0 <= regs[ip] < len(prog):
        # intersect instruction for halt condition
        if regs[ip] == 28:
            val = regs[main]
            if part1:
                return val
            if val in seen:
                return prev
            seen.add(val)
            prev = val
            regs[ip] = 5
        # optimize loop in instructions 17-27
        elif regs[ip] == 17:
            regs[opt] //= 256
            regs[ip] = 7
        # execute instruction normally
        else:
            ins = prog[regs[ip]]
            ops[ins[0]](regs, *ins[1:])

        regs[ip] += 1


print(f"P1: {run(part1=True)}")
print(f"P2: {run(part1=False)}")
