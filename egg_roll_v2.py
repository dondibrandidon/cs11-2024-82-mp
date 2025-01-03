import os
import subprocess
import sys
import time
from copy import deepcopy
from dataclasses import dataclass, astuple
from io import TextIOWrapper


@dataclass
class TileSet:
    """This stores the characters used to process `grid` in
    :class:`~egg_roll_v2.Level`."""
    egg_key: str
    grass_key: str
    wall_key: str
    pan_key: str
    empty_key: str
    full_key: str
    magic_key: str


class Level:
    """This class is the model handling all logic involving the grid.
    Each instance generates with the following attributes:

    :param grid: The grid of tiles to be processed
    :type grid: tuple[tuple[str, ...], ...]

    :ivar grid: The 2D matrix filled with string representing the tiles
    :vartype grid: list[list[str]]
    :ivar rows: The number of rows of the grid
    :vartype rows: int
    :ivar cols: The maximum row length of the grid
    :vartype cols: int
    :ivar key: The :class:`~egg_roll_v2.TileSet`
               of the characters used by `grid`
    :vartype key: :class:`~egg_roll_v2.TileSet`
    :ivar eggs: The mutable array of egg coordinates in the grid
    :vartype eggs: list[tuple[int, int]]
    :ivar gaps: The immutable array of all gap coordinates in a non-square grid
    :vartype gaps: tuple[tuple[int, int]]

    :raises ValueError: Raised for grids that don't follow a
                        :class:`~egg_roll_v2.TileSet`
    """

    emoji_set: TileSet = TileSet(
        egg_key='🥚',
        grass_key='🟩',
        wall_key='🧱',
        pan_key='🍳',
        empty_key='🪹',
        full_key='🪺',
        magic_key='✨',
        )
    ascii_set: TileSet = TileSet(
        egg_key='0',
        grass_key='.',
        wall_key='#',
        pan_key='P',
        empty_key='O',
        full_key='@',
        magic_key='*',
        )
    sea_set: TileSet = TileSet(
        egg_key='⛵',
        grass_key='🟦',
        wall_key='🌴',
        pan_key='🌀',
        empty_key='🪹',
        full_key='🪺',
        magic_key='☁️',
        )
    #: This is the set of all allowed :class:`~egg_roll_v2.TileSet` .
    themes: tuple[TileSet, TileSet, TileSet] = (emoji_set, ascii_set, sea_set)
    #: This dictionary converts character directions to coordinate increments.
    freedom: dict[str, tuple[int, int]] = {
        'f': (-1, 0),
        'b': (1, 0),
        'r': (0, 1),
        'l': (0, -1),
        }

    def __init__(
            self,
            grid: tuple[tuple[str, ...], ...],
            ) -> None:
        """This initializes all of the attributes of
        the :class:`~egg_roll_v2.Level` instance.

        :param grid: The grid of tiles to be processed
        :type grid: tuple[tuple[str, ...], ...]

        :raises ValueError: Raised for grids that don't follow a
                            :class:`~egg_roll_v2.TileSet`
        """
        self.grid: list[list[str]] = list(
            list(char for char in row if char != '\n')
            for row in grid
            )

        self.rows: int = len(self.grid)
        self.cols: int = max(len(row) for row in self.grid)

        tiles: set[str] = set(char for row in self.grid for char in row)
        # This checks for the right TileSet:
        for theme in Level.themes:
            if all(
                    tile in astuple(theme)
                    for tile in tiles
                    if tile != ' '
                    ):
                hold_key: TileSet = theme
        try:
            self.key: TileSet = hold_key
        except NameError:
            raise ValueError(f"Invalid map! *{tiles=}")

        self.eggs: list[tuple[int, int]] = []
        gaps_holder: list[tuple[int, int]] = []
        # This traverses the grid to populate eggs and gaps:
        for i in range(self.rows):
            for j in range(self.cols):
                try:
                    if any(
                            self.grid[i][j] == theme.egg_key
                            for theme in Level.themes
                            ):
                        self.eggs.append((i, j))
                    elif self.grid[i][j] == ' ':
                        gaps_holder.append((i, j))
                except IndexError:
                    gaps_holder.append((i, j))
        self.gaps = tuple(gaps_holder)
        super().__init__()

    def __str__(self) -> str:
        """This returns a string with the format:
        "str_row_0\nstr_row_1\n...str_row_n"
        """
        return '\n'.join(tuple(''.join(row) for row in self.grid))

    def get_grid(self) -> list[list[str]]:
        return self.grid

    def get_rows(self) -> int:
        return self.rows

    def get_cols(self) -> int:
        return self.cols

    def get_key(self) -> TileSet:
        return self.key

    def _outside(self, i: int, j: int) -> bool:
        """Given coordinates i and j,
        returns whether (i, j) is within `grid`, zero-indexed.

        :param i: The row index
        :type i: int
        :param j: The column index
        :type j: int
        :return: Returns whether (i, j) is within `grid`
        :rtype: bool
        """
        return (
            ((i, j) in self.gaps)
            or not (0 <= i < self.get_rows() and 0 <= j < self.get_cols())
            )

    def tilt(self, degree: str, moves_left: int
             ) -> tuple[list[str], int, tuple[str, ...], bool]:
        """The main logical interaction with the player!
        Simulates a tilting of the board, which usually moves `eggs`.

        :param degree: A character in "fbrl" which determines direction.
        :type degree: str
        :param moves_left: Moves :class:`~egg_roll_v2.Player` has left,
                           used to calculate points.
        :type moves_left: int

        :raises ValueError: Raised when :param: degree is not in "fbrl."

        :return: Returns debugging logs, points gained or lost, array
                 for grid animation, and whether there are any `eggs` left.
        :rtype: tuple[list[str], int, tuple[str], bool]
        """

        try:
            i_velocity, j_velocity = Level.freedom[degree.lower()]
        except KeyError:
            raise ValueError(f"Level.tilt received {degree}")

        debug_logs: list[str] = []
        increment_points: int = 0
        energy: int = 0 if moves_left == -1 else int(moves_left)
        tweens: list[str] = [str(self)]  # used to animate the eggs rolling

        roll_eggs: list[tuple[int, int]]
        # This is done to prevent multiple eggs in one tile:
        if degree in "fl":
            roll_eggs = sorted(self.eggs)
        else:
            roll_eggs = sorted(self.eggs)[::-1]

        # All `eggs` are set to "roll" in `roll_eggs` at first.
        # The `tilt` action is then considered finished
        # once all the `eggs` have "stopped" (no more eggs in `rolls_eggs`).
        wall_eggs: list[tuple[int, int]] = []

        while roll_eggs:
            for (i, j) in tuple(roll_eggs):
                debug_logs.extend([
                    f"# {i}, {j} -> {i+i_velocity}, {j+j_velocity}",
                    f"# {roll_eggs=}, {wall_eggs=}, {self.gaps=}",
                    f"# {self} #",
                    ])

                if (
                        self._outside(i+i_velocity, j+j_velocity)
                        or (i+i_velocity, j+j_velocity) in wall_eggs
                        or (i+i_velocity, j+j_velocity) in self.gaps
                        or (
                            self.grid[i+i_velocity][j+j_velocity]
                            in self.key.wall_key + self.key.full_key
                            )
                        ):
                    roll_eggs.remove((i, j))
                    wall_eggs.append((i, j))
                elif (
                        self.grid[i+i_velocity][j+j_velocity]
                        in self.key.pan_key
                        ):
                    roll_eggs.remove((i, j))
                    self.grid[i][j] = self.key.grass_key
                    increment_points -= 5
                elif (
                        self.grid[i+i_velocity][j+j_velocity]
                        in self.key.empty_key
                        ):
                    roll_eggs.remove((i, j))
                    self.grid[i][j] = self.key.grass_key
                    self.grid[i+i_velocity][j+j_velocity] = (
                        self.key.full_key
                        )
                    increment_points += 10 + energy
                else:
                    roll_eggs.remove((i, j))
                    self.grid[i][j] = self.key.grass_key
                    roll_eggs.append((i+i_velocity, j+j_velocity))
                    self.grid[i+i_velocity][j+j_velocity] = (
                        self.key.egg_key
                        )
            tweens.append(str(self))

        if degree in "fl":
            self.eggs = sorted(wall_eggs)
        elif degree in "br":
            self.eggs = sorted(wall_eggs)[::-1]

        return debug_logs, increment_points, tuple(tweens), not self.eggs


