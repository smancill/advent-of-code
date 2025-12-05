#!/usr/bin/env python

from collections.abc import Sequence
from typing import TextIO, TypeAlias

Rule: TypeAlias = str | list[list[int]]
Rules: TypeAlias = dict[int, Rule]


def parse_data(f: TextIO) -> tuple[Rules, list[str]]:
    def parse_match(rule: str) -> Rule:
        if '"' in rule:
            return rule.strip().replace('"', "")
        subrules = [s.split() for s in rule.split("|")]
        return [list(map(int, s)) for s in subrules]

    def parse_rule(line: str) -> tuple[int, Rule]:
        n, r = line.split(":")
        return int(n), parse_match(r)

    sections = [s.splitlines() for s in f.read().split("\n\n")]
    rules = dict(parse_rule(r) for r in sections[0])
    messages = sections[1]

    return rules, messages


def match_message(msg: str, rules: Rules, rule_id: int = 0) -> bool:
    last = len(msg) - 1
    queue = [(0, [rule_id])]
    while queue:
        i, seq = queue.pop()
        current = rules[seq[0]]
        if isinstance(current, str):
            if msg[i] == current:
                if i == last:
                    if len(seq) == 1:
                        return True
                else:
                    if len(seq) > 1:
                        queue.append((i + 1, seq[1:]))
        else:
            for s in reversed(current):
                queue.append((i, s + seq[1:]))
    return False


def part1(rules: Rules, messages: Sequence[str]) -> int:
    return sum(1 for m in messages if match_message(m, rules))


def part2(rules: Rules, messages: Sequence[str]) -> int:
    rules = rules.copy()
    rules[8] = [[42], [42, 8]]
    rules[11] = [[42, 31], [42, 11, 31]]

    return sum(1 for m in messages if match_message(m, rules))


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(*data)}")
    print(f"P2: {part2(*data)}")


if __name__ == "__main__":
    main()
