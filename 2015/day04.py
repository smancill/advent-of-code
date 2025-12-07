#!/usr/bin/env python

import hashlib
from concurrent import futures
from typing import TextIO


def parse_data(f: TextIO) -> str:
    return f.read().rstrip()


def _find_number_in_range(key: str, zeros: int, numbers: range) -> int | None:
    prefix = "0" * zeros
    for i in numbers:
        combined = key + str(i)
        hash = hashlib.md5(combined.encode())
        digest = hash.hexdigest()
        if digest.startswith(prefix):
            return i
    return None


def _find_number(key: str, zeros: int, limit: int) -> int:
    # Speed up using multiple processes
    processes = 8
    with futures.ProcessPoolExecutor(max_workers=processes) as executor:
        tasks = []
        for i in range(processes):
            r = range(1 + i, limit + 1, processes)
            t = executor.submit(_find_number_in_range, key, zeros, r)
            tasks.append(t)
    results = [n for t in tasks if (n := t.result()) is not None]
    return min(results, default=0)


def part1(data: str) -> int:
    # limit chosen manually
    return _find_number(data, zeros=5, limit=2_000_000)


def part2(data: str) -> int:
    # limit chosen manually
    return _find_number(data, zeros=6, limit=10_000_000)


def main() -> None:
    data = parse_data(open(0))

    print(f"P1: {part1(data)}")
    print(f"P2: {part2(data)}")


if __name__ == "__main__":
    main()
