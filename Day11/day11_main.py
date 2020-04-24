from collections import defaultdict
from typing import List

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from Intcode import Intcode
from my_tools import open_program, time_decorator


@time_decorator
def part1(comp: Intcode, program: List, inp: int):
    color_map = defaultdict(int, {(0, 0): 0})
    current_loc = [0, 0]
    heading = 0
    old_len = 0
    for _ in comp.new_program_gen(program, user_input=[inp]):
        if len(comp.program_output) != old_len and len(comp.program_output) % 2 == 0:
            color, turn = comp.program_output[-2:]
            color_map[tuple(current_loc)] = color
            heading = move_robot(current_loc, heading, turn)
            comp.user_input = iter([color_map[tuple(current_loc)]])
            old_len = len(comp.program_output)
    return color_map


def move_robot(current_loc: List, heading: int, turn: int) -> int:
    if turn == 0:
        new_heading = (heading - 1) % 4
    elif turn == 1:
        new_heading = (heading + 1) % 4
    else:
        raise ValueError("Wrong turn!")

    if new_heading == 0:
        current_loc[1] += 1
    elif new_heading == 1:
        current_loc[0] += 1
    elif new_heading == 2:
        current_loc[1] -= 1
    elif new_heading == 3:
        current_loc[0] -= 1
    else:
        raise ValueError("Wrong heading!")

    return new_heading


if __name__ == "__main__":
    day11_program = open_program("day11_input.txt")
    computer = Intcode()
    computer.suppress_output = True
    painted_hull = part1(computer, day11_program, 0)
    print("=" * 20 + " PART 1 " + "=" * 20)
    print(f"Panels painted at least once: {len(painted_hull.keys())}")

    painted_hull = part1(computer, day11_program, 1)
    print("=" * 20 + " PART 2 " + "=" * 20)
    print(f"Registration identifier:")
    coords = np.asarray(list(map(list, painted_hull.keys())))
    values = list(painted_hull.values())
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(coords[:, 0], coords[:, 1], values)
    plt.show()
