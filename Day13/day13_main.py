from typing import List

import numpy as np

from Intcode import Intcode
from my_tools import open_program, time_decorator


@time_decorator
def day13_part1(comp: Intcode, program: List):
    comp.new_program(program)
    screen = np.array(comp.program_output).reshape((len(comp.program_output) // 3, 3))
    n_block_tiles = np.count_nonzero(screen[:, 2] == 2)
    return n_block_tiles


if __name__ == "__main__":
    day13_program = open_program("day13_input.txt")
    computer = Intcode()
    computer.suppress_output = True
    block_tiles = day13_part1(computer, day13_program)
    print("=" * 20 + " PART 1 " + "=" * 20)
    print(f"Number of block tiles: {block_tiles}")
