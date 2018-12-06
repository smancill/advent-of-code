#!/usr/bin/env python3

import re
from collections import defaultdict

data = sorted(open("input04.txt"))

time_re = re.compile((r'\[.*(?P<hh>\d\d):(?P<mm>\d\d)\] (?P<log>.*)'))

guards = defaultdict(lambda: [0] * 60)

for record in data:
    match = time_re.search(record)
    if match:
        log = match.group('log')
        if log.startswith('Guard'):
            guard_id = int(log.split()[1][1:])
        elif log == 'falls asleep':
            t_start = (
                int(match.group('hh')),
                int(match.group('mm')),
            )
        elif log == 'wakes up':
            t_end = (
                int(match.group('hh')),
                int(match.group('mm')),
            )
            for i in range(t_start[1], t_end[1]):
                guards[guard_id][i] += 1

# By max total sleep time
totals = {k: sum(v) for k, v in guards.items()}
sleepy = max(totals, key=totals.get)
minute, _ = max(enumerate(guards[sleepy]), key=lambda t: t[1])
print(f"P1: {sleepy * minute}")

# By max sleep time in a single minute
totals = {k: max(v) for k, v in guards.items()}
sleepy = max(totals, key=totals.get)
minute, _ = max(enumerate(guards[sleepy]), key=lambda t: t[1])
print(f"P2: {sleepy * minute}")
