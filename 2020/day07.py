#!/usr/bin/env python

import re

with open("input07.txt") as f:
    rules = {
        re.match(r"\w+ \w+", r)[0]:
        [(int(q), b) for q, b in re.findall(r"(\d+) (\w+ \w+)", r)]
        for r in f
    }

BAG = "shiny gold"


def part1():
    def contains(bag, target):
        visited = set()
        queue = set(b for _, b in rules[bag])
        while queue:
            current = queue.pop()
            if current in visited:
                continue
            if current == target:
                return True
            visited.add(current)
            queue.update(b for _, b in rules[current])
        return False

    return sum(1 for bag in rules if contains(bag, BAG))


def part2():
    def count_content(bag):
        counter = {}
        stack = [bag]
        while stack:
            current = stack[-1]
            content = rules[current]
            if current not in counter:
                stack.extend(b for _, b in content)
                counter[current] = 0
                continue
            counter[current] = sum(q + q * counter[b] for q, b in content)
            stack.pop()
        return counter[bag]

    return count_content(BAG)


print(f"P1: {part1()}")
print(f"P2: {part2()}")
