#!/usr/bin/env python

T = {
    0: (1, 0),
    90: (0, 1),
    180: (-1, 0),
    270: (0, -1),
}

A = {
    'E': 0,
    'N': 90,
    'W': 180,
    'S': 270,
}

with open("input12.txt") as f:
    data = [(l[0], int(l[1:])) for l in f]


class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def rotate(self, angle):
        t = T[angle % 360]
        self.x, self.y = (
            self.x * t[0] - self.y * t[1],
            self.x * t[1] + self.y * t[0],
        )

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, factor):
        return Vector(factor * self.x, factor * self.y)

    def __str__(self):
        return f"({self.x}, {self.y})"


def to_vector(direction):
    return Vector(*T[A[direction]])


def part1():
    position = Vector(0, 0)
    direction = to_vector('E')

    for action, value in data:
        if action == 'R':
            direction.rotate(-value)
        elif action == 'L':
            direction.rotate(value)
        elif action == 'F':
            position += direction * value
        else:
            position += to_vector(action) * value

    return abs(position.x) + abs(position.y)


def part2():
    position = Vector(0, 0)
    waypoint = Vector(10, 1)

    for action, value in data:
        if action == 'R':
            waypoint.rotate(-value)
        elif action == 'L':
            waypoint.rotate(value)
        elif action == 'F':
            position += waypoint * value
        else:
            waypoint += to_vector(action) * value

    return abs(position.x) + abs(position.y)


print(f"P1: {part1()}")
print(f"P2: {part2()}")
