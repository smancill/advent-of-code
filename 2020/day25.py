#!/usr/bin/env python

from typing import Final, TextIO

MAGIC: Final = 20201227
SECRET: Final = 7


def parse_data(f: TextIO) -> tuple[int, int]:
    card_key, door_key = [int(l) for l in f]
    return card_key, door_key


def detect(secret: int, key: int) -> int:
    n = 0
    val = 1
    while val != key:
        n += 1
        val = (val * secret) % MAGIC
    return n


# https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange
# https://en.wikipedia.org/wiki/Modular_exponentiation
def part1(pubkeys: tuple[int, int]) -> int:
    exp = [detect(SECRET, key) for key in pubkeys]
    enckeys = [pow(k, e, MAGIC) for k, e in zip(reversed(pubkeys), exp, strict=True)]

    return enckeys[0]


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")


if __name__ == "__main__":
    main()
