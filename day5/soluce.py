import re
from typing import Tuple


def build_seeds_and_maps(input_file) -> Tuple[list, dict]:
    seeds = []
    delimiter_pattern = r'([a-z|\-]+) map'
    maps_by_type = {}
    current_map = ''
    for line_num, input_line in enumerate(input_file):
        if line_num == 0:
            seeds = input_line.split()[1:]
        else:
            delimiter_match = re.match(delimiter_pattern, input_line)
            if delimiter_match is not None:
                current_map = delimiter_match.group()
                maps_by_type[current_map] = []
            else:
                values = input_line.split()
                if values:
                    maps_by_type[current_map].append(list(map(int, values)))
    return seeds, maps_by_type


def get_min_seed_position(seeds: list, maps_by_type: dict) -> int:
    postions = []
    for seed in seeds:
        next_val = int(seed)
        for _, maps in maps_by_type.items():
            for map_values in maps:
                dest_pos = map_values[0]
                src_pos = map_values[1]
                map_range = map_values[2]
                if next_val < src_pos or src_pos + map_range <= next_val:
                    # Check other maps
                    continue
                elif src_pos <= next_val < src_pos + map_range:
                    next_val = dest_pos + (next_val - src_pos)
                    break
        postions.append(next_val)
    return min(postions)


def premier_exercice() -> int:
    with open('input.txt', 'r') as input_file:
        seeds, maps_by_type = build_seeds_and_maps(input_file)

    return get_min_seed_position(seeds, maps_by_type)


def transform_seeds(seeds: list):
    seed_ranges_raw = [seeds[i:i + 2] for i in range(0, len(seeds), 2)]
    return [(int(s[0]), int(s[0]) + int(s[1])) for s in seed_ranges_raw]


def get_seed_positions_v2(seed_range: list, maps: dict) -> list[tuple[int, int]]:
    matched_ranges = []
    for (dest_pos, src_start, map_range) in maps:
        src_end = src_start + map_range
        unmatched_ranges = []
        while seed_range:
            seed_start, seed_end = seed_range.pop()
            # Interval
            before_match_range = (seed_start, min(seed_end, src_start))
            intersecting_range = (max(seed_start, src_start), min(src_end, seed_end))
            after_match_range = (max(src_end, seed_start), seed_end)
            if before_match_range[1] > before_match_range[0]:
                unmatched_ranges.append(before_match_range)
            if intersecting_range[1] > intersecting_range[0]:
                matched_ranges.append((intersecting_range[0] - src_start + dest_pos,
                                       intersecting_range[1] - src_start + dest_pos))
            if after_match_range[1] > after_match_range[0]:
                unmatched_ranges.append(after_match_range)
        seed_range = unmatched_ranges
    return seed_range + matched_ranges


def second_exercice() -> int:
    with open('input.txt', 'r') as input_file:
        seeds, maps_by_type = build_seeds_and_maps(input_file)

    position_ranges = []
    seed_ranges = transform_seeds(seeds)
    for seed_range in seed_ranges:
        seed_range = [seed_range]
        for _, maps in maps_by_type.items():
            seed_range = get_seed_positions_v2(seed_range, maps)
        position_ranges.append(min(seed_range)[0])
    return min(position_ranges)


if __name__ == '__main__':
    print('------------------ JOUR 5 ------------------')
    print(f'Résultat du premier exercice : {premier_exercice()}')
    print(f'Résultat du second exercice : {second_exercice()}')
