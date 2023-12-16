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


def get_blocked_idx(data):
    r, c = data.shape
    return_dict = {
        'n': [],
        's': [],
        'e': [],
        'w': [],
        'total_map': []
    }

    return_dict['total_map'] = data == 8

    # For North
    for i in range(c):
        tgt_col = data[:, i]
        idx = np.argwhere(tgt_col == 8)
        idx = np.append(idx, r)
        return_dict['n'].append(idx)

    # For South
    return_dict['s'] = [np.append(np.sort(r - 1 - x[:-1]), r)
                        for x in return_dict['n']]

    # For West
    for i in range(r):
        tgt_row = data[i, :]
        idx = np.argwhere(tgt_row == 8)
        idx = np.append(idx, c)
        return_dict['w'].append(idx)

    # For East
    return_dict['e'] = [np.append(np.sort(c - 1 - x[:-1]), c)
                        for x in return_dict['w']]
    return return_dict


def tilt_board_inplace(data, block_idx, block_map):
    r, c = data.shape

    tilted_board = np.zeros((r, c)).astype(np.uint8)
    tilted_board[block_map] = 8
    for i in range(c):
        tgt_col = data[:, i]
        idx = block_idx[i]
        start_idx = 0
        for j in range(len(idx)):
            end_idx = idx[j]
            sliced = tgt_col[start_idx:end_idx]
            num_rocks = np.count_nonzero(sliced == 4)
            if num_rocks > 0:
                data[start_idx:start_idx + num_rocks, i] = 4
                data[start_idx + num_rocks:end_idx, i] = 0
            start_idx = end_idx + 1

    # return tilted_board


def run_cycle_inplace(data, bloc_dict):
    # Tilt North
    tilt_board_inplace(data, bloc_dict['n'], bloc_dict['total_map'])
    # Tilt West
    tilt_board_inplace(data.T, bloc_dict['w'], bloc_dict['total_map'])
    # Tilt South
    tilt_board_inplace(data[::-1], bloc_dict['s'], bloc_dict['total_map'])
    # Tilt East
    tilt_board_inplace(data.T[::-1], bloc_dict['e'], bloc_dict['total_map'])


def calculate_no_loop(board):
    board = board[::-1]
    totals = sum([x * y for x, y in enumerate(
        np.count_nonzero(board == 4, axis=1), 1
    )])
    return totals


def test(file_path):
    data = load_data(file_path)

    print(data)
    bloc_dict = get_blocked_idx(data)
    # print('Tilt South')
    # # Tilt South
    # tilt_board_inplace(data[::-1], bloc_dict['s'], bloc_dict['total_map'])
    # print(data)

    # print('Tilt West')
    # # Tilt West
    # tilt_board_inplace(data.T, bloc_dict['w'], bloc_dict['total_map'])
    # print(data)

    print('Tilt East')
    # Tilt East
    tilt_board_inplace(data.T[::-1], bloc_dict['e'], bloc_dict['total_map'])
    print(data)


def main(file_path):
    data = load_data(file_path)
    bloc_dict = get_blocked_idx(data)
    # tilt_board_inplace(data, bloc_dict['n'], bloc_dict['total_map'])

    # running_total = calculate_load(tilted_board)
    # running_total = calculate_no_loop(data)
    # run_cycle_inplace(data, bloc_dict)
    baseline_total = 89170

    print('[I] Baseline: %d' % baseline_total)

    t = tqdm(range(1_000_000_000))
    cnt = 0
    term_cond = 10
    for i in t:
        run_cycle_inplace(data, bloc_dict)
        total = calculate_no_loop(data)
        t.set_description('Current Total: %d' % total)
        if total == baseline_total and cnt < term_cond:
            tqdm.write('[%d] Sum: %d\n' % (i, total))
            cnt += 1
        if cnt == term_cond:
            break

    # print('[I] Final total is: ', running_total)


if __name__ == '__main__':
    # test(file_path='../data/day14_test.str')
    # main(file_path='../data/day14_test.str')
    main(file_path='../data/day14_input.str')
