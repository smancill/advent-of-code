#!/usr/bin/env python

import re
from collections.abc import Sequence
from typing import Final, Mapping, TextIO, TypeAlias

Quantity: TypeAlias = tuple[int, str]
Rules: TypeAlias = Mapping[str, Sequence[Quantity]]

BAG: Final = "shiny gold"


def parse_data(f: TextIO) -> Rules:
    def parse_bag(rule: str) -> str:
        if match := re.match(r"\w+ \w+", rule):
            return match[0]
        raise ValueError(rule)

    def parse_content(rule: str) -> list[Quantity]:
        matches = re.findall(r"(\d+) (\w+ \w+)", rule)
        return [(int(q), b) for q, b in matches]

    return {parse_bag(r): parse_content(r) for r in f}


def part1(rules: Rules) -> int:
    # Solve without recursion
    def contains(bag: str, target: str) -> bool:
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


def part2(rules: Rules) -> int:
    # Solve without recursion
    def count_content(bag: str) -> int:
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


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
