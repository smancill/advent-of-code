#!/usr/bin/env python

from typing import TextIO

type Point = tuple[int, int]
type Area = dict[Point, int]
type Fold = tuple[int, int]


def parse_points(data: str) -> Area:
    def parse(ln: str) -> Point:
        x, y = map(int, ln.split(","))
        return (x, y)

    return {parse(ln): 1 for ln in data.splitlines()}


def parse_folds(data: str) -> list[Fold]:
    def parse(ln: str) -> Fold:
        *_, fold = ln.split()
        match fold.split("="):
            case "x", x:
                return (int(x), 0)
            case "y", y:
                return (0, int(y))
            case _:
                raise AssertionError

    return [parse(ln) for ln in data.splitlines()]


def parse_data(f: TextIO) -> tuple[Area, list[Fold]]:
    points, folds = f.read().split("\n\n")
    return parse_points(points), parse_folds(folds)


def view(area: Area) -> str:
    mx = max(x for x, _ in area)
    my = max(y for _, y in area)
    s = ""
    for y in range(my + 1):
        for x in range(mx + 1):
            s += "#" if area.get((x, y), 0) > 0 else "."
        s += "\n"
    return s


def fold(area: Area, folds: list[Fold]) -> Area:
    area = dict(area)
    for fold in folds:
        match fold:
            case fx, 0:
                for x, y in [(x, y) for x, y in area if x > fx]:
                    del area[x, y]
                    x = fx - (x - fx)
                    area[x, y] = 1
            case 0, fy:
                for x, y in [(x, y) for x, y in area if y > fy]:
                    del area[x, y]
                    y = fy - (y - fy)
                    area[x, y] = 1
    return area


def main() -> None:
    points, folds = parse_data(open(0))

    a1 = fold(points, folds[:1])
    a2 = fold(points, folds)

    print(f"P1: {len(a1)}")
    print(f"P2:\n{view(a2)}")


if __name__ == "__main__":
    main()
