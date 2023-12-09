def main(file_path):

    lines = [x.strip() for x in open(file_path, 'r').readlines()]
    print('[I] Found %d lines!' % len(lines))
    running_total = 0
    for i, l in enumerate(lines):
        print('Processing line %d...' % i, end='')
        num_list = [int(x) for x in list(l) if x.isnumeric()]
        # Because it is always a 2 digit number
        num = num_list[0] * 10 + num_list[-1]
        print('done!')
        print('\t[*] %s -> %d' % (l, num))
        running_total += num

    print('[I] Final total is: ', running_total)


if __name__ == '__main__':
    main(file_path='../data/day1_input.str')
