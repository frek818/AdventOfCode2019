from typing import List

import numpy as np
from matplotlib import pyplot as plt

from my_tools import time_decorator


def read_instruction(command: str) -> List[int]:
    coord = [0, 0]
    direction = command[0]
    distance = int(command[1:])
    if direction == "R":
        coord[0] += distance
    elif direction == "L":
        coord[0] -= distance
    elif direction == "U":
        coord[1] += distance
    elif direction == "D":
        coord[1] -= distance
    else:
        raise ValueError("Unknown direction!")
    return coord


def calc_turns(instruction: List[str]) -> List[List[int]]:
    current_coord = [0, 0]
    path = [current_coord[:]]
    for command in instruction:
        x_step, y_step = read_instruction(command)
        current_coord[0] += x_step
        current_coord[1] += y_step
        path.append(current_coord[:])
    return path


def calc_grid_path(instr: List[str]) -> List[List[int]]:
    current_coord = [0, 0]
    grid_path = []
    for command in instr:
        x_step, y_step = read_instruction(command)
        new_coord = [current_coord[0] + x_step, current_coord[1] + y_step]
        if x_step == 0:
            grid_path += [(current_coord[0], y) for y in range(current_coord[1] + 1, new_coord[1] + 1)]
        else:
            grid_path += [(x, current_coord[1]) for x in range(current_coord[0] + 1, new_coord[0] + 1)]
        current_coord = new_coord[:]
    return grid_path


@time_decorator
def day3_part1(instr: List[List[str]], *,  show_wires: bool = True) -> np.ndarray:
    if show_wires:
        wires = []
        for i in instr:
            wires.append(calc_turns(i))
        wires = np.asarray(wires, dtype=int)
        plt.figure("Jumble of wires")
        plt.plot(wires[0][:, 0], wires[0][:, 1], color="k")
        plt.plot(wires[1][:, 0], wires[1][:, 1], color="r")
        plt.show()
    wires = []
    for i in instr:
        wires.append(set(calc_grid_path(i)))  # Ignore self crossings
    intersections = list(set.intersection(*wires))
    manhattan_dists = np.sum(np.abs(np.asarray(intersections)), axis=1)
    return min(manhattan_dists)


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        instructions = []
        for line in f:
            instructions.append(line.split(","))
    print(f"{'=' * 20} PART 1 {'=' * 20}")
    closest_intersection = day3_part1(instructions, show_wires=False)
    print(f"Manhattan distance of closest intersection = {closest_intersection}")
