from itertools import cycle
from tqdm import tqdm


def main(file_path):
    lines = [x.strip() for x in open(file_path, 'r').readlines() if
             len(x.strip()) > 0]
    print('[I] Found %d lines!' % len(lines))
    running_total = 0
    inst = [0 if x == 'L' else 1 for x in list(lines[0])]

    start_loc = 'AAA'
    print('[I] Instruction set: ', lines[0])
    print('[I] Starting node: ', start_loc)
    graph_map = {}
    # for i, l in tqdm(enumerate(lines[1:]), total=len(lines)):
    for i, l in enumerate(lines[1:]):
        sp = l.split('=')
        orig = sp[0].strip()
        L, R = sp[1].strip().split(',')
        L = L.strip()[1:]
        R = R.strip()[:-1]

        graph_map[orig] = [L, R]

    # Explore path
    path_config = cycle(inst)
    tgt_choice = graph_map[start_loc]
    for p in path_config:
        loc = tgt_choice[p]
        running_total += 1
        if loc == 'ZZZ':
            break
        tgt_choice = graph_map[loc]

    print('[I] Final total is: ', running_total)


if __name__ == '__main__':
    main(file_path='../data/day8_test.str')
    main(file_path='../data/day8_test2.str')
    main(file_path='../data/day8_input.str')
