from collections import Counter

import numpy as np

# Not very elegant but works
if __name__ == "__main__":
    start = 264793
    end = 803935

    passwords = np.asarray(list(map(list, map(str, range(start, end)))), dtype=int)
    for i in range(5):
        passwords = passwords[passwords[:, i] <= passwords[:, i + 1]]
    valid_passwords = np.array([], dtype=int).reshape(0, 6)
    for i in range(5):
        valid_passwords = np.r_[valid_passwords, passwords[passwords[:, i] == passwords[:, i + 1]]]
    valid_passwords = np.unique(valid_passwords, axis=0)
    print(f"PART 1\t Number of valid passwords: {len(valid_passwords)}")
    valid_ctr = 0
    for password in iter(map(dict, map(Counter, valid_passwords))):
        for occurrence in password.values():
            if occurrence == 2:
                valid_ctr += 1
                break
    print(f"PART 2\t Number of valid passwords: {valid_ctr}")
