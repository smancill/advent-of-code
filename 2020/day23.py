#!/usr/bin/env python

with open("input23.txt") as f:
    cups = [int(c) for c in f.read().strip()]


def arrange(cups, moves=10):
    mc = len(cups)

    # Create linked list (index -> value)
    linked = [0] * (mc + 1)
    for i in range(0, mc - 1):
        linked[cups[i]] = cups[i+1]
    linked[cups[-1]] = cups[0]

    current = cups[0]
    for _ in range(moves):
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
                dest = mc

        # Add pickups after dest
        linked[p3] = linked[dest]
        linked[dest] = p1

        # Select next cup
        current = linked[current]

    return linked


def part1():
    linked = arrange(cups, moves=100)
    result = ''
    target = 1
    dest = linked[target]
    while dest != target:
        result += str(dest)
        dest = linked[dest]
    return result


def part2():
    n, m = max(cups) + 1, 1_000_000 + 1
    linked = arrange(cups + list(range(n, m)), moves=10_000_000)
    a = linked[1]
    b = linked[a]
    return a * b


print(f"P1: {part1()}")
print(f"P2: {part2()}")
