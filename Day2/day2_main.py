from itertools import product

from Intcode import Intcode
from my_tools import time_decorator


@time_decorator
def day2_part1(comp, inp):
    print("="*20 + " PART 1 " + "="*20)
    initial_state = inp[:]
    initial_state[1] = 12
    initial_state[2] = 2
    comp.new_program(initial_state)
    print(f"Value at position 0 after execution: {comp.program_input[0]}")


@time_decorator
def day2_part2(comp, inp):
    print("=" * 20 + " PART 2 " + "=" * 20)
    original_state = inp[:]
    for noun, verb in product(range(100), repeat=2):
        initial_state = original_state[:]
        initial_state[1] = noun
        initial_state[2] = verb
        comp.new_program(initial_state)
        if comp.program_input[0] == 19690720:
            break
    print(f"Noun = {noun}\tVerb = {verb}")
    print(f"Solution: Noun * 100 + Verb = {100 * noun + verb}")


if __name__ == "__main__":
    with open("day2_input.csv") as f:
        program_input = list(map(int, next(f).split(',')))
    computer = Intcode()
    day2_part1(computer, program_input)
    day2_part2(computer, program_input)
