import itertools
import numpy as np
from tqdm import tqdm


def load_data(data_path):
    lines = [list(x.strip()) if len(x.strip()) > 1 else 'b'
             for x in open(data_path, 'r').readlines()]
    print('[I] Found %d lines!' % len(lines))

    break_points = [i for i, val in enumerate(lines) if val == 'b']
    break_points.append(len(lines))

    notes = []

    prev_i = -1
    for i, bp in enumerate(break_points):
        arr = np.array(lines[prev_i + 1:bp])
        prev_i = bp
        notes.append(arr)

    print('[I] Found %d notes!' % len(notes))
    return notes


def find_reflection_line(arr):
    r, c = arr.shape

    # checking vertical reflection line
    # (vals == (0, 1)).all(axis=1).nonzero()

    vert_ref_line = -1

    found = False
    for i in range(c - 1):
        lhs = arr[:, i]
        rhs = arr[:, i + 1]

        if np.array_equal(lhs, rhs):
            vert_ref_line = i
            found = True
            break

    if found:
        return {
            'reflec vert': True,
            'idx': vert_ref_line,
        }

    hori_ref_line = -1
    for i in range(r - 1):
        lhs = arr[i, :]
        rhs = arr[i + 1, :]

        if np.array_equal(lhs, rhs):
            hori_ref_line = i
            found = True
            break

    if found:
        return {
            'reflec vert': False,
            'idx': hori_ref_line,
        }
    else:
        return None


def test_find_reflection_line(arr, direction):
    r, c = arr.shape

    # checking vertical reflection line
    # (vals == (0, 1)).all(axis=1).nonzero()

    if direction == 'vert':
        vert_ref_line = -1
        for i in range(c - 1):
            lhs = arr[:, i]
            rhs = arr[:, i + 1]

            if np.array_equal(lhs, rhs):
                vert_ref_line = i
                found = True
                return {
                    'reflec vert': True,
                    'idx': vert_ref_line,
                }
                break

    elif direction == 'hori':
        hori_ref_line = -1
        for i in range(r - 1):
            lhs = arr[i, :]
            rhs = arr[i + 1, :]

            if np.array_equal(lhs, rhs):
                hori_ref_line = i
                found = True
                return {
                    'reflec vert': False,
                    'idx': hori_ref_line,
                }

def test_case(notes):
    pattern_dict = {}

    num_cols = 0
    num_rows = 0

    ret_dict = test_find_reflection_line(notes[0], direction='vert')
    if ret_dict['reflec vert']:
        num_cols += ret_dict['idx'] + 1
    else:
        num_rows += (100 * (ret_dict['idx'] + 1))

    ret_dict = test_find_reflection_line(notes[1], direction='hori')
    if ret_dict['reflec vert']:
        num_cols += ret_dict['idx'] + 1
    else:
        num_rows += (100 * (ret_dict['idx'] + 1))

    running_total = num_cols + num_rows

    print('[I] Final total is: ', running_total)


def main(file_path):
    notes = load_data(file_path)

    pattern_dict = {}

    num_cols = 0
    num_rows = 0

    test_case(notes)

    # for i, note in tqdm(enumerate(notes), total=len(notes)):
    #     ret_dict = find_reflection_line(note)
    #     pattern_dict[i] = ret_dict

    #     if ret_dict['reflec vert']:
    #         num_cols += ret_dict['idx'] + 1
    #     else:
    #         num_rows += (100 * (ret_dict['idx'] + 1))

    # running_total = num_cols + num_rows

    # print('[I] Final total is: ', running_total)


if __name__ == '__main__':
    main(file_path='../data/day13_test.str')
    # main(file_path='../data/day13_input.str')
