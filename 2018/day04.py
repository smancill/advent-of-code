#!/usr/bin/env python

import re
from collections import defaultdict
from typing import TextIO

type GuardSleep = dict[int, list[int]]


def parse_data(f: TextIO) -> GuardSleep:
    pattern = re.compile((r"\[.*(?P<hh>\d\d):(?P<mm>\d\d)\] (?P<log>.*)"))

    def get_time(m: re.Match[str]) -> tuple[int, int]:
        return (int(m.group("hh")), int(m.group("mm")))

    def slept(guard: int, begin: int, end: int) -> None:
        for i in range(begin, end):
            guards[guard][i] += 1

    guards = defaultdict[int, list[int]](lambda: [0] * 60)
    for record in sorted(f):
        if match := pattern.search(record):
            log = match.group("log")
            if log.startswith("Guard"):
                guard_id = int(log.split()[1][1:])
            elif log == "falls asleep":
                t_start = get_time(match)
            elif log == "wakes up":
                t_end = get_time(match)
                slept(guard_id, t_start[1], t_end[1])
    return guards


def part1(guards: GuardSleep) -> int:
    """By max total sleep time"""
    totals = {k: sum(v) for k, v in guards.items()}
    sleepy = max(totals, key=lambda k: totals[k])
    minute, _ = max(enumerate(guards[sleepy]), key=lambda t: t[1])
    return sleepy * minute


def part2(guards: GuardSleep) -> int:
    """By max sleep time in a single minute"""
    totals = {k: max(v) for k, v in guards.items()}
    sleepy = max(totals, key=lambda k: totals[k])
    minute, _ = max(enumerate(guards[sleepy]), key=lambda t: t[1])
    return sleepy * minute


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
