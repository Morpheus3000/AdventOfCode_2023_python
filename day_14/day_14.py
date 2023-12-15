import itertools
import numpy as np
from tqdm import tqdm


def load_data(data_path):
    lines = [[x.strip() for x in l if len(x.strip()) > 0]
             for l in open(data_path, 'r').readlines()]
    print('[I] Found %d lines!' % len(lines))

    lines = [[4 if x == 'O' else 8 if x == '#' else 0 for x in l]
             for l in lines]

    data = np.array(lines)

    return data


def tilt_board(data, direction='n'):
    r, c = data.shape

    tilt_board = np.zeros((r, c)).astype(np.uint8)
    # cnt = 0
    for i in range(c):
        tgt_col = data[:, i]
        e_r = tgt_col.shape
        idx = np.argwhere(tgt_col == 8)
        tilt_board[idx[:, 0], i] = 8
        idx = np.append(idx, [[e_r]])
        start_idx = 0
        for j in range(len(idx)):
            end_idx = idx[j]
            sliced = tgt_col[start_idx:end_idx]
            num_rocks = np.count_nonzero(sliced == 4)
            if num_rocks > 0:
                tilt_board[start_idx:start_idx + num_rocks, i] = 4
            start_idx = end_idx + 1
        # if cnt == 2:
        #     break
        # else:
        #     cnt += 1

    return tilt_board


def calculate_load(board):
    board = board[::-1]
    r, c = board.shape

    total_weight = 0
    for i in range(r):
        row_slice = board[i, :]
        num_rocks = np.count_nonzero(row_slice == 4)
        total_weight += (i + 1) * num_rocks

    return total_weight


def main(file_path):
    data = load_data(file_path)
    tilted_board = tilt_board(data, direction='n')

    running_total = calculate_load(tilted_board)

    print('[I] Final total is: ', running_total)


if __name__ == '__main__':
    # main(file_path='../data/day14_test.str')
    main(file_path='../data/day14_input.str')
