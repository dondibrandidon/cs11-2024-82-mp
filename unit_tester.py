import pytest
import os
import sys, io
import egg_roll

global debug, text_based
debug, text_based = False, False

'''
> Expected outputs and inputs:

test_level = egg_roll.Level(grid, limits)

if character in "fFbBrRlL":
    new_grid, increment_points, animation, no_eggs = current_level.tilt(character, moves_left)

file_name = valid_location/level_file.in
with open(file_name, encoding='utf-8') as level_file:
    level_file_Level, list_of_moves_made, total_points = egg_roll.game_state(level_file)
'''

# Start of tests

# Expected file format for _test_Level_Tilt ("./unit_testing/test_Level_Tilt/file.in"):
'''
level_rows: int
moves_left: int
row_1: str <input level>
row_2: str
...
row_level_rows: str
character_input: str
row_1 <expected output level>
row_2
...
row_level_rows 
expected_points: int
expected_no_eggs: bool
'''
#@pytest.mark.parametrize("test_file", [file for file in os.listdir("./unit_testing/_test_Level_Tilt")])
def _test_Level_Tilt(test_file):
    file_path = os.path("./unit_testing/_test_Level_Tilt/" + test_file)
    assert True


# Expected file format for _test_game_state ("./unit_testing/_test_game_state/file.in"):
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
#@pytest.mark.parametrize("test_file", [file for file in os.listdir("./unit_testing/_test_game_state")])
def _test_game_state(test_file):
    file_path = os.path("./unit_testing/_test_game_state/" + test_file)

    #This overrides input() to load expected inputs instead
    sys.stdin = io.StringIO("")
    final_state, moves_made, total_points = egg_roll.game_state(file_path)
    assert True

#input testing
print("Hello world")
def greet():
    print(f"Hello {input()}")
    print(f"Big {input()}")
def main():
    expected_inputs = ("Martin", "balls")
    sys.stdin = io.StringIO('\n'.join(expected_inputs)) # ito gagamitin natin pangtest nung game_state
    greet()
main()