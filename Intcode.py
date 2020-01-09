from typing import List


class Intcode:

    PARAMETER_MODE = 0
    IMMEDIATE_MODE = 1

    def __init__(self, program_input: List = None):
        self.program = program_input
        self.instruction_ptr = 0
        self.opcode = {1: self.addition, 2: self.multiplication, 3: self.save_param, 4: self.output_param,
                       5: self.jump_if_true, 6: self.jump_if_false, 7: self.less_than, 8: self.equal_to,
                       99: self.end_program}
        if self.program is not None:
            self.program = self.program[:]
            self.opcode[self.program[self.instruction_ptr]]()
        # else:
        #     print("Awaiting instructions...")

    def addition(self, p1_mode: int = 0, p2_mode: int = 0):
        first_integer, second_integer, store_idx = self.program[self.instruction_ptr + 1:self.instruction_ptr + 4]
        self.program[store_idx] = self.read_mode(first_integer, p1_mode) + self.read_mode(second_integer, p2_mode)
        self.advance(4)

    def multiplication(self, p1_mode: int = 0, p2_mode: int = 0):
        first_integer, second_integer, store_idx = self.program[self.instruction_ptr + 1:self.instruction_ptr + 4]
        self.program[store_idx] = self.read_mode(first_integer, p1_mode) * self.read_mode(second_integer, p2_mode)
        self.advance(4)

    def save_param(self):
        store_idx = self.program[self.instruction_ptr + 1]
        self.program[store_idx] = int(input("User input requested: "))
        self.advance(2)

    def output_param(self, p1_mode: int = 0):
        param_idx = self.program[self.instruction_ptr + 1]
        print(self.read_mode(param_idx, p1_mode))
        self.advance(2)

    def jump_if_true(self, p1_mode: int = 0, p2_mode: int = 0):
        condition, param = self.program[self.instruction_ptr + 1:self.instruction_ptr + 3]
        if self.read_mode(condition, p1_mode) != 0:
            self.instruction_ptr = self.read_mode(param, p2_mode)
            self.advance(0)
        else:
            self.advance(3)

    def jump_if_false(self, p1_mode: int = 0, p2_mode: int = 0):
        condition, param = self.program[self.instruction_ptr + 1:self.instruction_ptr + 3]
        if self.read_mode(condition, p1_mode) == 0:
            self.instruction_ptr = self.read_mode(param, p2_mode)
            self.advance(0)
        else:
            self.advance(3)

    def less_than(self, p1_mode: int = 0, p2_mode: int = 0):
        first_integer, second_integer, store_idx = self.program[self.instruction_ptr + 1:self.instruction_ptr + 4]
        if self.read_mode(first_integer, p1_mode) < self.read_mode(second_integer, p2_mode):
            self.program[store_idx] = 1
        else:
            self.program[store_idx] = 0
        self.advance(4)

    def equal_to(self, p1_mode: int = 0, p2_mode: int = 0):
        first_integer, second_integer, store_idx = self.program[self.instruction_ptr + 1:self.instruction_ptr + 4]
        if self.read_mode(first_integer, p1_mode) == self.read_mode(second_integer, p2_mode):
            self.program[store_idx] = 1
        else:
            self.program[store_idx] = 0
        self.advance(4)

    def advance(self, advance_by: int):
        self.instruction_ptr += advance_by
        instruction = str(self.program[self.instruction_ptr])
        opcode_key = int(instruction[-2:])
        parameter_modes = map(int, reversed(instruction[:-2]))
        # print(f"Idx {self.instruction_ptr}\tOpcode {self.program_input[self.instruction_ptr]}")
        try:
            self.opcode[opcode_key](*parameter_modes)
        except KeyError:
            print(f"Unknown input {self.program[self.instruction_ptr]} encountered at "
                  f"index {self.instruction_ptr}")

    def read_mode(self, value: int, mode: int) -> int:
        if mode == Intcode.PARAMETER_MODE:
            return self.program[value]
        elif mode == Intcode.IMMEDIATE_MODE:
            return value
        else:
            raise ValueError("Unknown parameter mode")

    @staticmethod
    def end_program():
        pass
        # print("Finished program execution!")

    def new_program(self, new_input: List):
        self.program = new_input[:]
        self.instruction_ptr = 0
        self.advance(0)
