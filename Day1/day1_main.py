import numpy as np

from my_tools import time_decorator


def get_fuel_required(module_mass: int) -> int:
    fuel = module_mass // 3 - 2
    if fuel <= 0:
        fuel = 0
    return fuel


@time_decorator
def get_fuel_map(mass_vec: list) -> int:
    return sum(map(get_fuel_required, mass_vec))


# Too slow
def get_fuel_recursive(mass: int) -> int:
    fuel = get_fuel_required(mass)
    tot_module_fuel = 0
    while fuel >= 0:
        tot_module_fuel += fuel
        fuel = get_fuel_required(fuel)
    return tot_module_fuel


def get_fuel_vector(mass_vec: np.ndarray) -> np.ndarray:
    fuel_vec = mass_vec // 3 - 2
    fuel_vec = fuel_vec[fuel_vec > 0]
    return fuel_vec


@time_decorator
def get_fuel_vector_recursive(mass_vec: np.ndarray) -> int:
    tot_fuel = 0
    fuel_vec = get_fuel_vector(mass_vec)
    while len(fuel_vec) != 0:
        tot_fuel += sum(fuel_vec)
        fuel_vec = get_fuel_vector(fuel_vec)
    return tot_fuel


if __name__ == "__main__":
    masses = []
    with open("day1_input.txt", "r") as f:
        for mass in f:
            masses.append(int(mass))

    # ============== PART 1 ================
    tot_fuel_p1 = get_fuel_map(masses)
    masses = np.asarray(masses)
    tot_fuel_p1 = sum(get_fuel_vector(masses))
    print(f"Part 1:\nFuel required = {tot_fuel_p1} kg")

    # ============== PART 2 ================
    tot_fuel_p2 = get_fuel_vector_recursive(masses)
    print(f"Part 2:\nFuel required = {tot_fuel_p2} kg")
