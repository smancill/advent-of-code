#!/usr/bin/env python

from collections import Counter
from dataclasses import dataclass, field
from typing import Self, TextIO


def parse_data(f: TextIO) -> list[str]:
    return [l.strip() for l in f.readlines()]


@dataclass
class Unbalanced:
    program: str
    unbalanced_weight: int
    fixed_weight: int


@dataclass
class Tower:
    root: str
    tower: dict[str, list[str]]
    weight: dict[str, int]
    total_weight: dict[str, int] = field(default_factory=dict)

    @classmethod
    def from_data(cls, data: list[str]) -> Self:
        tower = {}
        weight = {}
        for line in data:
            p, w, ch = cls._parse_program(line)
            tower[p] = ch
            weight[p] = w
        root = cls._find_root(tower)
        return cls(root, tower, weight)

    @staticmethod
    def _parse_program(info: str) -> tuple[str, int, list[str]]:
        tokens = info.split(" -> ")
        name, weight = tokens[0].split()
        weight = weight[1:-1]
        children = tokens[1].split(", ") if len(tokens) == 2 else []
        return (name, int(weight), children)

    @staticmethod
    def _find_root(tower: dict[str, list[str]]) -> str:
        # Find the program that is not a child of any other program.
        all_programs = set(tower.keys())
        all_children = {n for children in tower.values() for n in children}
        return next(iter(all_programs - all_children))

    def find_unbalanced(self) -> Unbalanced:
        self._calculate_weight(self.root)

        unb = self._find_unbalanced(self.root)
        assert unb is not None

        unb_p, unb_tw, exp_tw = unb
        unb_w = self.weight[unb_p]
        fixed_w = unb_w - (unb_tw - exp_tw)

        return Unbalanced(unb_p, unb_w, fixed_w)

    def _calculate_weight(self, prog: str) -> int:
        children_weight = sum(self._calculate_weight(ch) for ch in self.tower[prog])
        total_weight = self.weight[prog] + children_weight
        self.total_weight[prog] = total_weight
        return total_weight

    def _find_unbalanced(self, parent: str) -> tuple[str, int, int] | None:
        assert self.tower[parent]
        tw = {ch: self.total_weight[ch] for ch in self.tower[parent]}
        c = Counter(tw.values())

        # If all children are balanced, return to caller.
        # The parent is the program with unbalanced weight
        if len(c) == 1:
            return None

        # The right weight is the most common, only one child has unbalanced weight
        assert len(c) == 2
        (exp_w, _), (unb_w, _) = c.most_common()

        # Find the unbalanced child
        unb_p = next(p for p, w in tw.items() if w == unb_w)

        # Check if the child is unbalanced because of its own unbalanced child
        unb_s = self._find_unbalanced(unb_p)
        if unb_s is not None:
            return unb_s

        # Else, the child is the one with unbalanced weight
        return (unb_p, unb_w, exp_w)


def main() -> None:
    data = parse_data(open(0))

    tower = Tower.from_data(data)
    unbalanced = tower.find_unbalanced()

    print(f"P1: {tower.root}")
    print(f"P2: {unbalanced.fixed_weight}")


if __name__ == "__main__":
    main()
