import math
from tqdm import tqdm


def main(file_path):
    lines = [x.strip() for x in open(file_path, 'r').readlines()]
    print('[I] Found %d lines!' % len(lines))
    running_total = 0
    times = int(''.join(
        [x.strip() for x in lines[0].split(':')[-1].strip().split(' ') if
         len(x.strip()) > 0]
    ))
    dist = int(''.join(
        [x.strip() for x in lines[1].split(':')[-1].strip().split(' ') if
         len(x.strip()) > 0]
    ))

    for hold_t in tqdm(range(times), total=times):
        dist_trav = hold_t * (times - hold_t)
        if dist_trav > dist:
            running_total += 1

    print('Total time: ', times)
    print('Record distance: ', dist)
    print('[I] Final total is: ', running_total)


if __name__ == '__main__':
    main(file_path='../data/day6_input.str')

