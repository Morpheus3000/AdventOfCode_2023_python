import itertools
import numpy as np
from tqdm import tqdm


def load_data(data_path):

    lines = [x.strip() for x in open(data_path, 'r').readlines()]
    print('[I] Found %d lines!' % len(lines))

    return data


def main(file_path):
    data = load_data(file_path)

    running_total = 0

    print('[I] Final total is: ', running_total)


if __name__ == '__main__':
    main(file_path='../data/day11_test.str')
    # main(file_path='../data/day11_input.str')

