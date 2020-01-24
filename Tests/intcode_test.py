import os
import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest import mock

from Intcode import Intcode


class TestIntcode(unittest.TestCase):
    def setUp(self):
        self.computer = Intcode()

    def tearDown(self) -> None:
        self.computer.program = None

    def test_init(self):
        self.assertTrue(self.computer.program is None)

    def test_addition(self):
        self.computer.new_program([1001, 1, 1, 0, 99])
        self.assertEqual(list(self.computer.program.values()), [2, 1, 1, 0, 99])

    def test_multiplication_1(self):
        self.computer.new_program([1002, 3, 2, 3, 99])
        self.assertEqual(list(self.computer.program.values()), [1002, 3, 2, 6, 99])

    def test_multiplication_2(self):
        self.computer.new_program([1002, 4, 99, 5, 99, 0])
        self.assertEqual(list(self.computer.program.values()), [1002, 4, 99, 5, 99, 9801])

    def test_program(self):
        self.computer.new_program([1001, 1, 1001, 4, 99, 5, 6, 0, 99])
        self.assertEqual(list(self.computer.program.values()), [30, 1, 1001, 4, 1002, 5, 6, 0, 99])

    def test_unknown_opcode(self):
        self.assertRaises(KeyError, self.computer.new_program([98, 0, 0, 99]))

    @mock.patch("builtins.input", side_effect=["1"])
    def test_immediate_mode(self, inp):
        stdout = StringIO()
        with redirect_stdout(stdout):
            file_path = (os.path.dirname(__file__)) + "/immediate_mode_test_input.csv"
            with open(file_path, "r") as f:
                self.computer.new_program(list(map(int, next(f).split(","))))
        self.assertEqual(stdout.getvalue(), "0\n0\n0\n0\n0\n0\n0\n0\n0\n13210611\n")

    def test_equal_to(self):
        stdout = StringIO()
        with redirect_stdout(stdout):
            self.computer.new_program([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], user_input=[1])
            self.computer.new_program([3, 3, 1108, -1, 8, 3, 4, 3, 99], user_input=[8])
        self.assertEqual(stdout.getvalue(), "0\n1\n")

    @mock.patch("builtins.input", side_effect=["1", "8"])
    def test_less_than(self, inp):
        stdout = StringIO()
        with redirect_stdout(stdout):
            self.computer.new_program([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8])
            self.computer.new_program([3, 3, 1107, -1, 8, 3, 4, 3, 99])
        self.assertEqual(stdout.getvalue(), "1\n0\n")

    def test_jump(self):
        stdout = StringIO()
        with redirect_stdout(stdout):
            self.computer.new_program([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], user_input=[1])
            self.computer.new_program([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], user_input=[0])
        self.assertEqual(stdout.getvalue(), "1\n0\n")

    @mock.patch("builtins.input", side_effect=["7", "8", "9"])
    def test_program_2(self, inp):
        stdout = StringIO()
        with redirect_stdout(stdout):
            for i in range(3):
                self.computer.new_program([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                                           1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                                           999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99])
        self.assertEqual(stdout.getvalue(), "999\n1000\n1001\n")

    def test_large_number(self):
        self.computer.new_program([1102, 34915192, 34915192, 7, 4, 7, 99, 0])
        self.assertEqual(self.computer.program_output[0], 1219070632396864)

    def test_large_number_2(self):
        self.computer.new_program([104, 1125899906842624, 99])
        self.assertEqual(self.computer.program_output[0], 1125899906842624)

    def test_relative_mode(self):
        program = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
        self.computer.new_program(program)
        self.assertEqual(self.computer.program_output, program)


if __name__ == '__main__':
    unittest.main()
