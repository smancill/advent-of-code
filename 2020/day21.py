#!/usr/bin/env python

import re
from collections.abc import Sequence
from typing import TextIO

type Ingredients = set[str]
type Allergens = set[str]
type Food = tuple[Ingredients, Allergens]


def parse_data(f: TextIO) -> list[Food]:
    def parse_food(line: str) -> Food:
        if match := re.fullmatch(r"(.*) \(contains (.*)\)\n", line):
            ingredients, allergens = match.groups()
            return set(ingredients.split()), set(allergens.split(", "))
        raise ValueError(line)

    return [parse_food(l) for l in f]


def find_allergic_ingredients(foods: Sequence[Food]) -> dict[str, str]:
    def known_allergens() -> Allergens:
        return set.union(*(fa for _, fa in foods))

    def may_contain_allergen(allergen: str) -> Ingredients:
        return set.intersection(*(fi for fi, fa in foods if allergen in fa))

    allergic = {}
    candidates = [(a, may_contain_allergen(a)) for a in known_allergens()]

    while candidates:
        allergen, ingredients = candidates.pop(0)
        if len(ingredients) == 1:
            ingredient = ingredients.pop()
            allergic[ingredient] = allergen
        else:
            ingredients -= set(allergic)
            candidates.append((allergen, ingredients))

    return dict(sorted(allergic.items(), key=lambda t: t[1]))


def part1(foods: Sequence[Food]) -> int:
    allergic = set(find_allergic_ingredients(foods))
    return sum(len(ingredients - allergic) for ingredients, _ in foods)


def part2(foods: Sequence[Food]) -> str:
    allergic = find_allergic_ingredients(foods)
    allergic = dict(sorted(allergic.items(), key=lambda t: t[1]))
    return ",".join(allergic)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
