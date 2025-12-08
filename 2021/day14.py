#!/usr/bin/env python

from collections import Counter
from typing import TextIO

type Template = list[str]
type Match = tuple[str, str]
type Rules = dict[Match, str]


def parse_data(f: TextIO) -> tuple[Template, Rules]:
    def rule(line: str) -> tuple[Match, str]:
        adj, _, ins = line.split()
        return ((adj[0], adj[1]), ins)

    section1, section2 = f.read().split("\n\n")

    template = list(section1.strip())
    rules = dict(rule(r) for r in section2.splitlines())
    return template, rules


def count_polymers(template: Template, rules: Rules, steps: int) -> int:
    pair_count = Counter(t for t in zip(template[:-1], template[1:], strict=True))
    poly_count = Counter(template)
    for _ in range(steps):
        for (p1, p2), n in pair_count.copy().items():
            elem = rules[p1, p2]
            pair_count[p1, p2] -= n
            pair_count[p1, elem] += n
            pair_count[elem, p2] += n
            poly_count[elem] += n
    most, *_, least = poly_count.most_common()
    return most[1] - least[1]


def part1(template: Template, rules: Rules) -> int:
    return count_polymers(template, rules, 10)


def part2(template: Template, rules: Rules) -> int:
    return count_polymers(template, rules, 40)


def main() -> None:
    template, rules = parse_data(open(0))

    print(f"P1: {part1(template, rules)}")
    print(f"P2: {part2(template, rules)}")


if __name__ == "__main__":
    main()
