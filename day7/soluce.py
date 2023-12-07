import copy
from typing import Tuple

CARD_ORDER_v1 = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
CARD_ORDER_v2 = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']


def build_hands_and_bids() -> Tuple[list[str], list[str]]:
    with open('input.txt', 'r') as input_file:
        hands = []
        bids = []
        for _, input_line in enumerate(input_file):
            input_line = input_line.strip()
            hands.append(input_line.split(' ')[0])
            bids.append(input_line.split(' ')[1])
    return hands, bids


class Hand:
    index: int
    content: str
    score: int

    def __init__(self, index: int, content: str, score: int):
        self.index = index
        self.content = content
        self.score = score

    def __gt__(self, other_hand):
        if self.score > other_hand.score:
            return 1
        elif self.score < other_hand.score:
            return 0
        else:
            return self.better_content(other_hand)

    def __repr__(self):
        return f'HAND {self.index} : {self.content}'

    def better_content(self, other_hand):
        for i, char in enumerate(self.content):
            if CARD_ORDER_v1.index(char) == CARD_ORDER_v1.index(other_hand.content[i]):
                other_hand_copy = copy.deepcopy(other_hand)
                other_hand_copy.content = other_hand_copy.content[1:]
                self_copy = copy.deepcopy(self)
                self_copy.content = self_copy.content[1:]
                return self_copy.better_content(other_hand_copy)
            else:
                return CARD_ORDER_v1.index(char) > CARD_ORDER_v1.index(other_hand.content[i])


def build_cards_scores(hands_str) -> list[Hand]:
    hands = []
    # Know how to score hands
    nb_cards_by_card = []
    for _, hand in enumerate(hands_str):
        nb_card_by_card = {}
        index = 0
        for card in hand:
            nb_card_by_card.setdefault(card, 0)
            if card in hand:
                if nb_card_by_card.get(card) is not None:
                    nb_card_by_card[card] += 1
            index += 1
        nb_cards_by_card.append(nb_card_by_card)

    # Score hands
    for index, nb_card_by_card in enumerate(nb_cards_by_card):
        nb_diff_card = len(nb_card_by_card.values())
        score = 0
        if nb_diff_card == 1:
            score = 6
        if nb_diff_card == 2:
            if any(v == 4 for v in nb_card_by_card.values()):
                score = 5
            else:
                score = 4
        if nb_diff_card == 3:
            if any(v == 3 for v in nb_card_by_card.values()):
                score = 3
            else:
                score = 2
        if nb_diff_card == 4:
            score = 1
        if nb_diff_card == 5:
            score = 0
        hands.append(Hand(index, hands_str[index], score))

    hands.sort()
    return hands


def premier_exercice() -> int:
    hands, bids = build_hands_and_bids()
    scored_hands = build_cards_scores(hands)

    total_winnings = 0
    for place, hand in enumerate(scored_hands):
        total_winnings += int(bids[hand.index]) * (place + 1)
    return total_winnings


class HandV2(Hand):
    def better_content(self, other_hand):
        for i, char in enumerate(self.content):
            if CARD_ORDER_v2.index(char) == CARD_ORDER_v2.index(other_hand.content[i]):
                other_hand_copy = copy.deepcopy(other_hand)
                other_hand_copy.content = other_hand_copy.content[1:]
                self_copy = copy.deepcopy(self)
                self_copy.content = self_copy.content[1:]
                return self_copy.better_content(other_hand_copy)
            else:
                return CARD_ORDER_v2.index(char) > CARD_ORDER_v2.index(other_hand.content[i])


def get_max_score_keys(nb_card_by_card: dict, max_keys: list[str]) -> list[str]:
    last_max_key = max(nb_card_by_card, key=nb_card_by_card.get)
    max_keys.append(last_max_key)
    nb_card_by_card.pop(last_max_key)
    if nb_card_by_card.get(last_max_key) in nb_card_by_card.values():
        return get_max_score_keys(nb_card_by_card, max_keys)
    else:
        return max_keys


def build_cards_scores_v2(hands_str) -> list[Hand]:
    hands = []
    # Know how to score hands
    nb_cards_by_card = []
    for _, hand in enumerate(hands_str):
        nb_card_by_card = {}
        index = 0
        for card in hand:
            nb_card_by_card.setdefault(card, 0)
            if card in hand:
                if nb_card_by_card.get(card) is not None:
                    nb_card_by_card[card] += 1
            index += 1

        if 'J' in nb_card_by_card.keys() and len(nb_card_by_card.keys()) > 1:
            max_keys = []
            nb_joker = nb_card_by_card.get('J')
            nb_card_by_card.pop('J')
            max_keys = get_max_score_keys(nb_card_by_card.copy(), max_keys)
            nb_card_by_card[max(max_keys, key=CARD_ORDER_v2.index)] += nb_joker
        nb_cards_by_card.append(nb_card_by_card)

    # Score hands
    for index, nb_card_by_card in enumerate(nb_cards_by_card):
        nb_diff_card = len(nb_card_by_card.values())
        score = 0
        if nb_diff_card == 1:
            score = 6
        if nb_diff_card == 2:
            if any(v == 4 for v in nb_card_by_card.values()):
                score = 5
            else:
                score = 4
        if nb_diff_card == 3:
            if any(v == 3 for v in nb_card_by_card.values()):
                score = 3
            else:
                score = 2
        if nb_diff_card == 4:
            score = 1
        if nb_diff_card == 5:
            score = 0
        hands.append(HandV2(index, hands_str[index], score))

    hands.sort()
    return hands


def second_exercice() -> int:
    hands, bids = build_hands_and_bids()
    scored_hands = build_cards_scores_v2(hands)

    total_winnings = 0
    for place, hand in enumerate(scored_hands):
        total_winnings += int(bids[hand.index]) * (place + 1)
    return total_winnings


if __name__ == '__main__':
    print('------------------ JOUR 7 ------------------')
    print(f'Résultat du premier exercice : {premier_exercice()}')
    print(f'Résultat du second exercice : {second_exercice()}')
