import re


class PositionalData:
    row_pos: int = 0
    start_pos: int = 0
    end_pos: int = 0

    def __init__(self, row_pos, start_pos, end_pos):
        self.row_pos = row_pos
        self.start_pos = start_pos
        self.end_pos = end_pos


class NumberData(PositionalData):
    value: str

    def __init__(self, value, row_pos, start_pos, end_pos):
        super().__init__(row_pos, start_pos, end_pos)
        self.value = value

    def __repr__(self):
        return f'({self.value}: {self.row_pos}, {self.start_pos}, {self.end_pos})'

    def is_in_range(self, special_char_data_list: list['SpecialCharData']):
        for datum in special_char_data_list:
            if self.start_pos - 1 <= datum.start_pos <= self.end_pos:
                return True
        return False

    def counts(self, special_char_data: list['SpecialCharData'], max_pos: int):
        counts = False
        if self.row_pos != 0:
            counts |= self.is_in_range([d for d in special_char_data if d.row_pos == self.row_pos - 1])
        if self.row_pos < max_pos:
            counts |= self.is_in_range([d for d in special_char_data if d.row_pos == self.row_pos + 1])
        counts |= self.is_in_range([d for d in special_char_data if d.row_pos == self.row_pos])
        return counts


class SpecialCharData(PositionalData):
    def __init__(self, row_pos, start_pos, end_pos):
        super().__init__(row_pos, start_pos, end_pos)

    def __repr__(self):
        return f'({self.row_pos}, {self.start_pos}, {self.end_pos})'

    def get_nb_in_range(self, nb_data: list['NumberData']):
        nb_in_range = []
        for datum in nb_data:
            for pos in range(datum.end_pos - datum.start_pos):
                if self.start_pos - 1 <= datum.start_pos + pos <= self.end_pos:
                    nb_in_range.append(datum.value)
                    break
        return nb_in_range

    def gear_ratio(self, nb_data: list['NumberData'], max_pos: int) -> int:
        nb_in_range = []
        if self.row_pos != 0:
            nb_in_range += self.get_nb_in_range([d for d in nb_data if d.row_pos == self.row_pos - 1])
        if self.row_pos < max_pos:
            nb_in_range += self.get_nb_in_range([d for d in nb_data if d.row_pos == self.row_pos + 1])
        nb_in_range += self.get_nb_in_range([d for d in nb_data if d.row_pos == self.row_pos])

        if len(nb_in_range) == 2:
            return nb_in_range[0] * nb_in_range[1]
        else:
            return 0


def build_data_classes(line: str, line_number: int, v2: bool = False):
    nb_data_list = []
    char_data_list = []
    number_or_char_pattern = r'([0-9]+)|([^\.^\s])'
    matches = re.finditer(number_or_char_pattern, line)
    for match in matches:
        if match is None:
            return [], []

        match_value = match.group()
        if match_value.isdigit():
            nb_data_list.append(NumberData(int(match_value), line_number, *match.span()))
        elif v2 and match_value == '*':
            char_data_list.append(SpecialCharData(line_number, *match.span()))
        else:
            char_data_list.append(SpecialCharData(line_number, *match.span()))

    return nb_data_list, char_data_list


def build_numbers_that_count(numbers: list[NumberData], chars: list[SpecialCharData], max_pos: int) -> list:
    numbers_that_count = []
    for n_data in numbers:
        if n_data.counts(chars, max_pos):
            numbers_that_count.append(n_data.value)
    return numbers_that_count


def premier_exercice() -> int:
    numbers = []
    chars = []
    with open('input.txt', 'r') as input_file:
        for line_number, input_line in enumerate(input_file):
            n_list, char_list = build_data_classes(input_line, line_number)
            numbers += n_list
            chars += char_list

    numbers_that_count = build_numbers_that_count(numbers, chars, line_number)
    return sum(numbers_that_count)


def build_gear_ratios(numbers: list[NumberData], chars: list[SpecialCharData], max_pos: int) -> list[int]:
    gear_ratios = []
    for c_data in chars:
        gear_ratios.append(c_data.gear_ratio(numbers, max_pos))
    return gear_ratios


def second_exercice() -> int:
    numbers = []
    chars = []
    with open('input.txt', 'r') as input_file:
        for line_number, input_line in enumerate(input_file):
            n_list, char_list = build_data_classes(input_line, line_number, v2=True)
            numbers += n_list
            chars += char_list

    gear_ratios = build_gear_ratios(numbers, chars, line_number)
    return sum(gear_ratios)


if __name__ == '__main__':
    print('------------------ JOUR 3 ------------------')
    print(f'Résultat du premier exercice : {premier_exercice()}')
    print(f'Résultat du second exercice : {second_exercice()}')
