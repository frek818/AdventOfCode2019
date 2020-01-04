from Intcode import Intcode

if __name__ == "__main__":
    with open("day5_input.csv", "r") as f:
        computer = Intcode()
        computer.new_program(list(map(int, next(f).split(','))))
        # TODO Create test with this
