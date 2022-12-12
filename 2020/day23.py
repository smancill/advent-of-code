#!/usr/bin/env python

import logging
import logging.config
from collections.abc import Sequence
from typing import TextIO


def parse_data(f: TextIO) -> list[int]:
    return [int(l) for l in f.read().strip()]


def _log_cups(linked: Sequence[int], current: int, move: int) -> None:
    if not logging.getLogger().isEnabledFor(logging.DEBUG):
        return

    cups = [current]
    cup = linked[current]
    while cup != current:
        cups.append(cup)
        cup = linked[cup]

    shift = move % len(cups)
    if shift > 0:
        cups = cups[-shift:] + cups[:-shift]

    out = "".join(f' {c} ' for c in cups).replace(f" {current} ", f"({current})")
    logging.debug(f"cups: {out}")


def _log_move(linked: Sequence[int], current: int, move: int) -> None:
    logging.debug(f"-- move {move + 1} --")
    _log_cups(linked, current, move)


def _log_dest(pickups: Sequence[int], dest: int) -> None:
    if not logging.getLogger().isEnabledFor(logging.DEBUG):
        return
    logging.debug(f"pick up: {', '.join(str(p) for p in pickups)}")
    logging.debug(f"destination: {dest}\n")


def _log_final(linked: Sequence[int], current: int, move: int) -> None:
    logging.debug("-- final --")
    _log_cups(linked, current, move)


def arrange(cups: Sequence[int], *, moves: int) -> list[int]:
    n_cups = len(cups)

    # Create linked list (index -> value)
    linked = [0] * (n_cups + 1)
    for i in range(0, n_cups - 1):
        linked[cups[i]] = cups[i + 1]
    linked[cups[-1]] = cups[0]

    current = cups[0]
    for i in range(moves):
        _log_move(linked, current, i)

        # Pickup cups
        p1 = linked[current]
        p2 = linked[p1]
        p3 = linked[p2]

        # Remove pickups
        linked[current] = linked[p3]

        # Find dest
        ignored = (current, p1, p2, p3)
        dest = current
        while dest in ignored:
            dest -= 1
            if dest == 0:
                dest = n_cups
        _log_dest((p1, p2, p3), dest)

        # Add pickups after dest
        linked[p3] = linked[dest]
        linked[dest] = p1

        # Select next cup
        current = linked[current]

    _log_final(linked, current, moves)
    return linked


def part1(cups: Sequence[int]) -> str:
    linked = arrange(cups, moves=100)
    result = ""
    target = 1
    dest = linked[target]
    while dest != target:
        result += str(dest)
        dest = linked[dest]
    return result


def part2(cups: Sequence[int]) -> int:
    n, m = max(cups) + 1, 1_000_000 + 1
    cups = list(cups) + list(range(n, m))
    linked = arrange(cups, moves=10_000_000)
    a = linked[1]
    b = linked[a]
    return a * b


def main() -> None:
    logging.config.fileConfig("../logging.conf")

    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
