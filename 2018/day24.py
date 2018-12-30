#!/usr/bin/env python3

import re

from itertools import count

with open("input24.txt") as f:
    data = f.read().split('\n\n')
    verbose = False


class Group():
    def __init__(self, id, side, **kwargs):
        self.id = id
        self.side = side
        self.units = int(kwargs['units'])
        self.hp = int(kwargs['hp'])
        self.atk_dmg = int(kwargs['atk_dmg']) + kwargs['boost']
        self.atk_type = kwargs['atk_type']
        self.ini = int(kwargs['ini'])
        self.weak = kwargs['weak']
        self.immune = kwargs['immune']

    @property
    def atk(self):
        return self.units * self.atk_dmg

    def dmg(self, enemy):
        if self.atk_type in enemy.immune:
            return 0
        elif self.atk_type in enemy.weak:
            return 2 * self.atk
        else:
            return self.atk

    def __str__(self):
        return (f"{{"
                f"id: {self.id}, "
                f"units: {self.units}, "
                f"hp: {self.hp}, "
                f"atk_dmg: {self.atk_dmg}, "
                f"atk_type: '{self.atk_type}', "
                f"ini: {self.ini}, "
                f"weak: {self.weak or '{}'}, "
                f"immune: {self.immune or '{}'}"
                f"}}")


def parse_army(data, boost=0, show=False):
    group_re = re.compile(
        r'(?P<units>\d+) units each with (?P<hp>\d+) hit points '
        r'(?:\((?P<effects>.*)\) )?'
        r'with an attack that does (?P<atk_dmg>\d+) (?P<atk_type>\w+) '
        r'damage at initiative (?P<ini>\d+)'
    )

    def parse_effects(src):
        effects = {'weak': set(), 'immune': set()}
        if src:
            for group in src.split('; '):
                k, v = group.split(' to ')
                effects[k] = set(v.split(', '))
        return effects

    name, *groups = data.splitlines()
    name = name.replace(':', '')
    if show:
        print(f"{name}:")

    army = []
    for i, line in enumerate(groups):
        match = group_re.match(line)
        if match:
            kwargs = {**match.groupdict()}
            kwargs.update(parse_effects(match.group('effects')))
            kwargs.update({'boost': boost})
            group = Group(i+1, name, **kwargs)
            if show:
                print(f"  {group}")
            army.append(group)
    if show:
        print()

    return army


def show_groups(immune_sys, infection):
    def show(side, groups):
        print(f"{side}:")
        if groups:
            for g in groups:
                print(f"Group {g.id} contains {g.units} units")
        else:
            print("No groups remain.")

    show("Immune System", immune_sys)
    show("Infection", infection)
    print()


def select_targets(immune_sys, infection):
    all_targets = []

    def select(army, enemies):
        targets = []
        enemies = set(enemies)
        for group in sorted(army, key=lambda g: (g.atk, g.ini), reverse=True):
            if not enemies:
                break
            target = max(enemies, key=lambda e: (group.dmg(e), e.atk, e.ini))
            if group.dmg(target) > 0:
                targets.append((group, target))
                enemies.remove(target)
        return targets

    all_targets += select(infection, immune_sys)
    all_targets += select(immune_sys, infection)

    return all_targets


def attack_targets(immune_sys, infection, targets):
    total_killed = 0
    for group, target in sorted(targets, key=lambda t: t[0].ini, reverse=True):
        if group.atk < 0:
            # Group was destroyed by a previous attack
            continue
        killed = min(group.dmg(target) // target.hp, target.units)
        target.units -= killed
        total_killed += killed
        if verbose:
            print(f"{group.side} group {group.id} attacks "
                  f"defending group {target.id}, killing {killed} units")
        if target.units <= 0:
            if target in immune_sys:
                immune_sys.remove(target)
            else:
                infection.remove(target)
    if verbose:
        print()
    return total_killed


def battle(immune_sys, infection):
    if verbose:
        show_groups(immune_sys, infection)

    while immune_sys and infection:
        targets = select_targets(immune_sys, infection)
        destroyed = attack_targets(immune_sys, infection, targets)
        # Part 2 would loop forever without this check
        if destroyed == 0:
            return None, None
        if verbose:
            show_groups(immune_sys, infection)

    winner = max(immune_sys, infection, key=len)
    return bool(immune_sys), sum(g.units for g in winner)


def part1():
    immune_sys = parse_army(data[0], show=False)
    infection = parse_army(data[1], show=False)
    _, units = battle(immune_sys, infection)
    return units


def part2():
    for boost in count(1):
        immune_sys = parse_army(data[0], boost=boost)
        infection = parse_army(data[1])
        survived, units = battle(immune_sys, infection)
        if survived:
            return boost, units


print(f"P1: {part1()}")
print(f"P2: {part2()[1]}")
