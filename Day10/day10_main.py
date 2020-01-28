from math import gcd

import numpy as np

from my_tools import time_decorator


@time_decorator
def part1(asteroid_field: np.ndarray) -> [np.ndarray, int]:
    best_location = asteroid_coords[0]
    most_visible_asteroids = 0
    for asteroid in asteroid_field:
        relative_coords = asteroid_coords - asteroid
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


if __name__ == "__main__":
    asteroid_coords = []
    with open("day10_input.txt") as f:
        for y, line in enumerate(f):
            asteroid_coords += [[x, y] for x, char in enumerate(line) if char == "#"]
        asteroid_coords = np.array(asteroid_coords)
    station_coords, detectable_asteroids = part1(asteroid_coords)
    print("=" * 20 + " PART 1 " + "=" * 20)
    print(f"Number of detectable asteroids: {detectable_asteroids}")
