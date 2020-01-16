import numpy as np
from matplotlib import pyplot as plt

from my_tools import time_decorator


@time_decorator
def part1(pic_data: str, w: int, h: int) -> int:
    pixels = np.asarray(list(pic_data), dtype=int).reshape((len(pic_data) // (w*h), h, w))
    zero_cnt = 0
    most_zeros_idx = 0
    for i in range(pixels.shape[0]):
        nonzero_elements = np.count_nonzero(pixels[i])
        if nonzero_elements > zero_cnt:
            zero_cnt = nonzero_elements
            most_zeros_idx = i
    ones_and_twos = pixels[most_zeros_idx][pixels[most_zeros_idx] == 1].size * \
                    pixels[most_zeros_idx][pixels[most_zeros_idx] == 2].size
    return ones_and_twos


@time_decorator
def part2(pic_data: str, w: int, h: int):
    pixels = np.asarray(list(pic_data), dtype=int).reshape((len(pic_data) // (w*h), w*h))
    image = []
    for layer in pixels.T:
        image.append(layer[layer != 2][0])
    image = np.asarray(image, dtype=int).reshape((h, w))
    return image


if __name__ == "__main__":
    with open("day8_input.txt") as f:
        pixel_data = next(f)
        width = 25
        height = 6
        part1_solution = part1(pixel_data, width, height)
        print("=" * 20 + " PART 1 " + "=" * 20)
        print(f"Ones and twos: {part1_solution}")
        final_image = part2(pixel_data, width, height)
        print("=" * 20 + " PART 2 " + "=" * 20)
        print("Decoded image: ")
        print(final_image)
        plt.figure("Decoded image")
        plt.imshow(final_image)
        plt.show()
