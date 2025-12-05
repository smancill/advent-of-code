#!/usr/bin/env python

import itertools
import re
import sys
from collections import deque
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from typing import Final, TextIO, TypeAlias

Name: TypeAlias = str
Path: TypeAlias = list[Name]


@dataclass(frozen=True)
class Valve:
    rate: int
    tunnels: list[Name]


def parse_data(f: TextIO) -> dict[Name, Valve]:
    def parse_valve(line: str) -> tuple[Name, Valve]:
        match = re.match(
            r"Valve (?P<name>\w+) .* rate=(?P<rate>\d+); .* valves? (?P<valves>.*)$",
            line,
        )
        if match:
            name = match.group("name")
            rate = int(match.group("rate"))
            tunnels = match.group("valves").split(", ")
            return name, Valve(rate, tunnels)
        raise ValueError(line)

    return dict(parse_valve(l) for l in f.read().splitlines())


class PathFinder:
    _valves: Final[dict[Name, Valve]]
    _dist: Final[dict[Name, dict[Name, int]]]
    _working: Final[set[Name]]
    _start: Final[Name]

    def __init__(self, valves: Mapping[Name, Valve], start: Name):
        self._valves = dict(valves)
        self._dist = self._min_dist(valves)
        self._working = {v for v in self._dist if self._valves[v].rate > 0}
        self._start = start

    @staticmethod
    def _min_dist(valves: Mapping[Name, Valve]) -> dict[Name, dict[Name, int]]:
        # https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
        dist = {u: {v: sys.maxsize for v in valves} for u in valves}
        for u in dist:
            for v in valves[u].tunnels:
                dist[u][v] = 1
        for v in dist:
            dist[v][v] = 0
        for k in dist:
            for i in dist:
                for j in dist:
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
        return dist

    def best_path(self, max_time: int, travelers: int) -> tuple[Path | list[Path], int]:
        def all_paths(intermediate: bool) -> Iterator[tuple[Path, int]]:
            return (
                (path, self._pressure(path, max_time))
                for path in self._traverse(max_time, intermediate=intermediate)
            )

        match travelers:
            case 1:
                path, pressure = max(all_paths(False), key=lambda t: t[1])
                return path, pressure
            case 2:
                # Simplest solution: generate all possible paths to open valves
                # (including intermediate paths instead of just "completed"
                # paths), then find the pair of non-intersecting paths with the
                # best combined pressure.
                #
                # Optimization to reduce the search space: to avoid checking
                # O(n²) pairs, sort the paths by descending pressure first, and
                # discard all pairs whose combined pressure could never be
                # larger than the current max_pressure.
                best_path, max_pressure = [], 0
                ordered = sorted(all_paths(True), key=lambda t: t[1], reverse=True)
                for i, (path1, p1) in enumerate(ordered):
                    for path2, p2 in itertools.islice(ordered, i + 1):
                        pressure = p1 + p2
                        if pressure < max_pressure:
                            break
                        if set(path1) & set(path2):
                            continue
                        best_path = [path1, path2]
                        max_pressure = pressure
                return best_path, max_pressure
            case _:
                raise ValueError(f"invalid {travelers=}")

    def _traverse(self, max_time: int, intermediate: bool) -> Iterator[Path]:
        type State = tuple[int, Name, Path]

        queue: deque[State] = deque()
        queue.append((0, self._start, []))

        while queue:
            time, current, visited = queue.popleft()
            moved = False
            for closed in self._working - set(visited):
                open_time = time + self._time(current, closed)
                if open_time < max_time:
                    queue.append((open_time, closed, visited + [closed]))
                    moved = True
            if intermediate or not moved:
                yield visited

    def _pressure(self, path: Path, time: int) -> int:
        current = self._start
        pressure = 0
        for node in path:
            time -= self._time(current, node)
            pressure += time * self._valves[node].rate
            current = node
        return pressure

    def _time(self, u: Name, v: Name) -> int:
        return self._dist[u][v] + 1

    def __str__(self) -> str:
        header = "  " + "".join(f"{i:>4s}" for i in self._dist)
        columns = [
            f"{i:<2s}" + "".join(f"{self._dist[i][j]:>4d}" for j in self._dist)
            for i in self._dist
        ]
        return "\n".join([header] + columns)


def part1(data: Mapping[Name, Valve]) -> int:
    path_finder = PathFinder(data, "AA")
    _, pressure = path_finder.best_path(max_time=30, travelers=1)
    return pressure


def part2(data: Mapping[Name, Valve]) -> int:
    path_finder = PathFinder(data, "AA")
    _, pressure = path_finder.best_path(max_time=26, travelers=2)
    return pressure


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
