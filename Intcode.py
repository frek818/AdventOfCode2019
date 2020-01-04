from typing import List


class Intcode:

    PARAMETER_MODE = 0
    IMMEDIATE_MODE = 1

    def __init__(self, program_input: List = None):
        self.program_input = program_input
        self.instruction_ptr = 0
        self.opcode = {1: self.addition, 2: self.multiplication, 3: self.save_param, 4: self.output_param,
                       99: self.end_program}
        if self.program_input is not None:
            self.opcode[self.program_input[self.instruction_ptr]]()

    def addition(self, p1_mode: int = 0, p2_mode: int = 0):
        first_integer, second_integer, store_idx = self.program_input[self.instruction_ptr + 1:self.instruction_ptr + 4]
        self.program_input[store_idx] = self.read_mode(first_integer, p1_mode) + self.read_mode(second_integer, p2_mode)
        self.advance(4)

    def multiplication(self, p1_mode: int = 0, p2_mode: int = 0):
        first_integer, second_integer, store_idx = self.program_input[self.instruction_ptr + 1:self.instruction_ptr + 4]
        self.program_input[store_idx] = self.read_mode(first_integer, p1_mode) * self.read_mode(second_integer, p2_mode)
        self.advance(4)

    def save_param(self):
        store_idx = self.program_input[self.instruction_ptr + 1]
        self.program_input[store_idx] = int(input("User input requested: "))
        self.advance(2)

    def output_param(self, p1_mode: int = 0):
        param_idx = self.program_input[self.instruction_ptr + 1]
        print(self.read_mode(param_idx, p1_mode))
        self.advance(2)

    def advance(self, advance_by: int):
        self.instruction_ptr += advance_by
        instruction = str(self.program_input[self.instruction_ptr])
        opcode_key = int(instruction[-2:])
        parameter_modes = map(int, reversed(instruction[:-2]))
        try:
            self.opcode[opcode_key](*parameter_modes)
        except KeyError:
            print(f"Unknown input encountered at index {self.instruction_ptr}")

    def read_mode(self, value: int, mode: int) -> int:
        if mode == Intcode.PARAMETER_MODE:
            return self.program_input[value]
        elif mode == Intcode.IMMEDIATE_MODE:
            return value
        else:
            raise ValueError("Unknown parameter mode")

    @staticmethod
    def end_program():
        pass
        # print("Finished program execution!")

    def new_program(self, new_input: List):
        self.program_input = new_input
        self.instruction_ptr = 0
        self.advance(0)
