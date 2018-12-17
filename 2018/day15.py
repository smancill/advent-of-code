#!/usr/bin/env python3

from itertools import count

verbose = False

with open("input15.txt") as f:
    data = [l.strip() for l in f]


class Unit:
    def __init__(self, side, pos, atk):
        self.side = side
        self.pos = pos
        self.atk = atk
        self.hp = 200
        self.enemy = 'G' if side == 'E' else 'E'

    def is_alive(self):
        return self.hp > 0

    def is_enemy(self, unit):
        return self.side != unit.side

    def __str__(self):
        return f"{self.side}({self.hp})"

    def __repr__(self):
        return f"{self.side}[{self.pos}, {self.hp}, {self.atk}]"


class Battle():

    def __init__(self, data, elf_atk=3):
        self.area = []
        self.units = []

        for i, l in enumerate(data):
            row = []
            for j, c in enumerate(l):
                if c == 'E' or c == 'G':
                    atk = elf_atk if c == 'E' else 3
                    self.units.append(Unit(c, (i, j), atk))
                row.append(c)
            self.area.append(row)

    def run(self, elves_win=False):
        for k in count():
            finished = False
            for u in sorted(self.units, key=lambda u: u.pos):
                if not u.is_alive():
                    continue
                e = self._enemies(u)
                if not e:
                    winner = u.side
                    rounds = k
                    finished = True
                    break
                self._move(u)
                a = self._attack(u, e)
                if elves_win and a and a.side == 'E' and not a.is_alive():
                    return None
            if verbose:
                print(f"{self}")
            if finished:
                break

        return winner, rounds, self._points(winner, rounds)

    def _move(self, unit):
        moves = self._bfs(unit)
        if moves:
            x, y = unit.pos
            nx, ny = moves[0][2]
            unit.pos = nx, ny
            self.area[x][y] = '.'
            self.area[nx][ny] = unit.side

    def _attack(self, unit, enemies):
        cand = self._in_range(*unit.pos)
        enemies = [e for e in enemies if e.pos in cand]
        if enemies:
            selected = min(enemies, key=lambda e: (e.hp, e.pos))
            selected.hp -= unit.atk
            if not selected.is_alive():
                x, y = selected.pos
                self.area[x][y] = '.'
            return selected
        return None

    def _bfs(self, unit):
        if self._near_enemies(*unit.pos, unit.enemy):
            return None

        def adj_pos(x, y):
            return [(i, j) for i, j in self._in_range(x, y)
                    if self.area[i][j] == '.']

        queue = [((i, j), (i, j)) for i, j in adj_pos(*unit.pos)]
        visited = {unit.pos}

        visit = True
        dist = 1
        moves = []

        while visit and queue:
            next_queue = []

            for pos in queue:
                if pos in visited:
                    continue
                visited.add(pos)

                x, y = pos[0]
                if self._near_enemies(x, y, unit.enemy):
                    moves.append((dist, pos[0], pos[1]))
                    visit = False
                    continue
                next_queue += [((i, j), pos[1]) for i, j in adj_pos(x, y)]

            queue = next_queue
            dist += 1

        return sorted(moves)

    def _enemies(self, unit):
        return [e for e in self.units if e.is_enemy(unit) and e.is_alive()]

    def _near_enemies(self, x, y, e):
        return any(self.area[i][j] == e for i, j in self._in_range(x, y))

    def _in_range(self, x, y):
        return [(x-1, y), (x, y-1), (x, y+1), (x+1, y)]

    def _points(self, winner, rounds):
        return rounds * sum(u.hp for u in self.units
                            if u.side == winner and u.is_alive())

    def __str__(self):
        def get_units(i, r):
            a = []
            for j, c in enumerate(r):
                if c == 'E' or c == 'G':
                    u = next(u for u in self.units if u.pos == (i, j))
                    a.append(f"{u}")
            return ", ".join(a)

        output = ''
        for i, r in enumerate(self.area):
            row_output = ''.join(r)
            row_units = get_units(i, r)
            if row_units:
                row_output += "  " + row_units
            output += row_output + '\n'
        return output


def part1():
    battle = Battle(data)
    if verbose:
        print(f"{battle}")
    return battle.run()


def part2():
    for atk in count(4):
        battle = Battle(data, elf_atk=atk)
        result = battle.run(elves_win=True)
        if result:
            return result


print(f"P1: {part1()[2]}")
print(f"P2: {part2()[2]}")
