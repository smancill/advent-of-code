#!/usr/bin/env python

import re
from collections.abc import Iterator
from functools import reduce
from math import prod
from typing import TextIO

type Properties = list[int]
type Ingredients = dict[str, Properties]
type Recipe = list[int]


def parse_data(f: TextIO) -> Ingredients:
    def parse_ingredient(line: str) -> tuple[str, Properties]:
        name, properties = line.split(": ")
        values = [int(p) for p in re.findall(r"-?\d+", properties)]
        return name, values

    return dict(parse_ingredient(l) for l in f)


def recipes(ingredients: int, total: int) -> Iterator[Recipe]:
    if ingredients == 1:
        yield [total]
        return

    for i in range(total + 1):
        for r in recipes(ingredients - 1, total - i):
            yield [i] + r


def cookie(ingredients: Ingredients, recipe: Recipe) -> Properties:
    def get_properties(i: Properties, t: int) -> Properties:
        return [p * t for p in i]

    def sum_properties(acc: Properties, arg: Properties) -> Properties:
        return [a + b for a, b in zip(acc, arg, strict=True)]

    measures = zip(ingredients.values(), recipe, strict=True)
    properties = [get_properties(i, t) for i, t in measures]
    cookie = reduce(sum_properties, properties)
    return [max(0, p) for p in cookie]


def score(cookie: Properties) -> int:
    return prod(cookie[:-1])


def part1(ingredients: Ingredients) -> int:
    cookies = (cookie(ingredients, t) for t in recipes(len(ingredients), 100))
    return max(score(c) for c in cookies)


def part2(ingredients: Ingredients) -> int:
    cookies = (cookie(ingredients, t) for t in recipes(len(ingredients), 100))
    return max(score(c) for c in cookies if c[-1] == 500)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
