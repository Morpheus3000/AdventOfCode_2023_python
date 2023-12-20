import numpy as np
from tqdm import tqdm
import time


LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'


def load_data(data_path):

    lines = [x.strip() for x in open(data_path, 'r').readlines()]
    print('[I] Found %d lines!' % len(lines))
    grid = np.array([list(x) for x in lines])
    print(grid)
    print(grid.shape)
    return grid


def cell_checker(inp_dir, tgt_sym, sym_coord):
    if tgt_sym == '.':
        splitted = False
        out_dir = inp_dir
        if inp_dir == 'r':
            out_coord = [sym_coord[0], sym_coord[1] + 1]

        elif inp_dir == 'l':
            out_coord = [sym_coord[0], sym_coord[1] - 1]

        elif inp_dir == 'u':
            out_coord = [sym_coord[0] + 1, sym_coord[1]]

        elif inp_dir == 'd':
            out_coord = [sym_coord[0] - 1, sym_coord[1]]

    elif tgt_sym == '\\':
        splitted = False
        if inp_dir == 'r':
            out_coord = [sym_coord[0] + 1, sym_coord[1]]
            out_dir = 'd'
        elif inp_dir == 'l':
            out_coord = [sym_coord[0] - 1, sym_coord[1]]
            out_dir = 'u'
        elif inp_dir == 'u':
            out_coord = [sym_coord[0], sym_coord[1] + 1]
            out_dir = 'r'
        elif inp_dir == 'd':
            out_coord = [sym_coord[0], sym_coord[1] - 1]
            out_dir = 'l'

    elif tgt_sym == '/':
        splitted = False
        if inp_dir == 'r':
            out_coord = [sym_coord[0] - 1, sym_coord[1]]
            out_dir = 'u'
        elif inp_dir == 'l':
            out_coord = [sym_coord[0] + 1, sym_coord[1]]
            out_dir = 'd'
        elif inp_dir == 'u':
            out_coord = [sym_coord[0], sym_coord[1] - 1]
            out_dir = 'l'
        elif inp_dir == 'd':
            out_coord = [sym_coord[0], sym_coord[1] + 1]
            out_dir = 'r'

    elif tgt_sym == '|':
        if inp_dir == 'r':
            splitted = True
            out_dir = ['u', 'd']
            out_coord = [
                [sym_coord[0] + 1, sym_coord[1]],
                [sym_coord[0] - 1, sym_coord[1]],
            ]
        elif inp_dir == 'l':
            splitted = True
            out_dir = ['u', 'd']
            out_coord = [
                [sym_coord[0] + 1, sym_coord[1]],
                [sym_coord[0] - 1, sym_coord[1]],
            ]
        elif inp_dir == 'u':
            splitted = False
            out_coord = [sym_coord[0] + 1, sym_coord[1]]
            out_dir = inp_dir
        elif inp_dir == 'd':
            splitted = False
            out_coord = [sym_coord[0] - 1, sym_coord[1]]
            out_dir = inp_dir

    elif tgt_sym == '-':
        if inp_dir == 'r':
            splitted = False
            out_coord = [sym_coord[0], sym_coord[1] + 1]
            out_dir = inp_dir
        elif inp_dir == 'l':
            splitted = False
            out_coord = [sym_coord[0], sym_coord[1] - 1]
            out_dir = inp_dir
        elif inp_dir == 'u':
            splitted = True
            out_dir = ['r', 'l']
            out_coord = [
                [sym_coord[0], sym_coord[1] + 1],
                [sym_coord[0], sym_coord[1] - 1],
            ]
        elif inp_dir == 'd':
            splitted = True
            out_dir = ['r', 'l']
            out_coord = [
                [sym_coord[0], sym_coord[1] + 1],
                [sym_coord[0], sym_coord[1] - 1],
            ]

    return {
        'coord': out_coord,
        'dir': out_dir,
        'split': splitted
    }


def grid_print(grid, sym, coord, prev_line_num):
    # Clear N lines
    [print(LINE_UP, end=LINE_CLEAR) for i in range(prev_line_num)]

    mod_grid = grid
    if len(sym) > 0:
        mod_grid[coord[0], coord[1]] = sym
    r, c = mod_grid.shape
    [print(' '.join(grid[x, :])) for x in range(r)]


def ray_cast(grid):
    vis_grid = grid.copy()
    r, c = vis_grid.shape
    grid_print(vis_grid, '', [0, 0], 0)

    rays = [{
        'start': [0, 0],
        'dir': 'r'
    }]

    cur_ray_ind = 0

    inp_dir = rays[cur_ray_ind]['dir']
    sym_coord = rays[cur_ray_ind]['start']
    splitted = False

    cnt = 0
    while len(rays) > 0:
        # grid_print(vis_grid, '*', sym_coord, r)
        time.sleep(0.5)
        tgt_sym = grid[sym_coord[0], sym_coord[1]]
        print(cnt, sym_coord, tgt_sym, splitted, inp_dir)
        if not splitted:
            out_dict = cell_checker(inp_dir, tgt_sym, sym_coord)
            inp_dir = out_dict['dir']
            sym_coord = out_dict['coord']
            tgt_sym = grid[sym_coord[0], sym_coord[1]]
            splitted = out_dict['split']
        if cnt > 10:
            break
        else:
            cnt += 1


def test(file_path):
    data = load_data(file_path)
    running_total = 0
    print('[I] Final total is: ', running_total)

    r, c = data.shape
    sym_coord = [2, 2]
    tgt_sym = '-'

    # for inp_dir in ['r', 'l', 'u', 'd']:
    #     out_dict = cell_checker(inp_dir, tgt_sym, sym_coord)
    #     print(sym_coord, end='')
    #     print(' [%s : %s]' % (tgt_sym, inp_dir), end='')
    #     print(' -> ', end='')
    #     print(out_dict['coord'], end='')
    #     print(out_dict['dir'], end='')
    #     print(', Split: ', out_dict['split'])

    # grid_print(data, '', [0, 0], 0)
    # for j in range(r):
    #     for i in range(c):
    #         time.sleep(0.5)
    #         grid_print(data, '*', [j, i], r)
    data[0, 1] = '-'
    ray_cast(data)


def main(file_path):
    data = load_data(file_path)
    running_total = 0
    print('[I] Final total is: ', running_total)


if __name__ == '__main__':
    test(file_path='../data/day16_test.str')
    # main(file_path='../data/day15_input.str')
