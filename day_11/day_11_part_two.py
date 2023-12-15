import itertools
import numpy as np
from tqdm import tqdm


def get_empty_rows(universe):
    empty_row_idx = []
    r, c = universe.shape
    for l in range(r):
        if np.sum(universe[l, :]) == 0:
            empty_row_idx.append(l)
    return empty_row_idx


def get_expansion_matrices(universe, expansion_factor):
    r, c = universe.shape

    empty_row_idx = get_empty_rows(universe)
    empty_col_idx = get_empty_rows(universe.T)

    row_incr = np.zeros((r, c))
    col_incr = np.zeros((r, c))

    for idx in empty_row_idx:
        row_incr[idx:, :] += expansion_factor - 1

    for idx in empty_col_idx:
        col_incr[:, idx:] += expansion_factor - 1

    return {
        'row': row_incr,
        'col': col_incr
    }


def expand_universe(universe, expansion_factor=1):
    r, c = universe.shape
    empty_row_idx = get_empty_rows(universe)
    empty_col_idx = get_empty_rows(universe.T)

    expanded_universe = universe.copy()
    padding = np.zeros((expansion_factor, 1))

    for i, idx in enumerate(empty_row_idx):
        in_idx = idx + (expansion_factor * i)
        expanded_universe = np.insert(expanded_universe, in_idx,
                                      padding, axis=0)
    for i, idx in enumerate(empty_col_idx):
        in_idx = idx + (expansion_factor * i)
        expanded_universe = np.insert(expanded_universe, in_idx,
                                      padding, axis=1)
    # expanded_universe = np.insert(expanded_universe, empty_col_idx,
    #                               padding, axis=1)

    return expanded_universe


def load_data(data_path):

    cnt = itertools.count(1)
    lines = [x.strip() for x in open(data_path, 'r').readlines()]
    print('[I] Found %d lines!' % len(lines))
    universe = [[0 if x == '.' else next(cnt) for x in l]
                for l in lines]
    universe_size = (len(lines), len(lines[0]))
    data = np.array(universe)
    num_galaxies = next(cnt) - 1

    return data, num_galaxies


def get_shortest_path(orig_universe, incr_dict, tgt_gal, dest_gal):

    gal_a_coord = np.where(orig_universe == tgt_gal)
    gal_b_coord = np.where(orig_universe == dest_gal)

    A_r, A_c = gal_a_coord[0][0], gal_a_coord[1][0]
    exp_A_r = A_r + incr_dict['row'][A_r, A_c]
    exp_A_c = A_c + incr_dict['col'][A_r, A_c]

    B_r, B_c = gal_b_coord[0][0], gal_b_coord[1][0]
    exp_B_r = B_r + incr_dict['row'][B_r, B_c]
    exp_B_c = B_c + incr_dict['col'][B_r, B_c]

    dist = np.abs(exp_B_r - exp_A_r) + np.abs(exp_B_c - exp_A_c)
    # print('%d -> %d: %d' % (tgt_gal, dest_gal, dist))
    return dist


def main(file_path):
    # lines = [x.strip() for x in open(file_path, 'r').readlines()]
    # print('[I] Found %d lines!' % len(lines))
    universe, num_galaxies = load_data(file_path)
    print('[I] Observed universe size: ', universe.shape)
    incr_dict = get_expansion_matrices(universe, expansion_factor=1000000)
    expanded_r, expanded_c = universe.shape
    expanded_r += int(incr_dict['row'].max())
    expanded_c += int(incr_dict['col'].max())
    print('[I] Actual universe size: ', (expanded_r, expanded_c))
    # Calculate the pairs
    galaxy_pairs = list(itertools.combinations(range(
          1, num_galaxies + 1
         ), 2))
    print('[I] Found %d combinations of galaxies' % len(galaxy_pairs))

    running_total = 0

    for i in tqdm(galaxy_pairs):
    # for i in galaxy_pairs:
        running_total += get_shortest_path(universe, incr_dict,
                                           i[0], i[1])

    print('[I] Final total is: ', running_total)


if __name__ == '__main__':
    # main(file_path='../data/day11_test.str')
    main(file_path='../data/day11_input.str')

