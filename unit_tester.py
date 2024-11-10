import pytest
import os

from egg_roll import Level, game_state

global debug, text_based
debug, text_based = False, False

'''
Expected Syntax:

test_level = Level(grid, limits)
test_level_map = test_level.grid
test_level_moves = test_level.limit
test_level_rows = test_level.rows
test_level_cols = test_level.cols
test_level_print = str(test_level)

file_name = valid_level_file.xx
with open(file_name, encoding='utf-8') as level_file:
    level_file_Level, list_of_moves_made, total_points = game_state(level_file)
'''

#UNIT TESTS HERE
test_cases = os.listdir("./unit_testing")

assert 1 == 1