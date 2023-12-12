from itertools import cycle
from tqdm import tqdm


def main(file_path):
    lines = [x.strip() for x in open(file_path, 'r').readlines() if
             len(x.strip()) > 0]
    print('[I] Found %d lines!' % len(lines))
    running_total = 0
    inst = [0 if x == 'L' else 1 for x in list(lines[0])]

    print('[I] Instruction set: ', lines[0])
    print('[I] Instruction set: ', inst)
    graph_map = {}
    # for i, l in tqdm(enumerate(lines[1:]), total=len(lines)):
    for i, l in enumerate(lines[1:]):
        sp = l.split('=')
        orig = sp[0].strip()
        L, R = sp[1].strip().split(',')
        L = L.strip()[1:]
        R = R.strip()[:-1]

        graph_map[orig] = [L, R]

    start_locs = [x for x in graph_map.keys() if x[-1] == 'A']
    print('[I] Starting nodes: ', start_locs)
    print('[I] Num nodes: ', len(start_locs))
    # Explore path
    path_config = cycle(inst)

    tgt_choices = []

    for s in start_locs:
        tgt_choices.append(graph_map[s])

    for p in path_config:
        locs = []
        for tgt_choice in tgt_choices:
            locs.append(tgt_choice[p])
        running_total += 1
        end_char = [x[2] for x in locs]
        if 'Z' in end_char:
            print(' ' * 100)
            print(end_char)
        else:
            print(locs, end='\r')
        if set(end_char) == {'Z'}:
            break

        tgt_choices = []
        for l in locs:
            tgt_choices.append(graph_map[l])

    print('[I] Final end nodes: ', locs)
    print('[I] Num end nodes: ', len(locs))
    print('[I] Final total is: ', running_total)


if __name__ == '__main__':
    # main(file_path='..\data\day8_test_part_two.str')
    main(file_path='../data/day8_input.str')
