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

def this_is_true():
    assert True

def this_is_false():
    assert False

this_is_true()
this_is_false()

#UNIT TESTS HERE
test_cases_dir = "./unit_testing"
test_cases = os.listdir(test_cases_dir)

@pytest.mark.parametrize("test_file", test_cases)
def test_edge_case(test_file):
    
    file_path = os.path.join(test_cases_dir, test_file)

    with open(file_path, encoding='utf-8') as level_file:
        try:
            level, moves, points = egg_roll.game_state(level_file)
        except Exception as e:
            pytest.fail(f"Test {test_file} failed with error: {e}")

        # Example assertions (modify these based on expected results for each file)
        assert isinstance(level, egg_roll.Level), f"Level instance not returned for {test_file}"
        assert isinstance(moves, list), f"Moves not returned as a list for {test_file}"
        assert isinstance(points, int), f"Points not returned as an integer for {test_file}"

# Output the test case files (for debugging purposes)
print(f"Loaded test cases: {test_cases}")
