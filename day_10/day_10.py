from tqdm import tqdm
import numpy as np


def pretty_print(l):
    [print(x) for x in l]

# Assuming (0, 0) to be top-left.
# Add sub category with input direction, to determine the output directions.
# Maybe a lambda function?
# map_dict = {
#     '|': (1, 0),
#     '-': (0, 1),
#     'L': (1, 1),
#     'J': (1, -1),
#     '7': (-1, -1),
#     'F': (-1, 1),
# }

map_movement_dict = {
    '|': lambda x, d: ([x[0] + 1, x[1]], 'd') if d else ([x[0] - 1, x[1]], 'u'),
    '-': lambda x, d: ([x[0], x[1] + 1], 'r') if d else ([x[0], x[1] - 1], 'l'),
    'L': lambda x, d: ([x[0], x[1] + 1], 'r') if d else ([x[0] - 1, x[1]], 'u'),
    'J': lambda x, d: ([x[0], x[1] - 1], 'l') if d else ([x[0] - 1, x[1]], 'u'),
    '7': lambda x, d: ([x[0], x[1] - 1], 'l') if d else ([x[0] + 1, x[1]], 'd'),
    'F': lambda x, d: ([x[0], x[1] + 1], 'r') if d else ([x[0] + 1, x[1]], 'd'),
}

# Possible connections based on incoming movements
valid_con_dict = {
    'r': ['-', '7', 'J'],
    'l': ['-', 'F', 'L'],
    'u': ['|', '7', 'F'],
    'd': ['|', 'J', 'L']
}

sym_direction_dict = {
    '|': {
        'd': True,
        'u': False
    },
    '-': {
        'r': True,
        'l': False
    },
    'L': {
        'd': True,
        'l': False
    },
    'J': {
        'd': True,
        'r': False
    },
    '7': {
        'u': True,
        'r': False
    },
    'F': {
        'u': True,
        'l': False
    },
}


def print_map(grid):
    print(len(grid))
    all_rows = [''.join(x) for x in grid]
    str_map = '\n'.join(all_rows)
    print(str_map)


def check_direction(cur_coord, prev_coord):
    # Movement is only in 4 directions. No diagonal movement.
    # u -> up
    # d -> down
    # r -> right
    # l -> left
    # n -> no movement

    c_y, c_x = cur_coord
    p_y, p_x = prev_coord

    y_diff = p_y - c_y
    x_diff = p_x - c_x

    if x_diff == 0:
        if y_diff > 0:
            mv = 'u'
        elif y_diff < 0:
            mv = 'd'
        else:
            mv = 'n'

    if y_diff == 0:
        if x_diff > 0:
            mv = 'l'
        elif x_diff < 0:
            mv = 'r'
        else:
            mv = 'n'

    return mv


def get_connecting_neighbours(grid, tgt_idx):
    valid_connections = []

    probe_y = tgt_idx[0] - 1
    probe_x = tgt_idx[1]

    if grid[probe_x][probe_y] != '.' and\
       grid[probe_x][probe_y] != 'S':
        valid_connections.append({
            'coord': [probe_y, probe_x],
            'direction': -1,
        })

    probe_y = tgt_idx[0]
    probe_x = tgt_idx[1] + 1

    if grid[probe_x][probe_y] != '.' and\
       grid[probe_x][probe_y] != 'S':
        valid_connections.append({
            'coord': [probe_y, probe_x],
            'direction': 1,
        })

    probe_y = tgt_idx[0] + 1
    probe_x = tgt_idx[1]

    if grid[probe_x][probe_y] != '.' and\
       grid[probe_x][probe_y] != 'S':
        valid_connections.append({
            'coord': [probe_y, probe_x],
            'direction': 1,
        })

    probe_y = tgt_idx[0]
    probe_x = tgt_idx[1] - 1

    if grid[probe_x][probe_y] != '.' and\
       grid[probe_x][probe_y] != 'S':
        valid_connections.append({
            'coord': [probe_y, probe_x],
            'direction': -1,
        })

    return valid_connections


