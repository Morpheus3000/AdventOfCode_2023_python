from collections import Counter
from tqdm import tqdm


card_order = ['A', 'K', 'Q', 'J', 'T']
card_order.extend(reversed([str(x) for x in range(2, 10)]))
card_order.reverse()

hand_order = ['5K', '4K', 'FH', '3K', '2P', '1P', 'HC']
hand_order.reverse()


def order_same_hand_type(hands):
    for i in range(5):
        cards = [x[i] for x in hands]
        if len(set(cards)) != 1:
            card_value = [card_order.index(x) for x in cards]
            break
    sorted_hand = [x for _, x in sorted(zip(card_value, hands))]

    return sorted_hand


def rank_hands(hand_type_dict):
    ranked_hand = []
    for h_type, hands in tqdm(hand_type_dict.items()):
        if len(hands) > 0:
            if len(hands) == 1:
                ranked_hand.append(hands[0])
            else:
                sorted_hand = order_same_hand_type(hands)
                for h in sorted_hand:
                    ranked_hand.append(h)
    return ranked_hand


def hand_classifier(hand_config):
    card_count = Counter(hand_config)

    num_keys = card_count.keys()
    num_cards = card_count.values()

    if len(num_keys) == 1:
        return '5K'
    elif len(num_keys) == 5:
        return 'HC'
    elif len(num_keys) == 2:
        if 4 in num_cards:
            return '4K'
        else:
            return 'FH'
    elif len(num_keys) == 3:
        if 3 in num_cards:
            return '3K'
        else:
            return '2P'
    elif len(num_keys) == 4:
        if 2 in num_cards:
            return '1P'
        else:
            return '2P'


def main(file_path):
    lines = [x.strip() for x in open(file_path, 'r').readlines()]
    print('[I] Found %d lines!' % len(lines))
    running_total = 0
    hand_dict = {}
    hand_type_dict = {x: [] for x in hand_order}
    for i, l in tqdm(enumerate(lines), total=len(lines)):
        hand, bid = [x.strip() for x in l.split(' ')]
        hand_type = hand_classifier(hand)
        hand_dict[hand] = {
            'bid': int(bid),
            'class': hand_type,
        }
        hand_type_dict[hand_type].append(hand)

    ranked_hands = rank_hands(hand_type_dict)

    for i, h in enumerate(ranked_hands):
        running_total += hand_dict[h]['bid'] * (i + 1)

    print('[I] Final total is: ', running_total)


if __name__ == '__main__':
    # main(file_path='../data/day7_test.str')
    main(file_path='../data/day7_input.str')
