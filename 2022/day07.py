#!/usr/bin/env python

from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Final, Self, TextIO

TOTAL_SIZE: Final = 70_000_000
UPDATE_SIZE: Final = 30_000_000


@dataclass
class File:
    name: str
    size: int


@dataclass()
class Directory:
    name: str
    parent: Self | None
    children: list[Self | File] = field(default_factory=list, init=False)


def parse_data(f: TextIO) -> Directory:
    root = Directory("/", None)
    current = root

    def parse_cd(current: Directory, target: str) -> Directory:
        match target:
            case "/":
                return root
            case "..":
                if current == root:
                    raise ValueError(f"$ cd .. ({current=})")
                if current.parent is not None:
                    return current.parent
                else:
                    raise ValueError(f"$ cd .. ({current=})")
            case _:
                for node in current.children:
                    if isinstance(node, Directory) and node.name == target:
                        return node
                raise ValueError(f"$ cd {target}")

    def parse_ls(current: Directory) -> list[Directory | File]:
        children: list[Directory | File] = []
        while queue:
            line = queue[0]
            match line.split():
                case ["dir", name]:
                    children.append(Directory(name, current))
                case [size, name]:
                    children.append(File(name, int(size)))
                case ["$", *_]:
                    break
                case _:
                    raise ValueError(line)
            queue.popleft()
        return children

    queue = deque(f.readlines())
    while queue:
        line = queue.popleft()
        match line.split():
            case ["$", *cmd]:
                match cmd:
                    case ["cd", target]:
                        current = parse_cd(current, target)
                    case ["ls"]:
                        current.children = parse_ls(current)
                    case _:
                        raise ValueError(line)
            case _:
                raise ValueError(line)

    return root


def list_directory(directory: Directory, indent: str = "") -> None:
    print(f"{indent}- {directory.name} (dir)")
    indent += "  "
    for child in directory.children:
        match child:
            case File(name, size):
                print(f"{indent}- {name} (file, {size=})")
            case Directory():
                list_directory(child, indent)


def find_directories(root: Directory) -> Iterator[Directory]:
    yield root
    for child in root.children:
        if isinstance(child, Directory):
            yield from find_directories(child)


def find_size(root: Directory) -> int:
    total = 0
    for child in root.children:
        match child:
            case Directory():
                total += find_size(child)
            case File(size=size):
                total += size
    return total


def part1(root: Directory) -> int:
    return sum(s for d in find_directories(root) if (s := find_size(d)) <= 100_000)


def part2(root: Directory) -> int:
    free_space = TOTAL_SIZE - find_size(root)
    must_free = UPDATE_SIZE - free_space

    candidates = [
        (d, s) for d in find_directories(root) if (s := find_size(d)) >= must_free
    ]
    selected = min(candidates, key=lambda t: t[1])
    return selected[1]


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
