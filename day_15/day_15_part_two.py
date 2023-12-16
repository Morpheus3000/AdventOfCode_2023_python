from tqdm import tqdm


def load_data(data_path):

    lines = [x.strip() for y in open(data_path, 'r').readlines() for x in
             y.split(',')]
    print('[I] Found %d lines!' % len(lines))
    return lines


def hash_algorithm(tgt_str):
    cur_val = 0
    elements = list(tgt_str)
    for e in elements:
        cur_val = ((cur_val + ord(e)) * 17) % 256
    return cur_val


def main(file_path):
    data = load_data(file_path)
    running_total = sum([hash_algorithm(x) for x in tqdm(data)])
    print('[I] Final total is: ', running_total)


if __name__ == '__main__':
    # main(file_path='../data/day15_test.str')
    main(file_path='../data/day15_input.str')
