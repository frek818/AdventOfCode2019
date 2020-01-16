from itertools import permutations

from Intcode import Intcode
from my_tools import open_program, time_decorator


@time_decorator
def part1(comp, program):
    max_thruster_signal = 0
    for sequence in permutations(range(5), 5):
        input_signal = 0
        for phase_setting in sequence:
            comp.new_program(program, user_input=[phase_setting, input_signal])
            input_signal = comp.program_output[0]
        if input_signal > max_thruster_signal:
            max_thruster_signal = input_signal
    return max_thruster_signal


@time_decorator
def part2(program):
    comps = [Intcode(), Intcode(), Intcode(), Intcode(), Intcode()]
    for c in comps:
        c.suppress_output = True
    t_signal = 0
    for sequence in permutations(range(5, 10), 5):
        active_c = 0
        for phase_setting in sequence:
            comps[active_c].new_program(program, user_input=[phase_setting])
            active_c += 1
        comps[0].user_input = iter([0])
        comps[0].resume_execution()
        active_c = 1
        while not comps[-1].has_program_finished:
            if active_c > 4:
                active_c = 0
            comps[active_c].user_input = iter([comps[active_c - 1].program_output[-1]])
            comps[active_c].resume_execution()
            active_c += 1
        if comps[-1].program_output[-1] > t_signal:
            t_signal = comps[-1].program_output[-1]
    return t_signal


if __name__ == "__main__":
    day7_program = open_program("day7_input.csv")
    computer = Intcode()
    computer.suppress_output = True
    thruster_signal = part1(computer, day7_program)
    print("=" * 20 + " PART 1 " + "=" * 20)
    print(f"Max thruster signal: {thruster_signal}")
    fb_thruster_signal = part2(day7_program)
    print("=" * 20 + " PART 2 " + "=" * 20)
    print(f"Max thruster signal after fb loop: {fb_thruster_signal}")
