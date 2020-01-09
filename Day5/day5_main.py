from Intcode import Intcode

if __name__ == "__main__":
    with open("day5_input.csv", "r") as f:
        program_input = list(map(int, next(f).split(",")))
        computer = Intcode()
        print("=" * 20 + " PART 1 " + "=" * 20)
        print("Enter TEST ID: 1")
        computer.new_program(program_input)  # Enter 1
        print("=" * 20 + " PART 2 " + "=" * 20)
        print("Enter TEST ID: 5")
        computer.new_program(program_input)  # Enter 5
