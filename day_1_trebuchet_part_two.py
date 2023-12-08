def main(file_path):

    lines = [x.strip() for x in open(file_path, 'r').readlines()]
    print('[I] Found %d lines!' % len(lines))
    running_total = 0
    valid_digits = ['one', 'two', 'three', 'four', 'five', 'six', 'seven',
                    'eight', 'nine']
    for i, l in enumerate(lines):
        print('Processing line %d...' % i, end='')
        cache = ''
        num_list = []
        for a in list(l):
            if a.isnumeric():
                num_list.append(int(a))
            else:
                cache += a
                if cache in valid_digits:
                    num_list.append(valid_digits.index(cache) + 1)
                    cache = ''

        # Because it is always a 2 digit number
        num = num_list[0] * 10 + num_list[-1]
        print('done!')
        print('\t[*] %s -> %d' % (l, num))
        running_total += num

    print('[I] Final total is: ', running_total)


if __name__ == '__main__':
    main(file_path='data\day1_part_two_test.str')

