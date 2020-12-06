#!/usr/bin/env python

# Boarding passes are actually binary numbers,
# described in a fancy way
to_binary = str.maketrans('FBLR', '0101')

with open("input05.txt") as f:
    seats = [int(bp.strip().translate(to_binary), 2) for bp in f]


def part1():
    return max(seats)


def part2():
    # All seats are occupied sequentially except one somewhere in between,
    # so the sum of all the numbers in the expected sequence
    # minus the sum of all the scanned numbers
    # will give the one missing seat number
    all_seats = range(min(seats), max(seats) + 1)
    return sum(all_seats) - sum(seats)


print(f"P1: {part1()}")
print(f"P2: {part2()}")
