def part1(filename):
    with open(filename, "r") as f:
        orbit_ctr = 0
        direct_orbits = dict()
        for line in f:
            orbit_center, orbiting_obj = line.strip("\n").split(")")
            if orbiting_obj not in direct_orbits:
                direct_orbits[orbiting_obj] = orbit_center
        for obj in direct_orbits.keys():
            next_obj = direct_orbits[obj]
            orbit_ctr += 1
            while next_obj != "COM":
                next_obj = direct_orbits[next_obj]
                orbit_ctr += 1
        print("=" * 20 + " PART 1 " + "=" * 20)
        print(f"Total number of direct and indirect orbits: {orbit_ctr}")


if __name__ == "__main__":
    part1("day6_input.txt")
