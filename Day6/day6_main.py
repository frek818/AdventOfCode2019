from typing import Dict

from my_tools import time_decorator


@time_decorator
def map_all_orbits(filename: str) -> Dict:
    with open(filename, "r") as f:
        orbit_map = dict()
        for line in f:
            orbit_center, orbiting_obj = line.strip("\n").split(")")
            if orbiting_obj not in orbit_map:
                orbit_map[orbiting_obj] = orbit_center
    return orbit_map


def orbit_chain(orbit_map: Dict, start_obj: str, end_obj: str = "COM"):
    next_obj = start_obj
    chain = [start_obj]
    while next_obj != end_obj:
        next_obj = orbit_map[next_obj]
        chain.append(next_obj)
    return chain


@time_decorator
def part1(orbit_map: Dict):
    orbit_ctr = 0
    for obj in orbit_map.keys():
        next_obj = orbit_map[obj]
        orbit_ctr += 1
        while next_obj != "COM":
            next_obj = orbit_map[next_obj]
            orbit_ctr += 1
    print("=" * 20 + " PART 1 " + "=" * 20)
    print(f"Total number of direct and indirect orbits: {orbit_ctr}")


@time_decorator
def part2(orbit_map: Dict):
    my_orbits = orbit_chain(orbit_map, "YOU")
    santa_orbits = orbit_chain(orbit_map, "SAN")
    common_obj = set(my_orbits).intersection(set(santa_orbits))
    for obj in my_orbits:
        if obj in common_obj:
            break
    transfers_required = len(my_orbits[:my_orbits.index(obj)]) + len(santa_orbits[:santa_orbits.index(obj)]) - 2
    print("=" * 20 + " PART 2 " + "=" * 20)
    print(f"Total number of direct and indirect orbits: {transfers_required}")


if __name__ == "__main__":
    orb_map = map_all_orbits("day6_input.txt")
    part1(orb_map)
    part2(orb_map)
