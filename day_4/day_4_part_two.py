from tqdm import tqdm


def update_card_count(count_dict, card_config):
    for card_id in card_config:
        count_dict['%d' % card_id] += 1
    return count_dict

def main(file_path):
    lines = [x.strip() for x in open(file_path, 'r').readlines()]
    print('[I] Found %d lines!' % len(lines))
    running_total = 0
    card_matches = {}
    cards_won = {}
    for i, l in enumerate(lines):
        # print('Processing line %d...' % (i + 1), end='')

        game_split = l.split(':')
        card_id = game_split[0].split(' ')[-1].strip()
        num_list = game_split[-1].strip().split('|')
        winning_num = [int(x.strip()) for x in num_list[0].strip().split(' ')
                       if len(x) > 0]
        scratch_num = [int(x.strip()) for x in num_list[1].strip().split(' ')
                       if len(x) > 0]

        common_num = list(set(winning_num).intersection(scratch_num))

        card_matches[card_id] = len(common_num)
        cards_won[card_id] = 0

    # Can be solved with recursion, but recursion is messy, can lead to runaway
    # memory and hard to debug. Loop is more controllable and manageable.

    for card_id, num_won in tqdm(card_matches.items()):
        # Update subsequent cards
        start_num = int(card_id)
        end_num = start_num + num_won + 1
        next_cards = list(range(start_num + 1, end_num))
        # Update copies
        num_updates = cards_won[card_id]
        for i in tqdm(range(num_updates), total=num_updates, leave=False):
            cards_won = update_card_count(cards_won, next_cards)

        # Update current copies
        cards_won = update_card_count(cards_won, next_cards)

        # Update original
        cards_won[card_id] += 1

    running_total = sum(cards_won.values())

    print('[I] Final total is: ', running_total)


if __name__ == '__main__':
    # main(file_path='../data/day4_test.str')
    main(file_path='../data/day4_input.str')
