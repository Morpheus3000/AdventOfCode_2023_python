import math
from tqdm import tqdm


def main(file_path):
    lines = [x.strip() for x in open(file_path, 'r').readlines()]
    print('[I] Found %d lines!' % len(lines))
    running_total = 0
    times = [int(x.strip()) for x in lines[0].split(':')[-1].strip().split(' ') if len(x.strip()) > 0]
    dist = [int(x.strip()) for x in lines[1].split(':')[-1].strip().split(' ') if len(x.strip()) > 0]

    win_prob = [0 for x in range(len(times))]
    for i, t in tqdm(enumerate(times), total=len(times)):
        tgt_dist = dist[i]
        valid_hold = 0
        for hold_t in tqdm(range(t), total=t, leave=False):
            dist_trav = hold_t * (t - hold_t)
            if dist_trav > tgt_dist:
                valid_hold += 1
        win_prob[i] = valid_hold

    print(times)
    print(dist)
    print(win_prob)
    running_total = math.prod(win_prob)
    print('[I] Final total is: ', running_total)


if __name__ == '__main__':
    # main(file_path='../data/day6_test.str')
    main(file_path='../data/day6_input.str')
