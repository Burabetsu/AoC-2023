import re


def build_ball_by_color(game_results: str) -> dict:
    max_ball_by_color = {}
    draw_regex = r'([0-9]+)\s([a-z]+)'
    for sub_result in game_results.split('; '):
        for draw_item in sub_result.split(', '):
            match_result = re.match(draw_regex, draw_item)
            nb_ball, ball_color = int(match_result.group(1)), match_result.group(2)
            previous_max = max_ball_by_color.setdefault(ball_color, 0)
            max_ball = max(nb_ball, previous_max)
            max_ball_by_color[ball_color] = max_ball
    return max_ball_by_color


def get_game_id_if_possible(line: str, nb_red: int, nb_green: int, nb_blue: int) -> int:
    game_id_pattern = r'Game\s(\d+):\s(.*)'
    match = re.match(game_id_pattern, line)
    if match is None:
        return 0

    game_results = match.group(2)
    max_ball_by_color = build_ball_by_color(game_results)

    too_many_red_balls = max_ball_by_color.get('red', 0) > nb_red
    too_many_green_balls = max_ball_by_color.get('green', 0) > nb_green
    too_many_blue_balls = max_ball_by_color.get('blue', 0) > nb_blue
    if too_many_red_balls or too_many_green_balls or too_many_blue_balls:
        return 0

    game_id = int(match.group(1))
    return game_id


def premier_exercice(nb_red: int, nb_green: int, nb_blue: int) -> int:
    total = []
    with open('input.txt', 'r') as input_file:
        for input_line in input_file:
            total.append(get_game_id_if_possible(input_line, nb_red, nb_green, nb_blue))
    return sum(total)


def get_game_cubes_power(line: str) -> int:
    game_id_pattern = r'Game\s\d+:\s(.*)'
    match = re.match(game_id_pattern, line)
    if match is None:
        return 0

    game_results = match.group(1)
    max_ball_by_color = build_ball_by_color(game_results)

    nb_red = max_ball_by_color.get('red', 0)
    nb_green = max_ball_by_color.get('green', 0)
    nb_blue = max_ball_by_color.get('blue', 0)
    return nb_red * nb_green * nb_blue


def second_exercice() -> int:
    total = []
    with open('input.txt', 'r') as input_file:
        for input_line in input_file:
            total.append(get_game_cubes_power(input_line))
    return sum(total)


if __name__ == '__main__':
    print('------------------ JOUR 2 ------------------')
    print(f'Résultat du premier exercice : {premier_exercice(12, 13, 14)}')
    print(f'Résultat du second exercice : {second_exercice()}')