class Player:
    """This class is the controller and view handling the gameplay.

    :param level_file: The level file to be read and processed
    :type level_file: TextIOWrapper
    :param freedom: The dictionary defining accepted inputs,
                    defaults to example control scheme ("fFbBrRlL").
    :type freedom: dict[str, str], optional
    :param is_debug: Makes debugging more convenient if True,
                        defaults to False
    :type is_debug: bool, optional

    :ivar degrees: This turns the player input into the characters
                   :func:`~egg_roll_v2.Level.tilt` can process
    :vartype degrees: dict[str, str]
    :ivar valids: String containing all valid inputs from `degrees`
    :vartype valids: str
    :ivar file_name: The name of the level file
    :vartype file_name: str
    :ivar moves_left: Decrements with each successful
                      character or "undo" input, treated as
                      infinite if set to -1
    :vartype moves_left: int
    :ivar max_moves: The number of moves prescribed in level file
    :vartype max_moves: int
    :ivar current_level: The main Level instance interacted with
    :vartype current_level: :class: Level
    :ivar points: All points gained by so far
    :vartype points: int
    :ivar game_end: Starts False, the Game Over screen is displayed once True
    :vartype game_end: bool
    :ivar past_moves: Array of symbols to denote past successful inputs
    :vartype past_moves: list[str]
    :ivar past_levels: Array of past :class:`~egg_roll_v2.Level`
                       states for undo-ing
    :vartype past_levels: list[Level]
    :ivar past_points: Array of past points for undo-ing
    :vartype past_points: list[int]
    :ivar current_input: The input for processing to
                         :func:`~egg_roll_v2.Level.tilt`
    :vartype current_input: str
    :ivar debug: Enables printing of debug info and disables
                 `time.sleep()` if True
    :vartype debug: bool

    :raises ValueError: Raised for :class:`~egg_roll_v2.Level` with `grid`
                        that doesn't follow a :class:`~egg_roll_v2.TileSet`
    """

    name_to_char: dict[str, str] = {
        'forward': 'f',
        'backward': 'b',
        'rightward': 'r',
        'leftward': 'l',
    }
    char_to_name: dict[str, str] = {
        'f': 'forward',
        'b': 'backward',
        'r': 'rightward',
        'l': 'leftward',
    }
    char_to_symbol: dict[str, str] = {
        'f': '↑',
        'b': '↓',
        'r': '→',
        'l': '←',
    }

    def __init__(
            self,
            level_file: TextIOWrapper,
            freedom: dict[str, str] = {
                "forward": 'fF',
                "backward": 'bB',
                "rightward": 'rR',
                "leftward": 'lL,'
                },
            is_debug: bool = False
            ) -> None:
        """This initializes all of the attributes of
        the :class:`~egg_roll_v2.Player` instance.

        :param level_file: The level file to be read and processed
        :type level_file: TextIOWrapper
        :param freedom: The dictionary defining accepted inputs,
                        defaults to example control scheme ("fFbBrRlL").
        :type freedom: dict[str, str], optional
        :param is_debug: Makes debugging more convenient if True,
                            defaults to False
        :type is_debug: bool, optional

        :raises ValueError: Raised for :class:`~egg_roll_v2.Level` with `grid`
                            that doesn't follow a :class:`~egg_roll_v2.TileSet`
        """
        num_of_rows: int = int(level_file.readline())
        moves_left_holder: str = level_file.readline().strip('\n')
        grid = tuple(
            tuple(str(level_file.readline()).strip('\n'))
            for i in range(num_of_rows)
            )

        self.degrees: dict[str, str] = {
            char: Player.name_to_char[key]
            for key, value
            in freedom.items()
            for char
            in value
        }
        self.valids: str = ''.join(freedom.values())
        self.file_name: str = level_file.name
        self.moves_left: int = (
            -1 if moves_left_holder == "inf"
            else int(moves_left_holder)
            )
        self.max_moves: int = int(self.moves_left)
        try:
            self.current_level: Level = Level(grid)
        except ValueError:
            raise ValueError(
                'Invalid level! '
                'Please choose a different level_file.in...'
                )
        self.points: int = 0
        self.game_end: bool = (self.moves_left == 0)
        self.current_input: tuple[str, ...] = ()
        self.debug: bool = is_debug
        self.past_moves: list[str] = []

        # Variables for undo processing:
        self.past_levels: list[Level] = [deepcopy(self.current_level)]
        self.past_points: list[int] = [self.points]
        super().__init__()

    def _set_current_input(self) -> None:
        """This prints the prompt asking for user input."""
        try:
            self.current_input = tuple(
                str(char)
                for char
                in input(colored("Next move/s:", attrs=["reverse"]) + ' ')
                )
        except NameError:
            self.current_input = tuple(
                str(char)
                for char
                in input("Next move/s: ")
                )
        return None

    def _exit_scenario(self) -> None:
        """This is for the scenario of an `exit` input.
        Simple sets `game_end` to True.
        """
        self.game_end = True
        return None

    def _undo_scenario(self) -> None:
        """This is for the scenario for an `undo` input.
        Note that the last state saved is the current state.

        If there are past states to undo to,
        this method sets the second to the last
        :class:`~egg_roll_v2.Level` and `int`
        in `past_levels` and `past_points`
        to be `current_level` and the current `points`,
        respectively.
        """
        if len(self.past_levels) > 1:
            self.past_moves.append('⎌')
            ghost_grid: list[str] = str(self.past_levels.pop()).split('\n')
            self.current_level = deepcopy(self.past_levels[-1])
            self.past_points.pop()
            self.points = self.past_points[-1]
            self.moves_left -= 1 if self.moves_left > 0 else 0

            for i in range(self.current_level.get_rows()+1):
                if self.debug:  # debug info
                    print(f"# {i=}")

                clear_screen(self.debug)
                print("<Undoing...>")
                print()

                for _ in range(i):
                    print(
                        self.current_level.get_key().magic_key
                        * self.current_level.get_cols()
                        )
                for k in range(i, self.current_level.get_rows()):
                    if self.debug:  # debug info
                        print(f"# {k=}")

                    print(ghost_grid[k])

                # Makes animation go faster for levels with more rows:
                time.sleep(
                    (1/self.current_level.get_rows())
                    * (not self.debug)
                    )
        else:
            print("You can't go back any further...")
            time.sleep(2 * (not self.debug))
        return None

    def _character_scenario(self, char: str) -> None:
        """This is for all other input scenarios.

        This class treats all input not `exit` nor `undo` as a series
        of multiple character inputs, which this methods processes.

        :param char: Character to be cross-checked with :ivar: degrees
        :type char: str
        """
        if self.debug:  # debug info
            print(f"# Input to process: {char}")

        if char in self.valids:
            self.past_moves.append(
                Player.char_to_symbol[self.degrees[char]])

            debug_logs: list[str]
            temp_points: int
            wowaka: tuple[str, ...]
            debug_logs, temp_points, wowaka, self.game_end = (
                self.current_level.tilt(self.degrees[char], self.moves_left))

            if self.debug:  # debug info
                for log in debug_logs:
                    print(log)

            if len(wowaka) > 1:
                wowaka = wowaka[:-1]  # Removes buffer for multi-frame tilts

            for frame in wowaka:
                clear_screen(self.debug)
                print(
                    f'<Tilting '
                    f'{Player.char_to_name[self.degrees[char]]}...>')
                print()
                print(frame)
                time.sleep(0.3 * (not self.debug))

            if self.debug:
                print(f"temp_points: {temp_points}")

            self.points += temp_points
            self.moves_left -= 1 if self.moves_left > 0 else 0

            clear_screen(self.debug)

            self.past_levels.append(deepcopy(self.current_level))
            self.past_points.append(self.points)
        return None

    def _print_interface(self) -> None:
        """This handles printing of the main user interface:

            1. The level file name currently being played
            2. The actual :class:`~egg_roll_v2.Level` grid of tiles
            3. The controls as are in `degrees`, as well as `undo` and `exit`
            4. The moves made so far
            5. The number of moves left
            6. The points collected so far
        """
        print("<Currently playing from level file: ", end='')
        try:
            print(colored(f"{self.file_name}", attrs=["reverse"]), end='')
        except NameError:
            print((self.file_name), end='')
        print('>')
        print()

        print(self.current_level)
        print()

        print("Controls:")
        for arrow in Player.char_to_name:
            sub_valids = ''.join(
                char for char in self.degrees
                if self.degrees[char] == arrow)
            print(
                f"> Use any of ['{sub_valids}']"
                f" to tilt the board {Player.char_to_name[arrow]}")
        print()
        print(
            "> [\"Undo\"] to use energy to undo last move",
            "> [\"Exit\"] to quit this level",
            sep="\n")
        print()

        if self.past_moves:
            print(f"Moves made so far: {', '.join(self.past_moves)}")
        else:
            print("Moves made so far: None")

        print("Energy left: ", end='')
        try:
            if self.moves_left == -1:
                print(colored("∞", "red"))
            elif self.moves_left == 1:
                print(colored(self.moves_left, "red"))
            elif self.moves_left <= self.max_moves//2:
                print(colored(self.moves_left, "yellow"))
            else:
                print(colored(self.moves_left, "green"))
        except NameError:
            if self.moves_left == -1:
                print("∞")
            else:
                print(self.moves_left)

        print(f"Points collected: {self.points}")
        self._set_current_input()
        return None

    def _game_over(self) -> None:
        """This handles the printing of the Game Over screen."""
        print("[!!!]")
        print()
        print(str(self.current_level))
        time.sleep(0.5 * (not self.debug))  # Short lag to make end less abrupt

        clear_screen(self.debug)
        print("<Game Over>")
        print()

        print(str(self.current_level))
        print()

        if self.past_moves:
            print(f"Moves made: {', '.join(self.past_moves)}")
        else:
            print("Moves made: None")

        print("Final Score: ", end='')

        if not self.points:
            print('0')
        try:
            print(colored(self.points, "green" if self.points > 0 else "red"))
        except NameError:
            print(self.points)
        print()

        return None

    def get_state(self) -> tuple[Level, tuple[str, ...], int]:
        """Can be used to check the effects of the following
        :func:`~egg_roll_v2.Player.start_playing` function
        without having to wait for the return once the game is over.

        :return: Returns the current values of
                 `current_level`, `past_moves`, and `points`
        :rtype: tuple[Level, tuple[str, ...], int]
        """
        return self.current_level, tuple(self.past_moves), self.points

    def start_playing(self) -> tuple[Level, tuple[str, ...], int]:
        """This where the main handling of all gameplay displays happens!

        :return: Returns from self.get_state
        :rtype: tuple[Level, tuple[str, ...], int]
        """
        while not self.game_end and self.moves_left != 0:
            if self.debug:  # debug info
                print("# Start of Undo Check")
                for i in range(len(self.past_levels)):
                    print(self.past_levels[i])
                    print(self.past_points[i])
                    print()
                print("# End of Undo Check")

            clear_screen(self.debug)
            self._print_interface()
            if self.debug:  # debug info
                print(f"self._print_interface() updated {self.current_input=}")

            clear_screen(self.debug)
            if ''.join(self.current_input).lower() == 'exit':
                self._exit_scenario()
            elif ''.join(self.current_input).lower() == 'undo':
                self._undo_scenario()
            else:
                for char in self.current_input:
                    self._character_scenario(char)

        clear_screen(self.debug)
        self._game_over()
        return self.get_state()


