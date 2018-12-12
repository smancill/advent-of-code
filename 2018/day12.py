#!/usr/bin/env python3

with open("input12.txt") as f:
    data = [l.strip() for l in f]

state = data[0][15:]
notes = {l[:5]: l[-1] for l in data[2:]}


def spread_plants(NG):
    L = 3
    # Use L dots at each side, because rules go from i-2 to i+2
    pots = '...' + state + '...'
    # The index of the pot 0
    idx = L

    for g in range(NG):
        new_gen = ['.'] * len(pots)
        for i in range(2, len(pots) - 2):
            new_gen[i] = notes[pots[i-2:i+3]]
        new_gen = ''.join(new_gen)

        # Keep at least L dots at the end of the state
        if '#' in new_gen[-L:]:
            new_gen = new_gen + '.'

        # Keep L dots at the beginning of the state, and remove extra dots
        # (to keep it of printable size). Adjust the zero index accordingly.
        if '#' in new_gen[:L]:
            new_gen = '.' + new_gen
            idx += 1
        else:
            f = new_gen.index('#')
            new_gen = new_gen[f-L:]
            idx -= f - L
            # After a while all states are the same but shifted to the right
            # <https://en.wikipedia.org/wiki/Glider_(Conway%27s_Life)>
            # so no need to iterate, just calculate the zero index for the
            # remaining iterations
            if new_gen == pots:
                idx -= (NG - g - 1) * (f - L)
                break

        pots = new_gen

    return pots, idx


def sum_pots(pots, idx):
    return sum(i - idx for i, p in enumerate(pots) if p == '#')


pots1, idx1 = spread_plants(20)
sum1 = sum_pots(pots1, idx1)
print(f"P1: {sum1}")

pots2, idx2 = spread_plants(50000000000)
sum2 = sum_pots(pots2, idx2)
print(f"P2: {sum2}")
