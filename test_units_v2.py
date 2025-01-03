"""The `test_units_v2` module tests the functions with logic
that can be unit tested:
:class:`~egg_roll_v2.Level`'s :func:`~egg_roll_v2.Level.tilt`
and
:class:`~egg_roll_v2.Player`'s :func:`~egg_roll_v2.Player.start_playing`.

To summarize expected inputs and outputs:

For an instance of :class:`~egg_roll_v2.Level`::

    test_level: Level = Level(grid: tuple[tuple[str, ...], ...])

For the use of the :class:`~egg_roll_v2.Level`
function :func:`~egg_roll_v2.Level.tilt`::

    debug_logs: list[str]           # not checked
    temporary_points: int
    animation_frames: list[str]     # not checked
    eggs_are_left: bool

    char_input: str
    assert char_input in "fblr"

    debug_logs, temporary_points, animation_frames, eggs_are_left = (
        self.test_level.tilt(
                                char: str,
                                moves_left: int,
                                )
        )

For an instance of :class:`~egg_roll_v2.Player`::

    test_file: TextIOWrapper
    game_state: Player = Player(test_file, is_debug=True)

For the use of the :class:`~egg_roll_v2.Player`
function :func:`~egg_roll_v2.Player.start_playing`::

    final_state: Level
    moves_made: tuple[str]
    total_points: int

    final_state, moves_made, total_points = game_state.start_playing()

    # Alternatively for incomplete inputs:
    final_state, moves_made, total_points = game_state.get_state()

As for the actual test functions:
"""

import pytest
import os
import sys
import io
from egg_roll_v2 import Level, Player


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
    """This tests the logic of :class:`~egg_roll_v2.Level` specifically
    with its handling of :func:`~egg_roll_v2.Level.tilt`.

    An example :func:`~egg_roll_v2.Level.tilt` unit test is::

        level_rows: int
        moves_left: int
        row_1: str                    # the initial grid state
        row_2: str
        ...
        row_n: str
        valid_character_input: str    # expects character in "fblr"
        row_1: str                    # the expected final state
        row_2: str
        ...
        row_n: str
        expected_points: int
        expected_no_eggs: 0 | 1       # acts as bool

    :param test_file: The file name of the unit test to be tested
    :type test_file: str
    """
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
    """This tests the logic of :class:`~egg_roll_v2.Player` specifically
    with its handling of :func:`~egg_roll_v2.Player.start_playing`.

    An example :func:`~egg_roll_v2.Player.start_playing` unit test is::

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

    :param test_file: The file name of the unit test to be tested
    :type test_file: str
    """
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
    """This handles non-`pytest` testing."""
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
