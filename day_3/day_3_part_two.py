import re
import math


def find_all_occurences_indices(main_string, tgt_string):
    last_start = 0
    ret = 0
    all_indices = []
    while ret != -1:
        ret = main_string.find(tgt_string, last_start)
        if ret != -1:
            last_start = ret + 1
            all_indices.append(ret)
    all_indices.sort()

    return all_indices

def find_attached_num(tgt_str, probe_idx):
    l_len = len(tgt_str)
    tgt_dig = tgt_str[probe_idx]
    digits = [tgt_dig]
    if not tgt_dig.isnumeric():
        return 0

    dig = '0'
    # Scan right
    start_idx = probe_idx
    while dig.isnumeric():
        start_idx += 1
        dig = tgt_str[start_idx]
        digits.append(dig)

    # Scan left
    dig = '0'
    start_idx = probe_idx
    while dig.isnumeric():
        start_idx -= 1
        dig = tgt_str[start_idx]
        digits.insert(0, dig)
    digits = int(''.join(digits[1:-1]))

    return digits

def main(file_path):
    # Patching because scanning expects '.' to be the last character. Otherwise
    # need more complicated scan logic.
    lines = ['.' + x.strip() + '.' for x in open(file_path, 'r').readlines()]
    print('[I] Found %d lines!' % len(lines))
    running_total = 0
    unique_sym = {}
    for i, l in enumerate(lines):
        filter_splits = [re.sub(r'[0-9]+', '', x) for x in l.split('.') if len(x) > 0 and not
                         x.isnumeric()]
        if len(filter_splits) > 0:
            for sym in filter_splits:
                if sym == '*':
                    idx = find_all_occurences_indices(l, sym)
                    unique_sym[i] = idx

    # Assuming the first and last line never has any symbols in them.
    for l_idx, star_idx in unique_sym.items():
        for ind in star_idx:
            adj_nums = []

            tgt_l = lines[l_idx]
            num = find_attached_num(tgt_l, ind - 1)
            adj_nums.append(num)
            num = find_attached_num(tgt_l, ind + 1)
            adj_nums.append(num)


            tgt_l = lines[l_idx - 1]
            mid_num = find_attached_num(tgt_l, ind)
            if mid_num == 0:
                left_num = find_attached_num(tgt_l, ind - 1)
                right_num = find_attached_num(tgt_l, ind + 1)
                adj_nums.append(left_num)
                adj_nums.append(right_num)
            else:
                adj_nums.append(mid_num)


            tgt_l = lines[l_idx + 1]
            mid_num = find_attached_num(tgt_l, ind)
            if mid_num == 0:
                left_num = find_attached_num(tgt_l, ind - 1)
                right_num = find_attached_num(tgt_l, ind + 1)
                adj_nums.append(left_num)
                adj_nums.append(right_num)
            else:
                adj_nums.append(mid_num)

            adj_nums = [x for x in adj_nums if x != 0]

            if len(adj_nums) == 2:
                running_total += math.prod(adj_nums)

    print('[I] Final total is: ', running_total)


if __name__ == '__main__':
    # main(file_path='../data/day3_test.str')
    main(file_path='../data/day3_input.str')
