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
        self.computer.program_input = None

    def test_init(self):
        self.assertTrue(self.computer.program_input is None)

    def test_addition(self):
        self.computer.new_program([1001, 1, 1, 0, 99])
        self.assertEqual(self.computer.program_input, [2, 1, 1, 0, 99])

    def test_multiplication_1(self):
        self.computer.new_program([1002, 3, 2, 3, 99])
        self.assertEqual(self.computer.program_input, [1002, 3, 2, 6, 99])

    def test_multiplication_2(self):
        self.computer.new_program([1002, 4, 99, 5, 99, 0])
        self.assertEqual(self.computer.program_input, [1002, 4, 99, 5, 99, 9801])

    def test_program(self):
        self.computer.new_program([1001, 1, 1001, 4, 99, 5, 6, 0, 99])
        self.assertEqual(self.computer.program_input, [30, 1, 1001, 4, 1002, 5, 6, 0, 99])

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


if __name__ == '__main__':
    unittest.main()
