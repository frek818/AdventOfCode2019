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


class System:
    def __init__(self, coords: List[List]):
        self.position = np.array(coords, dtype=int)
        self.velocity = np.zeros(self.position.shape, dtype=int)

    def __repr__(self):
        return f"pos={self.position}\nvel={self.velocity}"

    def e_pot(self):
        return np.abs(self.position).sum(axis=1)

    def e_kin(self):
        return np.abs(self.velocity).sum(axis=1)

    def e_tot(self):
        return sum(self.e_pot() * self.e_kin())

    def __gt__(self, other):
        return self.position > other.position

    def __lt__(self, other):
        return self.position < other.position

    def __eq__(self, other):
        return np.array_equal(self.position, other.position) and np.array_equal(self.velocity, other.velocity)


def apply_gravity_moon(moons: List[Moon]):
    for m1, m2 in itertools.combinations(moons, 2):
        mask1 = m1 < m2
        mask2 = m1 > m2
        m1.velocity[mask1] += 1
        m1.velocity[mask2] -= 1

        m2.velocity[~mask1] += 1
        m2.velocity[mask2] -= 1


def apply_gravity(sys: System):
    for m1, m2 in itertools.combinations(range(4), 2):
        mask1 = sys.position[m1] < sys.position[m2]
        mask2 = sys.position[m1] > sys.position[m2]
        sys.velocity[m1][mask1] += 1
        sys.velocity[m1][mask2] -= 1

        sys.velocity[m2][~mask1] += 1
        sys.velocity[m2][~mask2] -= 1


def apply_velocity_moon(moons: List[Moon]):
    for m in moons:
        m.position += m.velocity


def apply_velocity(sys: System):
    sys.position += sys.velocity


def scan(filename: str):
    with open(filename) as f:
        coords = []
        for line in f:
            coords.append(np.array(re.findall(r"[-0-9]+", line), dtype=int))
    return coords


def simulate_moon(moons: List[Moon], steps: int):
    for i in range(steps):
        apply_gravity_moon(moons)
        apply_velocity_moon(moons)


def simulate(moons: System, steps: int):
    for i in range(steps):
        apply_gravity(moons)
        apply_velocity(moons)


@time_decorator
def day12_part1(moons: List[Moon]):
    simulate_moon(moons, 1000)
    sys_e = 0
    for m in moons:
        sys_e += m.e_tot()
    return sys_e


@time_decorator
def day12_part2(moons: System):
    simulate(moons, 1000)
    sys_e = moons.e_tot()
    return sys_e


if __name__ == "__main__":
    ms_moon = np.array([Moon(*coords) for coords in scan("day12_input.txt")])
    ms = System(scan("day12_input.txt"))
    system_energy = day12_part1(ms_moon)
    system_energy = day12_part2(ms)
    print("=" * 20 + " PART 1 " + "=" * 20)
    print(f"Total system energy: {system_energy}")
