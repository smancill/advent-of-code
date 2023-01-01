#!/usr/bin/env python

import logging
import logging.config
import re
from collections.abc import Sequence, Set
from dataclasses import dataclass
from itertools import count
from typing import Any, Final, Self, TextIO, TypeAlias


@dataclass
class Group:
    id: Final[int]
    side: Final[str]
    units: int
    hp: Final[int]
    atk_dmg: Final[int]
    atk_type: Final[str]
    ini: Final[int]
    weak: Final[Set[str]]
    immune: Final[Set[str]]

    @property
    def power(self) -> int:
        return self.units * self.atk_dmg

    def dmg(self, enemy: Self) -> int:
        if self.atk_type in enemy.immune:
            return 0
        elif self.atk_type in enemy.weak:
            return 2 * self.power
        else:
            return self.power

    def attack(self, enemy: Self) -> int:
        killed = min(self.dmg(enemy) // enemy.hp, enemy.units)
        enemy.units -= killed
        return killed

    def is_destroyed(self) -> bool:
        return self.units <= 0

    def __hash__(self) -> int:
        return hash((self.id, self.side))

    def _eq__(self, other: Any) -> int:
        return (self.id, self.side) == (other.id, other.side)


Army: TypeAlias = list[Group]

Target: TypeAlias = tuple[Group, Group]


def parse_data(f: TextIO) -> tuple[str, str]:
    inmune, infection = f.read().split("\n\n")
    return inmune, infection


def parse_army(data: str, boost: int = 0) -> Army:
    pattern = re.compile(
        r"(?P<units>\d+) units each with (?P<hp>\d+) hit points "
        r"(?:\((?P<effects>.*)\) )?"
        r"with an attack that does (?P<atk_dmg>\d+) (?P<atk_type>\w+) "
        r"damage at initiative (?P<ini>\d+)"
    )

    def parse_effects(match_group: str | None) -> tuple[Set[str], Set[str]]:
        effects: dict[str, Set[str]] = {"weak": set(), "immune": set()}
        if match_group:
            for group in match_group.split("; "):
                k, v = group.split(" to ")
                effects[k] = set(v.split(", "))
        return effects["weak"], effects["immune"]

    def make_group(i: int, match: re.Match[str]) -> Group:
        return Group(
            i + 1,
            name,
            int(match.group("units")),
            int(match.group("hp")),
            int(match.group("atk_dmg")) + boost,
            match.group("atk_type"),
            int(match.group("ini")),
            *parse_effects(match.group("effects")),
        )

    name, *groups = data.splitlines()
    name = name.rstrip(":")

    return [make_group(i, m) for i, g in enumerate(groups) if (m := pattern.match(g))]


def _log_groups(immune_sys: Army, infection: Army) -> None:
    def show(side: str, groups: Army) -> None:
        logging.info(f"{side}:")
        if groups:
            for g in groups:
                logging.info(f"Group {g.id} contains {g.units} units")
        else:
            logging.info("No groups remain.")

    show("Immune System", immune_sys)
    show("Infection", infection)
    logging.info("")


def _log_targets(g: Group, enemies: Set[Group]) -> None:
    for e in sorted(enemies, key=lambda e: e.id):
        if (d := g.dmg(e)) > 0:
            logging.info(
                f"{g.side} group {g.id} would deal defending group {e.id} "
                f"{d} damage"
            )


def _log_attack(group: Group, target: Group, killed: int) -> None:
    logging.info(
        f"{group.side} group {group.id} attacks "
        f"defending group {target.id}, killing {killed} "
        f"unit{'' if killed == 1 else 's'}"
    )


def _select_targets(immune_sys: Army, infection: Army) -> list[Target]:
    verbose = logging.getLogger().isEnabledFor(logging.INFO)

    all_targets = []

    def select(army: Army, enemies: Sequence[Group]) -> list[Target]:
        targets = []
        untargeted = set(enemies)
        for group in sorted(army, key=lambda g: (g.power, g.ini), reverse=True):
            if not untargeted:
                break
            if verbose:
                _log_targets(group, untargeted)
            target = max(untargeted, key=lambda e: (group.dmg(e), e.power, e.ini))
            if group.dmg(target) > 0:
                targets.append((group, target))
                untargeted.remove(target)
        return targets

    all_targets += select(infection, immune_sys)
    all_targets += select(immune_sys, infection)

    logging.info("")

    return all_targets


def _attack_targets(
    immune_sys: Army, infection: Army, targets: Sequence[Target]
) -> int:
    verbose = logging.getLogger().isEnabledFor(logging.INFO)

    total_killed = 0

    for group, target in sorted(targets, key=lambda t: t[0].ini, reverse=True):
        if group.is_destroyed():
            # Group was destroyed by a previous attack
            continue
        killed = group.attack(target)
        total_killed += killed
        if verbose:
            _log_attack(group, target, killed)
        if target.is_destroyed():
            if target in immune_sys:
                immune_sys.remove(target)
            else:
                infection.remove(target)

    logging.info("")

    return total_killed


def battle(immune_sys: Army, infection: Army) -> tuple[bool | None, int]:
    if verbose := logging.getLogger().isEnabledFor(logging.INFO):
        _log_groups(immune_sys, infection)

    while immune_sys and infection:
        targets = _select_targets(immune_sys, infection)
        destroyed = _attack_targets(immune_sys, infection, targets)
        # Part 2 would loop forever without this check
        if destroyed == 0:
            return None, 0
        if verbose:
            logging.info("")
            _log_groups(immune_sys, infection)

    winner = max(immune_sys, infection, key=len)
    return bool(immune_sys), sum(g.units for g in winner)


def part1(data: tuple[str, str]) -> int:
    immune_sys = parse_army(data[0])
    infection = parse_army(data[1])
    _, units = battle(immune_sys, infection)
    return units


def part2(data: tuple[str, str]) -> int:
    for boost in count(1):
        immune_sys = parse_army(data[0], boost=boost)
        infection = parse_army(data[1])
        survived, units = battle(immune_sys, infection)
        if survived:
            return units
    assert False


def main() -> None:
    logging.config.fileConfig("../logging.conf")

    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
