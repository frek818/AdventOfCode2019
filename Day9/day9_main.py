from typing import List

from Intcode import Intcode
from my_tools import open_program, time_decorator


@time_decorator
def part1(comp: Intcode, program: List):
    comp.new_program(program, user_input=[1])


@time_decorator
def part2(comp: Intcode, program: List):
    comp.new_program(program, user_input=[2])


if __name__ == "__main__":
    day9_program = open_program("day9_input.txt")
    computer = Intcode()
    computer.suppress_output = True
    part1(computer, day9_program)
    print("=" * 20 + " PART 1 " + "=" * 20)
    print(f"BOOST keycode: {computer.program_output[-1]}")

    part2(computer, day9_program)
    print("=" * 20 + " PART 2 " + "=" * 20)
    print(f"Distress signal coordinated: {computer.program_output[-1]}")
