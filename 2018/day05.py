#!/usr/bin/env python3

from string import ascii_lowercase

with open("input05.txt") as f:
    data = f.read().strip()


def react(polymer):
    result = []
    for unit in polymer:
        if result:
            a = ord(unit)
            b = ord(result[-1])
            if a - 32 == b or a + 32 == b:
                result.pop()
                continue
        result.append(unit)
    return len(result)


def check_all():
    for c in ascii_lowercase:
        s = data.replace(c, '').replace(c.upper(), '')
        yield react(s)


print(f"P1: {react(data)}")
print(f"P2: {min(check_all())}")
