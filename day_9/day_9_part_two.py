from tqdm import tqdm


def calculate_diff_pyramid(sequences):
    diffs = [sequences[-1]]
    d = [j - i for i, j in zip(sequences[:-1], sequences[1:])]
    diffs.append(d[-1])
    sum_d = sum(d)
    while True:
        d = [j - i for i, j in zip(d[:-1], d[1:])]
        diffs.append(d[-1])
        sum_d = set(d)
        if sum_d == {0}:
            break

    return diffs


def test_case():
    # test_seq = [6, 30, 78, 166, 318, 581, 1054, 1938, 3622, 6826, 12819, 23717,
    #       42864, 75377, 129249, 218254, 369843, 645270, 1187135, 2324466,
    #       ]
    gt = 4792495
    test_seq = [-2, 10, 35, 81, 159, 279, 443, 635, 813, 920, 961, 1273, 3310,
                11699, 39236, 118346, 326191, 837605, 2032938, 4710820, ]
    gt = 10495116
    diff = calculate_diff_pyramid(test_seq)
    pred_val = sum(diff)

    print('Input: ', test_seq)
    print('Diff: ', diff)
    print('Pred Val: ', pred_val)
    print('GT: ', gt)


def verify(file_path):
    lines = [x.strip() for x in open(file_path, 'r').readlines()]
    print('[I] Found %d lines!' % len(lines))
    running_total = 0
    correct = 0

    for i, l in enumerate(lines):
        orig_seq = [int(x.strip()) for x in l.strip().split(' ')]
        orig_seq.reverse()
        gt = orig_seq[-1]
        seq = orig_seq[:-1]
        diff = calculate_diff_pyramid(seq)
        pred_val = sum(diff)
        if pred_val != gt:
            print('[!] Prediction not matching gt for entry %d! Debug below' %
                 i)
            print('[I] Orig sequence: ', orig_seq)
            print('[I] Input sequence: ', seq)
            print('[I] Pred: %d, GT: %d' % (pred_val, gt))
            break
        else:
            print('[I] Verfied %d/%d: ' % (i + 1, len(lines)), end='\r')

        running_total += pred_val


def main(file_path):
    lines = [x.strip() for x in open(file_path, 'r').readlines()]
    print('[I] Found %d lines!' % len(lines))
    running_total = 0

    for i, l in tqdm(enumerate(lines), total=len(lines)):
        seq = [int(x.strip()) for x in l.strip().split(' ')]
        seq.reverse()
        diff = calculate_diff_pyramid(seq)
        pred_val = sum(diff)
        running_total += pred_val

    print('[I] Final total is: ', running_total)


if __name__ == '__main__':
    # test_case()
    main(file_path='../data/day9_test.str')
    # verify(file_path='../data/day9_input.str')
    # main(file_path='../data/day9_input.str')

