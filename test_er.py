import pytest
import os       # for file handling
import sys, io  # for overloading print and input
from egg_roll import Level, game_state


# EXPECTED INPUTS AND OUTPUTS
'''
test_level = Level(grid, moves_left)

if character in 'fFbBrRlL':
    increment_points, animation, no_eggs = current_level.tilt(character, moves_left)

file_name = valid_location/level_file.in
with open(file_name, encoding='utf-8') as level_file:
    level_file_Level, list_of_moves_made, total_points = game_state(level_file)
'''

#-------------------------------------------START OF TESTS------------------------------------------------#

# Expected file format for _test_Level_tilt (".|unit_testing|test_Level_tilt|file.in"):
'''
level_rows: int
moves_left: int
row_1: str <input level>
row_2: str
...
row_level_rows: str
valid_character_input: str (character_input validation happens in game_state)
row_1 <expected output level>
row_2
...
row_level_rows 
expected_points: int
expected_no_eggs: bool (int: 0 or 1)
'''
@pytest.mark.parametrize("test_file", [file for file in os.listdir("." + os.sep + "unit_testing" + os.sep + "_test_Level_Tilt")])
def test_Level_tilt(test_file):
    with open("." + os.sep + "unit_testing" + os.sep + "_test_Level_tilt" + os.sep + test_file, encoding='utf-8') as level_file:
        level_rows = int(level_file.readline())
        moves_left = int(level_file.readline())
        ini_grid = tuple(list(level_file.readline()) for i in range(level_rows))

        test_level = Level(ini_grid, moves_left)

        character_input = str(level_file.readline()).strip('\n')

        fin_grid = list(list(tile for tile in level_file.readline() if tile != '\n') for i in range(level_rows))
        expected_points = int(level_file.readline())
        expected_no_eggs = int(level_file.readline())

        increment_points, animation, no_eggs = test_level.tilt(character_input, moves_left)

        assert fin_grid == test_level.get_grid()
        assert expected_points == increment_points
        assert expected_no_eggs == no_eggs


# Expected file format for _test_game_state (".|unit_testing|_test_game_state|file.in"):
'''
level_rows: int
moves_left: int
row_1: str <input level>
row_2: str
...
row_level_rows: str
string_input: str <IMPORTANT: len(string_input) >= moves_left>
row_1 <expected output level>
row_2
...
row_level_rows 
expected_move_list: list[str]
expected_total_points: int
'''
@pytest.mark.parametrize("test_file", [file for file in os.listdir("." + os.sep + "unit_testing" + os.sep + "_test_game_state")])
def test_game_state(test_file):
    level_path = "." + os.sep + "unit_testing" + os.sep + "_test_game_state" + os.sep + test_file
    with open(level_path, encoding='utf-8') as level_file:
        sys.stdin = io.StringIO(level_file.readline())
        final_state, moves_made, total_points = game_state(level_file, 0)
        
        fin_grid = list(list(tile for tile in level_file.readline() if tile != '\n') for i in range(final_state.rows))
        expected_move_list = str(level_file.readline()).strip('\n')
        expected_total_points = int(level_file.readline())

        assert fin_grid == final_state.grid
        assert expected_move_list == ''.join(moves_made)
        assert expected_total_points == total_points


#-------------------------------------------FOR NON-PYTEST TESTING------------------------------------------------#
def main():
    sys.stdout = io.StringIO() #THIS DISABLES PRINTS

    for test_file in [file for file in os.listdir("." + os.sep + "unit_testing" + os.sep + "_test_Level_tilt")]:
        test_Level_tilt(test_file)

    for test_file in [file for file in os.listdir("." + os.sep + "unit_testing" + os.sep + "_test_game_state")]:
        test_game_state(test_file)

if __name__ == '__main__':
    main()