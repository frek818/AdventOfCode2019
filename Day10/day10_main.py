from math import gcd

import numpy as np

from my_tools import time_decorator


@time_decorator
def part1(asteroid_field: np.ndarray) -> [np.ndarray, int]:
    best_location = asteroid_field[0]
    most_visible_asteroids = 0
    for asteroid in asteroid_field:
        relative_coords = asteroid_field - asteroid
        visible_asteroids = set()
        for i in relative_coords:
            if np.array_equal(i, [0, 0]):
                continue
            reduced_coords = tuple(i // gcd(*i))
            if reduced_coords not in visible_asteroids:
                visible_asteroids.add(reduced_coords)
        n_visible_asteroids = len(visible_asteroids)
        if n_visible_asteroids > most_visible_asteroids:
            best_location = asteroid
            most_visible_asteroids = n_visible_asteroids
    return best_location, most_visible_asteroids


@time_decorator
def part2(asteroid_field: np.ndarray, station_loc: np.ndarray) -> [np.ndarray]:
    relative_coords = asteroid_field - station_loc
    distance = np.sqrt(relative_coords[:, 0]*relative_coords[:, 0] + relative_coords[:, 1]*relative_coords[:, 1])
    field_mask = np.argsort(distance)
    relative_coords = relative_coords[field_mask]
    sorted_field = asteroid_field[field_mask]
    vaporized_asteroids = 0
    while relative_coords.shape[0] > 1:
        visible_asteroids = set()
        visible_asteroids_idx = []
        for i, asteroid in enumerate(relative_coords):
            if np.array_equal(asteroid, [0, 0]):
                continue
            reduced_coords = tuple(asteroid // gcd(*asteroid))
            if reduced_coords not in visible_asteroids:
                visible_asteroids.add(reduced_coords)
                visible_asteroids_idx.append(i)
        vap_after_rot = vaporized_asteroids + len(visible_asteroids)
        if vap_after_rot > 200:
            visible_asteroids_idx = np.array(visible_asteroids_idx)
            visible_asteroids = relative_coords[visible_asteroids_idx]
            asteroid_angles = np.rad2deg(np.arctan2(visible_asteroids[:, 1], visible_asteroids[:, 0]))
            asteroid_bearings = (180 - ((90 - asteroid_angles) % 360)) % 360
            mask = np.argsort(asteroid_bearings)
            about_to_be_vap = np.array(visible_asteroids_idx)[mask]
            return sorted_field[about_to_be_vap[199 - vaporized_asteroids]]
        relative_coords = np.delete(relative_coords, visible_asteroids_idx, axis=0)


if __name__ == "__main__":
    asteroid_coords = []
    with open("day10_input.txt") as f:
        for y, line in enumerate(f):
            asteroid_coords += [[x, y] for x, char in enumerate(line) if char == "#"]
        asteroid_coords = np.array(asteroid_coords)
    station_coords, detectable_asteroids = part1(asteroid_coords)
    print("=" * 20 + " PART 1 " + "=" * 20)
    print(f"Number of detectable asteroids: {detectable_asteroids}")
    print(f"Station location: {station_coords}")
    print("=" * 20 + " PART 2 " + "=" * 20)
    asteroid200 = part2(asteroid_coords, station_coords)
    print(f"200th vaporized asteroid at: {asteroid200}")
    print(f"Solution to puzzle: {asteroid200[0] * 100 + asteroid200[1]}")
