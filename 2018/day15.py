#!/usr/bin/env python

import logging
import logging.config
from collections.abc import Sequence
from dataclasses import dataclass
from io import StringIO
from itertools import count
from typing import Final, Self, TextIO, TypeAlias

Position: TypeAlias = tuple[int, int]
Move: TypeAlias = tuple[Position, Position]


def read_data(f: TextIO) -> list[str]:
    return [l.rstrip() for l in f]


class Unit:
    side: Final[str]
    enemy: Final[str]
    atk: Final[int]
    _hp: int
    _pos: Position

    ELF: Final = "E"
    GOBLIN: Final = "G"

    def __init__(self, side: str, pos: Position, atk: int):
        self.side = side
        self.enemy = Unit.GOBLIN if side == Unit.ELF else Unit.ELF
        self.atk = atk
        self._hp = 200
        self._pos = pos

    @property
    def pos(self) -> Position:
        return self._pos

    @property
    def hp(self) -> int:
        return self._hp

    def move(self, pos: Position) -> None:
        self._pos = pos

    def is_alive(self) -> bool:
        return self._hp > 0

    def attack(self, enemy: Self) -> None:
        enemy._hp -= self.atk

    def __str__(self) -> str:
        return f"{self.side}({self._hp})"


@dataclass(frozen=True)
class Status:
    alive: int
    killed: int


@dataclass(frozen=True)
class Winner:
    side: str
    atk: int
    rounds: int
    points: int
    killed: int


class Battle:
    _area: Final[dict[Position, str]]
    _units: Final[list[Unit]]
    _killed: Final[dict[str, int]]

    DEFAULT_ATK: Final = 3

    WALL: Final = "#"
    CAVERN: Final = "."

    ENEMY: Final = {Unit.ELF: Unit.GOBLIN, Unit.GOBLIN: Unit.ELF}

    def __init__(self, data: Sequence[str], elf_atk: int = DEFAULT_ATK):
        self._area = {}
        self._units = []
        self._killed = {Unit.ELF: 0, Unit.GOBLIN: 0}

        for i, l in enumerate(data):
            for j, c in enumerate(l):
                p = (i, j)
                if self._is_unit(c):
                    atk = elf_atk if c == Unit.ELF else self.DEFAULT_ATK
                    self._units.append(Unit(c, p, atk))
                self._area[p] = c

    def run(self) -> Winner:
        def round() -> str | None:
            for unit in sorted(self._units, key=lambda u: u.pos):
                # Unit could have been killed by a previous attack in this round
                if not unit.is_alive():
                    continue
                # Side wins if there are no remaining enemies
                enemies = self._enemies(unit)
                if not enemies:
                    return unit.side
                # Optionally move before attacking
                self._move(unit, enemies)
                # Attack target in range, if any
                self._attack(unit, enemies)
            return None

        if debug := logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("Initially:")
            logging.debug(f"{self}")

        for k in count(1):
            winner = round()
            if debug:
                logging.debug(f"After {k} rounds:" if winner is None else "Last round:")
                logging.debug(f"{self}")
            if winner is not None:
                return self._winner(winner, k - 1)

        raise AssertionError

    def _move(self, unit: Unit, enemies: Sequence[Unit]) -> None:
        if self._has_enemies_in_range(unit):
            return
        if moves := self._bfs(unit.pos, enemies):
            _, start = moves[0]
            self._area[unit.pos] = self.CAVERN
            unit.move(start)
            self._area[unit.pos] = unit.side

    def _attack(self, unit: Unit, enemies: Sequence[Unit]) -> None:
        if targets := self._enemies_in_range(unit, enemies):
            selected = min(targets, key=lambda e: (e.hp, e.pos))
            unit.attack(selected)
            if not selected.is_alive():
                self._area[selected.pos] = self.CAVERN
                self._killed[selected.side] += 1

    def _bfs(self, orig: Position, enemies: Sequence[Unit]) -> list[Move]:
        def adj(pos: Position) -> list[Position]:
            return [p for p in self._in_range(pos) if self._area[p] == self.CAVERN]

        goals = {p for e in enemies for p in adj(e.pos)}
        moves = []

        # Start by moving to all adjacent positions, at distance 1
        queue = [(p, p) for p in adj(orig)]
        visited = {orig}

        found = False
        while queue:
            next_queue: list[Move] = []
            # Check all moves of distance d
            for target, start in queue:
                if target in visited:
                    continue
                visited.add(target)
                # if there is an enemy in range, distance d is the minimal distance
                if target in goals:
                    moves.append((target, start))
                    found = True
                    continue
                # Add moves of distance d + 1
                next_queue.extend((p, start) for p in adj(target))
            if found:
                break
            # Replace moves of distance d with moves of distance d + 1
            queue = next_queue

        # Return moves with minimal distance, sorted by end position
        return sorted(moves)

    def _winner(self, winner: str, rounds: int) -> Winner:
        atk = next(u.atk for u in self._units if u.side == winner)
        total_hp = sum(u.hp for u in self._units if u.side == winner and u.is_alive())
        points = total_hp * rounds
        return Winner(winner, atk, rounds, points, self._killed[winner])

    def _enemies(self, unit: Unit) -> list[Unit]:
        return [u for u in self._units if u.side == unit.enemy and u.is_alive()]

    def _enemies_in_range(self, unit: Unit, enemies: Sequence[Unit]) -> list[Unit]:
        near_positions = self._in_range(unit.pos)
        return [e for e in enemies if e.pos in near_positions]

    def _has_enemies_in_range(self, unit: Unit) -> bool:
        return any(self._area[pos] == unit.enemy for pos in self._in_range(unit.pos))

    @staticmethod
    def _in_range(pos: Position) -> tuple[Position, ...]:
        y, x = pos
        return ((y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x))

    @staticmethod
    def _is_unit(c: str) -> bool:
        return c == Unit.ELF or c == Unit.GOBLIN

    def __str__(self) -> str:
        def find_unit(pos: Position) -> Unit:
            return next(u for u in self._units if u.pos == pos and u.is_alive())

        n, m = max(self._area)
        buf = StringIO()
        for i in range(n + 1):
            row = [((p := (i, j)), self._area[p]) for j in range(m + 1)]
            buf.write("".join(c for _, c in row))
            if units := [find_unit(p) for p, c in row if self._is_unit(c)]:
                buf.write("   ")
                buf.write(", ".join(str(u) for u in units))
            buf.write("\n")
        return buf.getvalue()


def part1(data: Sequence[str]) -> Winner:
    battle = Battle(data)
    result = battle.run()
    if logging.getLogger().isEnabledFor(logging.INFO):
        logging.info(f"{battle}")
    return result


def part2(data: Sequence[str]) -> Winner:
    for atk in count(4):
        battle = Battle(data, elf_atk=atk)
        result = battle.run()
        if result.side == Unit.ELF and result.killed == 0:
            if logging.getLogger().isEnabledFor(logging.INFO):
                logging.info(f"{battle}")
            return result
    raise AssertionError


def main() -> None:
    logging.config.fileConfig("../logging.conf")

    data = read_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
