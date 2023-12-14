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

def expand_universe(universe):
    r, c = universe.shape
    empty_row_idx = get_empty_rows(universe)
    empty_col_idx = get_empty_rows(universe.T)

    expanded_universe = universe.copy()
    empty_row = np.zeros((1, c))
    empty_col = np.zeros((r, 1))

    expanded_universe = np.insert(expanded_universe, empty_row_idx, 0, axis=0)
    expanded_universe = np.insert(expanded_universe, empty_col_idx, 0, axis=1)

    return expanded_universe

def load_data(data_path):
    cnt = itertools.count(1)
    lines = [x.strip() for x in open(data_path, 'r').readlines()]
    print('[I] Found %d lines!' % len(lines))
    universe = [[0 if x == '.' else next(cnt) for x in l] for l in lines]
    universe_size = (len(lines), len(lines[0]))
    data = np.array(universe)
    num_galaxies = next(cnt) - 1

    return data, num_galaxies

def get_shortest_path(universe, tgt_gal, dest_gal):
    gal_a_coord = np.where(universe == tgt_gal)
    gal_b_coord = np.where(universe == dest_gal)

    A_r, A_c = gal_a_coord[0][0], gal_a_coord[1][0]
    B_r, B_c = gal_b_coord[0][0], gal_b_coord[1][0]

    dist = np.abs(B_r - A_r) + np.abs(B_c - A_c)
    # print('%d -> %d: %d' % (tgt_gal, dest_gal, dist))
    return dist

def main(file_path):
    # lines = [x.strip() for x in open(file_path, 'r').readlines()]
    # print('[I] Found %d lines!' % len(lines))
    universe, num_galaxies = load_data(file_path)
    expanded_universe = expand_universe(universe)
    # Calculate the pairs
    galaxy_pairs = list(itertools.combinations(range(1, num_galaxies + 1), 2))
    print('[I] Found %d combinations of galaxies' % len(galaxy_pairs))

    running_total = 0

    for i in tqdm(galaxy_pairs):
    # for i in galaxy_pairs:
        running_total += get_shortest_path(expanded_universe, i[0], i[1])

    print('[I] Final total is: ', running_total)


if __name__ == '__main__':
    # main(file_path='../data/day11_test.str')
    main(file_path='../data/day11_input.str')

