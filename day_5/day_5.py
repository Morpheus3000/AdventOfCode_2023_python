def main(file_path):
    lines = [x.strip() for x in open(file_path, 'r').readlines()]
    print('[I] Found %d lines!' % len(lines))
    running_total = 0
    for i, l in enumerate(lines):
        print('Processing line %d...' % (i + 1), end='')

        print('done!')
        print('\t[*] %s -> %d' % (l, num))
        running_total += num

    print('[I] Final total is: ', running_total)


if __name__ == '__main__':
    main(file_path='../data/day5_test.str')
