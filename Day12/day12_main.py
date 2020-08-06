import itertools
from typing import List
import re

import numpy as np

from my_tools import time_decorator


class Moon:
    def __init__(self, x: int, y: int, z: int):
        self.position = np.array([x, y, z])
        self.velocity = np.zeros(3, dtype=int)

    def __repr__(self):
        return f"pos=<x={self.position[0]}, y={self.position[1]}, z={self.position[2]}> " \
               f"vel=<x={self.velocity[0]}, y={self.velocity[1]}, z={self.velocity[2]}>"

    def e_pot(self):
        return np.abs(self.position).sum()

    def e_kin(self):
        return np.abs(self.velocity).sum()

    def e_tot(self):
        return self.e_pot() * self.e_kin()

    def __gt__(self, other):
        return self.position > other.position

    def __lt__(self, other):
        return self.position < other.position

    def __eq__(self, other):
        return np.array_equal(self.position, other.position) and np.array_equal(self.velocity, other.velocity)


class Moon1d:
    def __init__(self, p: int):
        self.position = p
        self.velocity = 0

    def __repr__(self):
        return f"pos={self.position}\tvel={self.velocity}"

    def __gt__(self, other):
        return self.position > other.position

    def __lt__(self, other):
        return self.position < other.position

    def __eq__(self, other):
        return self.position == other.position and self.velocity == other.velocity


def apply_gravity(moons: List[Moon]):
    for m1, m2 in itertools.combinations(moons, 2):
        mask1 = m1 < m2
        mask2 = m1 > m2
        m1.velocity[mask1] += 1
        m1.velocity[mask2] -= 1

        m2.velocity[~mask1] += 1
        m2.velocity[~mask2] -= 1


def apply_gravity1d(moons: List[Moon1d]):
    for m1, m2 in itertools.combinations(moons, 2):
        if m1 < m2:
            m1.velocity += 1
            m2.velocity -= 1
        elif m1 > m2:
            m1.velocity -= 1
            m2.velocity += 1


def apply_velocity(moons: List[Moon]):
    for m in moons:
        m.position += m.velocity


def scan(filename: str):
    with open(filename) as f:
        coords = []
        for line in f:
            coords.append(np.array(re.findall(r"[-0-9]+", line), dtype=int))
    return coords


def simulate(moons: List[Moon], steps: int):
    for i in range(steps):
        apply_gravity(moons)
        apply_velocity(moons)


def simulate1d(moons: List[Moon1d]):
    apply_gravity1d(moons)
    apply_velocity(moons)


@time_decorator
def day12_part1(moons: List[Moon]):
    simulate(moons, 1000)
    sys_e = 0
    for m in moons:
        sys_e += m.e_tot()
    return sys_e


@time_decorator
def day12_part2(m_pos: List[List]):
    moons = np.array(m_pos)
    repeat_steps = []
    for dim in moons.T:
        moons_1d = [Moon1d(pos) for pos in dim]
        moons_1d_init = [Moon1d(pos) for pos in dim]
        simulate1d(moons_1d)
        ctr = 1
        while not all([m1 == m2 for m1, m2 in zip(moons_1d, moons_1d_init)]):
            simulate1d(moons_1d)
            ctr += 1
        repeat_steps.append(ctr)
    lcm = np.lcm.reduce(repeat_steps)
    return lcm


if __name__ == "__main__":
    coords = scan("day12_input.txt")
    ms = [Moon(*coord) for coord in coords]
    system_energy = day12_part1(ms)
    print("=" * 20 + " PART 1 " + "=" * 20)
    print(f"Total system energy: {system_energy}")
    system_repeat = day12_part2(coords)
    print("=" * 20 + " PART 2 " + "=" * 20)
    print(f"System state will repeat in {system_repeat} steps")
