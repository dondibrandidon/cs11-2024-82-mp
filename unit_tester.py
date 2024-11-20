import pytest
import os
import egg_roll

global debug, text_based
debug, text_based = False, False

'''
Expected Syntax:

test_level = egg_roll.Level(grid, limits)

if character in "fFbBrRlL":
    new_grid, temporary_points, animation, is_over = current_level.tilt(character)

file_name = valid_location/level_file.in
with open(file_name, encoding='utf-8') as level_file:
    level_file_Level, list_of_moves_made, total_points = egg_roll.game_state(level_file)
'''

#UNIT TESTS HERE
test_cases = os.listdir("./unit_testing")

assert 1 == 1