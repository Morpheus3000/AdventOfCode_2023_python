from tqdm import tqdm


def check_range(tgt, start, range):
    if tgt > start and tgt < (start + range + 1):
        tgt_idx = tgt - start
        return True, tgt_idx
    return False, -1


def get_location(seed_tgt, almanac, map_list):
    tgt = seed_tgt
    seed_config = {
        'seed': seed_tgt,
    }
    for mp in map_list:
        mp_splits = mp.split('-')
        source = mp_splits[0]
        dest = mp_splits[2]

        sources = almanac[mp]['source']
        dests = almanac[mp]['dest']
        ranges = almanac[mp]['range']

        for s, r, d in zip(sources, ranges, dests):
            ret, tgt_idx = check_range(tgt, s, r)
            if ret:
                dest_start = d
                break

        if ret:
            tgt = dest_start + tgt_idx
        seed_config[dest] = tgt

    return seed_config, seed_config['location']


def main(file_path):
    lines = [x.strip() for x in open(file_path, 'r').readlines() if
             len(x.strip()) > 0]
    print('[I] Found %d lines!' % len(lines))
    running_total = 0
    map_list = []
    almanac = {
        'seeds': [int(x.strip()) for x in
                  lines[0].split(':')[-1].strip().split(' ') if len(x.strip())
                  > 0]
    }
    print('[I] Creating almanac...')
    for l in tqdm(lines[1:]):
        if l[0].isnumeric() == False:
            heading_name = l.split(' ')[0].strip()
            map_list.append(heading_name)
            almanac[heading_name] = {
                'source': [],
                'dest': [],
                'range': [],
            }
        else:
            range_det = [int(x.strip()) for x in l.split(' ') if len(x.strip()) > 0]
            dest_start = range_det[0]
            source_start = range_det[1]
            range_total = range_det[2]
            almanac[heading_name]['source'].append(source_start)
            almanac[heading_name]['dest'].append(dest_start)
            almanac[heading_name]['range'].append(range_total)

    location = []
    print('[I] Mapping seeds...')
    for s in tqdm(almanac['seeds']):
        _, loc = get_location(s, almanac, map_list)
        location.append(loc)

    running_total = min(location)
    print('[I] Final total is: ', running_total)



if __name__ == '__main__':
    # main(file_path='../data/day5_test.str')
    main(file_path='../data/day5_input.str')
