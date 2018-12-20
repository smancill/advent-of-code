#!/usr/bin/env python3

with open("input19.txt") as f:
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


def run(part2=False):
    regs = [0] * 6
    ip, prog = read_program()

    if part2:
        regs[0] = 1

    # get main register used by the program
    C = prog[4][-2]

    while 0 <= regs[ip] < len(prog):
        # Running Part 2 seems that it won't finish anytime soon.
        # Fix by intersecting and optimizing loop in instructions 1-16
        # The full program could be decompiled but the other instructions run
        # fast enough.
        if regs[ip] == 1:
            # Original loop:
            # for rA in 1..rC do
            #     for rB in 1..rC do
            #         if rA * rB == rC then
            #             r0 += rA
            n = regs[C]
            factors = set(f for i in range(1, int(n**0.5)+1)
                          if n % i == 0 for f in [i, n//i])
            regs[0] = sum(factors)
            regs[ip] = 256
        # execute instruction normally
        else:
            ins = prog[regs[ip]]
            ops[ins[0]](regs, *ins[1:])

        regs[ip] += 1

    return regs[0]


print(f"P1: {run(part2=False)}")
print(f"P2: {run(part2=True)}")
