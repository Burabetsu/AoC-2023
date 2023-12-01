import re


def get_calibration_value(pattern: str, line: str) -> int:
    matches = re.findall(pattern, line)
    if len(matches) == 0:
        return 0
    return int(matches[0] + matches[-1])


def premier_exercice() -> int:
    total = 0
    with open('input.txt', 'r') as input_file:
        for input_line in input_file:
            total += get_calibration_value('([1-9])', input_line)
    return total


def get_calibration_value_v2(pattern: str, line: str) -> int:
    help_dict = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
    }
    matches = re.findall(pattern, line)
    if len(matches) == 0:
        return 0

    res = int(help_dict.get(matches[0], matches[0]) + help_dict.get(matches[-1], matches[-1]))
    return res


def second_exercice() -> int:
    total = 0
    with open('input.txt', 'r') as input_file:
        for input_line in input_file:
            total += get_calibration_value_v2('(?=([1-9]|one|two|three|four|five|six|seven|eight|nine))', input_line)
    return total


if __name__ == '__main__':
    print('------------------ JOUR 1 ------------------')
    print(f'Résultat du premier exercice : {premier_exercice()}')
    print(f'Résultat du second exercice : {second_exercice()}')
