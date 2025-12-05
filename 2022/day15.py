#!/usr/bin/env python

import re
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from typing import NamedTuple, TextIO


class Coord(NamedTuple):
    x: int
    y: int


@dataclass(frozen=True)
class Sensor:
    position: Coord
    beacon: Coord

    @property
    def radius(self) -> int:
        return _dist(self.position, self.beacon)


@dataclass(frozen=True)
class Line:
    A: int
    B: int
    C: int


def parse_data(f: TextIO) -> list[Sensor]:
    def parse_pair(line: str) -> Sensor:
        groups = re.findall(r"x=(-?\d+), y=(-?\d+)", line)
        sensor, beacon = [Coord(int(x), int(y)) for x, y in groups]
        return Sensor(sensor, beacon)

    return [parse_pair(l) for l in f]


def _dist(a: Coord, b: Coord) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def _segment_at(sensor: Sensor, y: int) -> range | None:
    (sx, sy), r = sensor.position, sensor.radius
    if (dy := abs(sy - y)) <= r:
        dx = r - dy
        x0, x1 = sx - dx, sx + dx
        return range(x0, x1 + 1)
    return None


def _occupied_at(sensor: Sensor, y: int) -> list[int]:
    return [p.x for p in (sensor.position, sensor.beacon) if p.y == y]


def _merge_segments(segments: set[range]) -> set[range]:
    """Merge overlapping [x0, x1) segments."""
    merged = set()
    current, *rest = sorted(segments, key=lambda s: (s.start, s.stop))

    for segment in rest:
        if segment.start < current.stop:
            end = current.stop if segment.stop < current.stop else segment.stop
            current = range(current.start, end)
        else:
            merged.add(current)
            current = segment
    if current not in merged:
        merged.add(current)

    return merged


def _border(sensor: Sensor) -> tuple[list[Line], list[Line]]:
    (sx, sy), d = sensor.position, sensor.radius + 1

    # Coordinates:
    #           (sx, y0)
    #
    # (x0, sy)  (sx, sy)  (x1, sy)
    #
    #           (sx, y1)
    x0, x1 = sx - d, sx + d
    y0, y1 = sy - d, sy + d  # noqa: F841

    # Line (x₁, y₁) -> (x₂, y₂):
    #   Ax + By = C
    #
    # with:
    #   A: y₂ - y₁
    #   B: x₁ - x₂
    #   C: Ax₁ + By₁
    #
    # Normalize dividing all three coefficients by D.
    return (
        # with slope 1: (sx, y0) -> (x1, sy) and (x0, sy) -> (sx, y1)
        [Line(1, -1, (sx - y0)), Line(1, -1, (x0 - sy))],
        # with slope -1: (sx, y0) -> (x0, sy) and (x1, sy) -> (sx, y1)
        [Line(1, 1, (sx + y0)), Line(1, 1, (x1 + sy))],
    )


def _intersection(l1: Line, l2: Line) -> Coord | None:
    """Intersection between l1 (slope 1) and l2 (slope -1)"""
    # Intersection between two lines (in standard form):
    #   det = A₁B₂ - A₂B₁
    #   x = (B₂C₁ - B₁C₂) / det
    #   y = (A₁C₂ - A₂C₁) / det
    #
    # For L₁ (slope 1) and L₂ (slope -1):
    #   A₁, B₁ = 1, -1
    #   A₂, B₂ = 1, 1
    #   det = 2
    det = 2
    x = l1.C + l2.C
    y = l2.C - l1.C

    # coordinates must be integers
    if x % 2 == 1:
        return None
    if y % 2 == 1:
        return None
    x, y = x // det, y // det

    return Coord(x, y)


def _candidates(sensors: Sequence[Sensor]) -> Iterator[Coord]:
    borders = [_border(s) for s in sensors]
    lines1 = {l for g in borders for l in g[0]}
    lines2 = {l for g in borders for l in g[1]}

    return (c for l1 in lines1 for l2 in lines2 if (c := _intersection(l1, l2)))


# Optimized to avoid having a set with millions of values.
# Use a set of [x0, x1) segments instead of each indivitual x.
def part1(sensors: Sequence[Sensor], *, target: int = 2_000_000) -> int:
    # Collect scanned [x0, x1) segments at y=target
    segments = {s for sensor in sensors if (s := _segment_at(sensor, target))}
    occupied = {x for sensor in sensors for x in _occupied_at(sensor, target)}

    # Sum all merged [x0, x1) segments, minus the occupied positions
    return sum(len(s) for s in _merge_segments(segments)) - len(occupied)


# Heuristic: there is a single coordinate as solution, so it must
# exists just 1 unit outside the range of some of the sensors.
# For each sensor find the border next to its maximum range,
# and then find the solution by finding which border point is in the
# intersection of two sensors, and outside any sensor range.
def part2(sensors: Sequence[Sensor], *, limit: int = 4_000_000) -> int:
    def in_area(c: Coord) -> bool:
        return 0 <= c.x <= limit and 0 <= c.y <= limit

    def in_range(c: Coord) -> bool:
        return any(_dist(s.position, c) <= s.radius for s in sensors)

    c, *_ = [c for c in _candidates(sensors) if in_area(c) and not in_range(c)]

    return 4_000_000 * c.x + c.y


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
