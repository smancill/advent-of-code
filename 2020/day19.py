#!/usr/bin/env python

def parse_rule(rule):
    n, r = rule.split(':')
    if '"' in r:
        r = r.strip().replace('"', '')
    else:
        r = [list(map(int, s.split())) for s in r.split('|')]
    return (int(n), r)


with open("input19.txt") as f:
    rules, messages = f.read().split('\n\n')
    rules = dict(parse_rule(r) for r in rules.splitlines())
    messages = messages.splitlines()


def match_message(msg, rule_id=0):
    last = len(msg) - 1
    queue = []
    queue.append((0, [rule_id]))
    while queue:
        i, seq = queue.pop()
        current = rules[seq[0]]
        if type(current) == list:
            for s in reversed(current):
                queue.append((i, s + seq[1:]))
        else:
            if msg[i] == current:
                if i == last:
                    if len(seq) == 1:
                        return True
                else:
                    if len(seq) > 1:
                        queue.append((i+1, seq[1:]))
    return False


def part1():
    return sum(1 for m in messages if match_message(m))


def part2():
    rules[8] = [[42], [42, 8]]
    rules[11] = [[42, 31], [42, 11, 31]]

    return sum(1 for m in messages if match_message(m))


print(f"P1: {part1()}")
print(f"P2: {part2()}")
