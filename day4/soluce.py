import re
from pprint import pprint


def get_winning_numbers(input_line) -> list[str]:
    game_pattern = r'^Card\s+\d+:([\s+\d+]+) \|([\s+\d+]+)'
    match = re.search(game_pattern, input_line)
    if match is None:
        return []

    winning_numbers = []
    card_numbers, played_numbers = match.groups()
    card_numbers = card_numbers
    played_numbers = played_numbers
    for number in played_numbers.split():
        if number in card_numbers.split():
            winning_numbers.append(number)
    return winning_numbers


def compute_points(winning_numbers: list[str]):
    nb_win_numbers = len(winning_numbers)
    if nb_win_numbers == 0:
        return 0
    else:
        return 2 ** (nb_win_numbers - 1)


def premier_exercice() -> int:
    winning_numbers_list = []
    with open('input.txt', 'r') as input_file:
        for input_line in input_file:
            n = get_winning_numbers(input_line)
            winning_numbers_list.append(n)

    points = [compute_points(winning_numbers) for winning_numbers in winning_numbers_list]
    return sum(points)


def second_exercice() -> int:
    nb_card_by_card_id = {}
    with open('input.txt', 'r') as input_file:
        for line_num, input_line in enumerate(input_file):
            if nb_card_by_card_id.get(line_num) is None:
                nb_card_by_card_id[line_num] = 1

            winning_numbers = get_winning_numbers(input_line)
            for i in range(line_num + 1, line_num + 1 + len(winning_numbers)):
                for _ in range(nb_card_by_card_id.get(line_num)):
                    nb_card_by_card_id[i] = nb_card_by_card_id.get(i, 1) + 1

    return sum([v for v in nb_card_by_card_id.values()])


if __name__ == '__main__':
    print('------------------ JOUR 4 ------------------')
    print(f'Résultat du premier exercice : {premier_exercice()}')
    print(f'Résultat du second exercice : {second_exercice()}')
