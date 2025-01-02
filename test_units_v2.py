import pytest
import os
import sys
import io
from egg_roll_v2 import Level, Player


# EXPECTED INPUTS AND OUTPUTS

# test_level: Level = Level(grid: tuple[tuple[str, ...], ...], move_limit: int)

# if character in 'fFbBrRlL':
#     debug_logs: list[str]
#     temporary_points: int
#     animation_frames: list[str]
#     eggs_are_left: bool
#     debug_logs, temporary_points, animation_frames, eggs_are_left = (
#         self.current_level.tilt(
#                                 char: str,
#                                 moves_left: int,
#                                 )
#         )

# file_name = *|valid_location|level_file.in
# with open(file_name, encoding='utf-8') as level_file:
#     game_state = Player(level_file, is_debug=True)
#     level_file_Level, list_of_moves_made, total_points = (
#         game_state.start_playing(level_file))


# Expected file format for test_Level_tilt file
# (".|unit_testing|test_Level_tilt|file.in"):
'''
level_rows: int
moves_left: int
row_1: str                 # the initial grid state
row_2: str
...
row_n: str
valid_character_input: str # validation happens in game_state not here
row_1: str                 # the expected final state
row_2: str
...
row_n: str
expected_points: int
expected_no_eggs: 0 | 1    # acts as bool
'''


@pytest.mark.parametrize(
        "test_file",
        [
            file
            for file
            in os.listdir(
                "."
                + os.sep + "unit_testing"
                + os.sep + "test_Level_Tilt"
                )
        ]
    )
def test_Level_tilt(test_file: str) -> None:
    with open(
            (
                "."
                + os.sep + "unit_testing"
                + os.sep + "test_Level_tilt"
                + os.sep + test_file
            ),
            encoding='utf-8'
            ) as level_file:
        level_rows = int(level_file.readline())
        moves_left = int(level_file.readline())
        ini_grid = tuple(
            tuple(str(level_file.readline()).strip('\n'))
            for i in range(level_rows)
            )

        test_level = Level(ini_grid)

        character_input = str(level_file.readline()).strip('\n')

        fin_grid = list(
            list(
                tile
                for tile
                in level_file.readline()
                if tile != '\n'
                )
            for i
            in range(level_rows)
        )
        expected_points = int(level_file.readline())
        expected_no_eggs = int(level_file.readline())

        debug_logs, increment_points, animation, no_eggs = (
            test_level.tilt(character_input, moves_left))

        assert fin_grid == test_level.get_grid()
        assert expected_points == increment_points
        assert expected_no_eggs == no_eggs


# Expected file format for test_Player_start_playing file
# (".|unit_testing|test_Player_start_playing|file.in"):
'''
string_input: str
level_rows: int
moves_left: int
row_1: str                 # the initial grid state
row_2: str
...
row_n: str
row_1: str                 # the expected final state
row_2: str
...
row_n: str
expected_moves: str
expected_total_points: int
'''


@pytest.mark.parametrize(
        "test_file",
        [
            file
            for file
            in os.listdir(
                "."
                + os.sep + "unit_testing"
                + os.sep + "test_Player_start_playing"
                )
        ]
    )
def test_Player_start_playing(test_file: str) -> None:
    level_path = (
        "."
        + os.sep
        + "unit_testing"
        + os.sep
        + "test_Player_start_playing"
        + os.sep
        + test_file
    )
    with open(level_path, encoding='utf-8') as level_file:
        sys.stdin = io.StringIO(level_file.readline().replace(',', '\n'))
        try:
            game_state: Player = Player(level_file, is_debug=True)
            final_state, moves_made, total_points = (
                game_state.start_playing())
        except EOFError:
            final_state, moves_made, total_points = (
                game_state.get_state())

            # raise ValueError(
            #     '`sum(char for char in string_input char in "fFbBrRlL") '
            #     '>= moves_left` was not met'
            # )

        fin_grid = list(
            list(
                tile
                for tile
                in level_file.readline()
                if tile != '\n'
            )
            for i
            in range(final_state.rows))
        expected_moves = str(level_file.readline()).strip('\n')
        expected_total_points = int(level_file.readline())

        assert fin_grid == final_state.grid
        assert expected_moves == ''.join(moves_made)
        assert expected_total_points == total_points


def main() -> None:
    for test_file in [
            file
            for file
            in os.listdir(
                "."
                + os.sep + "unit_testing"
                + os.sep + "test_Level_tilt")]:
        test_Level_tilt(test_file)

    for test_file in [
            file
            for file
            in os.listdir(
                "."
                + os.sep + "unit_testing"
                + os.sep + "test_Player_start_playing")]:
        test_Player_start_playing(test_file)


if __name__ == '__main__':
    main()