def clear_screen(is_debug: bool = False) -> None:
    """This is a standalone method for
    clearing the terminal screen, if any.

    :param is_debug: Disables clear_screen action if True, defaults to False
    :type is_debug: bool, optional
    """
    if not is_debug:
        print()  # Newline to handle prints that don't end on line breaks
        if sys.stdout.isatty():
            clear_cmd: str = 'cls' if os.name == 'nt' else 'clear'
            try:
                subprocess.run([clear_cmd])
            except Exception:
                os.system(clear_cmd)
    else:
        print("# clear_screen called")  # debug info


def argument_handling() -> None:
    """This is a standalone function for handling file arguments.

    Uses default ("fFbBrRlL") controls and
    does not support highscores functionality from :class:`~menu_v2.Menu`.
    """
    print("<Welcome to EGG ROLL II!>")
    print()
    try:
        while True:
            with open(sys.argv[1], encoding='utf-8') as level_file:
                try:
                    game_state: Player = Player(
                        level_file,
                        is_debug=debug,
                        )

                    game_state.start_playing()

                except FileNotFoundError:
                    print(
                        'File argument invalid!'
                        'Please open game with valid file location...'
                        )
                    print()
                    return None

                repeat: str = input(
                    'Type [Yes] to replay level, else exit game: '
                    )
                if repeat.lower() == 'yes':
                    continue
                else:
                    break
        print()
        print(
            '<'
            'Thank you for playing egg_roll.py by '
            'Martin Mendoza (2024-10322) & Brandon Sayo (2024-05352)!\n'
            'extended to 2.0 by '
            'Brandon Sayo (2024-05352)'
            '>'
            )
        print()
    except IndexError:
        print(
            'No file argument! '
            'Please open file with valid file location argument...'
            )
    except Exception as e:
        print(f"Unexpected exception: {e}")


if __name__ == '__main__':
    debug = False

    if debug:  # debug info
        print("# egg_roll.py DEBUG IS ON")

    try:
        # "type: ignore"-ed since no mypy support
        from termcolor import colored  # type: ignore
        if debug:  # debug info
            print("# termcolor loaded")
    except ImportError:
        if debug:  # debug info
            print("# termcolor NOT loaded")
        pass

    argument_handling()
