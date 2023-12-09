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


def main(file_path):

    lines = [x.strip() for x in open(file_path, 'r').readlines()]
    print('[I] Found %d lines!' % len(lines))
    running_total = 0
    valid_digits = [['one', 1],
                    ['two', 2],
                    ['three', 3],
                    ['four', 4],
                    ['five', 5],
                    ['six', 6],
                    ['seven', 7],
                    ['eight', 8],
                    ['nine', 9],
                    ['1', 1],
                    ['2', 2],
                    ['3', 3],
                    ['4', 4],
                    ['5', 5],
                    ['6', 6],
                    ['7', 7],
                    ['8', 8],
                    ['9', 9]]

    valid_dict = {
        x[0]: [] for x in valid_digits
    }

    # test_str = 'fourseven5seveneightsvtkcjdrfour'
    # all_idx = find_all_occurences_indices(test_str, 'four')
    # print(test_str)
    # print(all_idx)

    for i, l in enumerate(lines):
        print('Processing line %d...' % i, end='')
        first_idx = float('inf')
        last_idx = -1
        first_dig = -1
        last_dig = -1
        for n in valid_digits:
            all_idx = find_all_occurences_indices(l, n[0])
            if len(all_idx) > 0:
                valid_dict[n[0]] = all_idx
                if first_idx > all_idx[0]:
                    first_idx = all_idx[0]
                    first_dig = n[1]
                if last_idx < all_idx[-1]:
                    last_idx = all_idx[-1]
                    last_dig = n[1]
        # Because it is always a 2 digit number
        num = first_dig * 10 + last_dig
        print('done!')
        print('\t[*] %s -> %d' % (l, num))
        running_total += num

    print('[I] Final total is: ', running_total)


if __name__ == '__main__':
    main(file_path='../data/day1_part_two_input.str')

