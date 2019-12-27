from typing import List


class Intcode:

    def __init__(self, program_input: List = None):
        self.program_input = program_input
        self.program_output = None
        self.instruction_ptr = 0
        self.opcode = {1: self.addition, 2: self.multiplication, 99: self.end_program}
        if self.program_input is not None:
            self.opcode[self.program_input[self.instruction_ptr]]()

    def addition(self):
        first_integer, second_integer, store_idx = self.program_input[self.instruction_ptr + 1:self.instruction_ptr + 4]
        self.program_input[store_idx] = self.program_input[first_integer] + self.program_input[second_integer]
        self.advance(4)

    def multiplication(self):
        first_integer, second_integer, store_idx = self.program_input[self.instruction_ptr + 1:self.instruction_ptr + 4]
        self.program_input[store_idx] = self.program_input[first_integer] * self.program_input[second_integer]
        self.advance(4)

    def advance(self, advance_by: int):
        self.instruction_ptr += advance_by
        try:
            self.opcode[self.program_input[self.instruction_ptr]]()
        except KeyError:
            print(f"Unknown input encountered at index {self.instruction_ptr}")

    @staticmethod
    def end_program():
        pass
        # print("Finished program execution!")

    def new_program(self, new_input: List):
        self.program_input = new_input
        self.instruction_ptr = 0
        self.opcode[self.program_input[self.instruction_ptr]]()