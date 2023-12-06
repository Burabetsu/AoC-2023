import math


def nb_winning_races(total_time, record_distance):
    sol1 = ((total_time + ((total_time ** 2 - 4 * record_distance) ** (1 / 2))) / 2 - 0.05)
    sol2 = ((total_time - ((total_time ** 2 - 4 * record_distance) ** (1 / 2))) / 2 + 0.05)
    return math.floor(sol1) - math.ceil(sol2) + 1


def premier_exercice() -> int:
    with open('input.txt', 'r') as input_file:
        lines = input_file.read().strip().split('\n')

        times = [value for value in lines[0].split(' ')[1:] if value != '']
        distances = [value for value in lines[1].split(' ')[1:] if value != '']

        nb_possible_record = 1
        for i in range(len(times)):
            nb_possible_record *= nb_winning_races(int(times[i]), int(distances[i]))

    return nb_possible_record


def second_exercice() -> int:
    with open('input.txt', 'r') as input_file:
        lines = input_file.read().strip().split('\n')

        times = [value for value in lines[0].split(' ')[1:] if value != '']
        time = ''
        for t in times:
            time += t

        distances = [value for value in lines[1].split(' ')[1:] if value != '']
        distance = ''
        for d in distances:
            distance += d

        return nb_winning_races(int(time), int(distance))


if __name__ == '__main__':
    print('------------------ JOUR 6 ------------------')
    print(f'Résultat du premier exercice : {premier_exercice()}')
    print(f'Résultat du second exercice : {second_exercice()}')
