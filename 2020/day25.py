#!/usr/bin/env python

with open("input25.txt") as f:
    pubkeys = [int(l) for l in f]

MAGIC = 20201227
SECRET = 7


def detect(secret, key):
    n = 0
    val = 1
    while val != key:
        n += 1
        val = (val * secret) % MAGIC
    return n


# https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange
# https://en.wikipedia.org/wiki/Modular_exponentiation
def part1():
    exp = [detect(SECRET, key) for key in pubkeys]
    enckeys = [pow(k, e, MAGIC) for k, e in zip(reversed(pubkeys), exp)]

    return enckeys[0]


print(f"P1: {part1()}")
