def next_value(oasis_values: list[int], v2=False):
    next_values = []
    for i in range(len(oasis_values) - 1):
        next_values.append(oasis_values[i + 1] - oasis_values[i])
    if any(value != 0 for value in next_values):
        if v2:
            return oasis_values[0] - next_value(next_values, v2)
        else:
            return oasis_values[-1] + next_value(next_values, v2)
    else:
        if v2:
            return oasis_values[0] - next_values[0]
        else:
            return next_values[-1] + oasis_values[-1]


def premier_exercice() -> int:
    with open('input.txt', 'r') as input_file:
        lines = [line for line in input_file.read().strip().split('\n') if line != '']

    oasis_values_list = [list(map(int, line.split())) for line in lines]
    res = 0
    for oasis_values in oasis_values_list:
        res += next_value(oasis_values)

    return res


def second_exercice() -> int:
    with open('input.txt', 'r') as input_file:
        lines = [line for line in input_file.read().strip().split('\n') if line != '']

    oasis_values_list = [list(map(int, line.split())) for line in lines]
    res = 0
    for oasis_values in oasis_values_list:
        res += next_value(oasis_values, v2=True)

    return res


if __name__ == '__main__':
    print('------------------ JOUR 8 ------------------')
    print(f'Résultat du premier exercice : {premier_exercice()}')
    print(f'Résultat du second exercice : {second_exercice()}')
