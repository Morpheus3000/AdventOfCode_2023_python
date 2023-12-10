def main(file_path):
    lines = [x.strip() for x in open(file_path, 'r').readlines()]
    print('[I] Found %d lines!' % len(lines))
    running_total = 0
    for i, l in enumerate(lines):
        # print('Processing line %d...' % (i + 1), end='')

        num_list = l.split(':')[-1].strip().split('|')
        winning_num = [int(x.strip()) for x in num_list[0].strip().split(' ')
                       if len(x) > 0]
        scratch_num = [int(x.strip()) for x in num_list[1].strip().split(' ')
                       if len(x) > 0]

        common_num = list(set(winning_num).intersection(scratch_num))

        if len(common_num) > 0:
            num = 1
        else:
            num = 0
        for n in common_num[1:]:
            num *= 2

        # print('done!')
        # print('\t[*] %s -> %d' % (l, num))
        running_total += num

    print('[I] Final total is: ', running_total)


if __name__ == '__main__':
    # main(file_path='../data/day4_test.str')
    main(file_path='../data/day4_input.str')
