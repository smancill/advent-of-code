#!/usr/bin/env python

from collections import defaultdict
from typing import TextIO

type Graph = dict[int, set[int]]
type Group = frozenset[int]


def parse_data(f: TextIO) -> Graph:
    graph = defaultdict(set)
    for l in f:
        t = l.split(" <-> ")
        n = int(t[0])
        for i in map(int, t[1].split(",")):
            graph[n].add(i)
            graph[i].add(n)
    return graph


def find_group(graph: Graph, root: int) -> Group:
    group = set()
    queue = {root}
    while queue:
        n = queue.pop()
        group.add(n)
        queue.update(graph[n] - group)
    return frozenset(group)


def find_groups(graph: Graph) -> set[Group]:
    groups = set()
    queue = set(graph.keys())
    while queue:
        root = queue.pop()
        group = find_group(graph, root)
        queue -= group
        groups.add(group)
    return groups


def part1(data: Graph) -> int:
    return len(find_group(data, 0))


def part2(data: Graph) -> int:
    return len(find_groups(data))


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