def test():
    prev_coord = [2, 1]
    sym = '-'
    cur_coord = [1, 1]

    mv = check_direction(cur_coord, prev_coord)
    print(mv)


def traversal_logic(grid, cur_coord, cur_mv):
    print('in logic')
    cur_y, cur_x = cur_coord
    cur_op = grid[cur_y][cur_x]
    direc = sym_direction_dict[cur_op][cur_mv]
    # print(cur_op, cur_mv, direc)
    next_coord, nex_mv = map_movement_dict[cur_op](cur_coord,
                                           direc)
    nex_y, nex_x = next_coord
    nex_op = grid[nex_y][nex_x]
    # print(cur_coord, next_coord, nex_op)
    if nex_op in valid_con_dict[nex_mv]:
        # nex_mv = check_direction(next_coord, cur_coord)
        return {
            'coord': next_coord,
            'mov': nex_mv
        }
    else:
        return None


def main(file_path):
    lines = [x.strip() for x in open(file_path, 'r').readlines()]
    print('[I] Found %d lines!' % len(lines))
    running_total = 0
    grid = [[x.strip() for x in l] for i, l in enumerate(lines)]
    # for i, l in tqdm(enumerate(lines), total=len(lines)):
    # for i, l in enumerate(lines):
    #     grid.append([x.strip() for x in l])

    # pretty_print(grid)
    print_map(grid)
    start_idx = [(i, x.index('S')) for i, x in enumerate(grid) if 'S' in x][0]
    print(start_idx)
    grid_size = [len(grid), len(grid[0])]
    start_connections = get_connecting_neighbours(grid, start_idx)
    print('Start connections: ', start_connections)
    print('Grid size: ', grid_size)

    print('[I] Traversing grid...')

    prev_coord = start_connections[0]['coord']

    step_cnt = 0
    cur_coord = start_idx
    nex_coord = start_connections[0]['coord']
    cur_mv = check_direction(nex_coord, cur_coord)

    cur_y, cur_x = cur_coord
    nex_y, nex_x = nex_coord
    print('Start info: ', end='')
    print(cur_coord, nex_coord, cur_mv)
    print('Syms: %s, %s, (%s)' % (
        grid[cur_y][cur_x], grid[nex_y][nex_x], cur_mv
    ))

    cur_coord = nex_coord

    for i in range(8):
        print('-' * 20)
        next_dict = traversal_logic(grid, cur_coord, cur_mv)
        if next_dict is not None:
            nex_coord = next_dict['coord']
            nex_mv = next_dict['mov']
            cur_y, cur_x = cur_coord
            nex_y, nex_x = nex_coord
            print('Start info: ', end='')
            print(cur_coord, nex_coord, cur_mv)
            print('Syms: %s, %s, (%s)' % (
                grid[cur_y][cur_x], grid[nex_y][nex_x], cur_mv
            ))

            cur_coord = nex_coord
            cur_mv = nex_mv

        else:
            print('Deadend!')
    # while True:
    #     y, x = prev_coord
    #     op = grid[y][x]
    #     if op != '.' and op != 'S':
    #         next_coord = map_dict[op](prev_coord, True)
    #         print(prev_coord, next_coord)
    #         mv = check_direction(next_coord, prev_coord)
    #         prev_coord = next_coord

    #         y, x, = prev_coord
    #         op = grid[y][x]
    #         print(op)
    #         next_coord = map_dict[op](prev_coord, sym_direction_dict[op][mv])
    #         print(mv)
    #         print(next_coord)
    #     break

        


    # print('[I] Final total is: ', running_total)

    # grid_vis = np.zeros(grid_size)
    # [print('-' * grid_size[0]) for x in range(grid_size[1])]


if __name__ == '__main__':
    # test()
    main(file_path='../data/day10_test.str')
    # main(file_path='../data/day10_test2.str')
    # main(file_path='../data/day10_input.str')
