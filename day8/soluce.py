import math
import re
from itertools import cycle


class Path:
    origin: str
    dest: dict[str, str]

    def __init__(self, origin: str, dest: dict[str, str]):
        self.origin = origin
        self.dest = dest

    def __repr__(self):
        return f"{self.origin} => ({self.dest.get('L')}, {self.dest.get('R')})"


def get_paths(path_pattern: str, paths_str: list[str]) -> list[Path]:
    paths = []
    for path in paths_str:
        m = re.match(path_pattern, path)
        if m is not None:
            origin = m.group(1)
            dest_str = m.group(2)
            left, right = dest_str.split(', ')
            dest = {'L': left, 'R': right}
            paths.append(Path(origin, dest))
    return paths


def premier_exercice() -> int:
    with open('input.txt', 'r') as input_file:
        lines = [line for line in input_file.read().strip().split('\n') if line != '']

    instructions = lines[0]
    paths_str = lines[1:]
    path_pattern = r'([A-Z]{3}) = \(([A-Z]{3}\, [A-Z]{3})\)'
    paths = get_paths(path_pattern, paths_str)

    first_path = [path for path in paths if path.origin == 'AAA'][0]

    end_of_path = False
    nb_step = 0
    while not end_of_path:
        current_path = first_path
        for instruction in cycle(instructions):
            new_origin = current_path.dest.get(instruction)
            current_path = [path for path in paths if path.origin == new_origin][0]
            nb_step += 1
            if new_origin == 'ZZZ':
                end_of_path = True
                break
    return nb_step


def second_exercice() -> int:
    with open('input.txt', 'r') as input_file:
        lines = [line for line in input_file.read().strip().split('\n') if line != '']

    instructions = lines[0]
    paths_str = lines[1:]
    path_pattern = r'([0-9A-Z]{3}) = \(([0-9A-Z]{3}\, [0-9A-Z]{3})\)'
    paths = get_paths(path_pattern, paths_str)
    first_paths = [path for path in paths if path.origin[2] == 'A']

    end_indexes = []
    for path in first_paths:
        end_index = 0
        for end_index, instruction in enumerate(cycle(instructions)):
            new_origin = path.dest.get(instruction)
            path = [path for path in paths if path.origin == new_origin][0]
            if path.origin[2] == 'Z':
                break
        end_indexes.append(end_index + 1)
    return math.lcm(*end_indexes)


if __name__ == '__main__':
    print('------------------ JOUR 8 ------------------')
    print(f'Résultat du premier exercice : {premier_exercice()}')
    print(f'Résultat du second exercice : {second_exercice()}')
