#!/usr/bin/env python

from collections.abc import Mapping
from typing import Final, TextIO

type Notes = Mapping[str, str]

NO_PLANT: Final = "."
PLANT: Final = "#"

L: Final = 3


def parse_data(f: TextIO) -> tuple[str, Notes]:
    def parse_state(line: str) -> str:
        _, state = line.split(": ")
        return state

    def parse_note(line: str) -> tuple[str, str]:
        current, _, next = line.split()
        return current, next

    header, _, *data = [l.rstrip() for l in f]

    state = parse_state(header)
    notes = dict(parse_note(l) for l in data)
    return state, notes


def spread_plants(state: str, notes: Notes, total_gen: int) -> tuple[str, int]:
    # The rules go from i-2 to i+2 for each pot i
    # Add L <no_plant> at each side
    pots = NO_PLANT * L + state + NO_PLANT * L
    # The index of the pot 0
    idx = L

    for i in range(total_gen):
        # Apply rules
        tmp = [NO_PLANT] * len(pots)
        for j in range(2, len(pots) - 2):
            tmp[j] = notes.get(pots[j - 2 : j + 3], NO_PLANT)
        new_gen = "".join(tmp)

        # Keep at least L <no_plant> at the end of the state
        if PLANT in new_gen[-L:]:
            new_gen = new_gen + NO_PLANT

        # Keep L <no_plant> at the beginning of the state, removing extra
        # (to keep it of printable size).
        # Adjust the zero index accordingly.
        if PLANT in new_gen[:L]:
            new_gen = NO_PLANT + new_gen
            idx += 1
        else:
            f = new_gen.index(PLANT) - L
            new_gen = new_gen[f:]
            idx -= f
            # After a while all states are the same but shifted to the right
            # <https://en.wikipedia.org/wiki/Glider_(Conway%27s_Life)>
            # so no need to iterate, just calculate the zero index for the
            # remaining iterations
            if new_gen == pots:
                idx -= (total_gen - i - 1) * f
                break

        pots = new_gen

    return pots, idx


def sum_pots(pots: str, idx: int) -> int:
    return sum(i - idx for i, p in enumerate(pots) if p == PLANT)


def part1(state: str, notes: Notes) -> int:
    pots, idx = spread_plants(state, notes, 20)
    return sum_pots(pots, idx)


def part2(state: str, notes: Notes) -> int:
    pots, idx = spread_plants(state, notes, 50_000_000_000)
    return sum_pots(pots, idx)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(*data)}")
    print(f"P2: {part2(*data)}")


if __name__ == "__main__":
    main()
