def process_record(game_rec):
    rec_splits = game_rec.split(':')
    game_id = int(rec_splits[0].split(' ')[-1])

    game_sets = rec_splits[-1].split(';')

    game_rec_dict = {
        'id': game_id,
        'blue': 0,
        'green': 0,
        'red': 0,
    }

    for s in game_sets:
        csv = s.strip().split(',')
        for c in csv:
            num_splits = c.strip().split(' ')
            num_cubes = int(num_splits[0])
            if game_rec_dict[num_splits[1]] < num_cubes:
                game_rec_dict[num_splits[1]] = num_cubes

    return game_rec_dict


def main(file_path):

    bag_total = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }

    lines = [x.strip() for x in open(file_path, 'r').readlines()]
    print('[I] Found %d lines!' % len(lines))
    running_total = 0
    for i, l in enumerate(lines):
        print('Processing line %d...' % (i + 1), end='')
        game_rec = process_record(l)
        print('done!')
        if game_rec['blue'] <= bag_total['blue'] and\
           game_rec['green'] <= bag_total['green'] and\
           game_rec['red'] <= bag_total['red']:
            running_total += game_rec['id']

    print('[I] Final total is: ', running_total)


if __name__ == '__main__':
    main(file_path='../data/day2_input.str')
