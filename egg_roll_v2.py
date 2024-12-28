import os
import subprocess
import sys
import time
from io import TextIOWrapper
from dataclasses import dataclass, astuple
from copy import deepcopy


class Level:
    """This class processes the current level file being played.

    :param grid: _description_
    :type grid: tuple[tuple[str, ...], ...]
    :param limit: _description_
    :type limit: int
    :param rows: _description_
    :type rows: int
    :param cols: _description_
    :type cols: int
    :param key: _description_
    :type key: TileSet
    :param eggs: _description_
    :type eggs: list[tuple[int, int]]
    :param gaps: _description_
    :type gaps: tuple[tuple[int, int]]
    """

    @dataclass
    class TileSet:
        egg_key: str
        grass_key: str
        wall_key: str
        pan_key: str
        empty_key: str
        full_key: str
        magic_key: str

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

    freedom = {'f': (-1, 0), 'b': (1, 0), 'r': (0, 1), 'l': (0, -1)}

    def __init__(self, grid: tuple[tuple[str, ...], ...], max_moves: int,
                 ) -> None:
        self.grid: list[list[str]] = list(
            list(char for char in row if char != '\n') for row in grid
            )
        self.limit: int = int(max_moves)
        self.rows: int = len(self.grid)
        self.cols: int = max(len(row) for row in self.grid)
        self.key: Level.TileSet = (
            Level.emoji_set if any(
                char in astuple(Level.emoji_set)
                for row in self.grid
                for char in row)
            else Level.ascii_set
            )
        """This sets the TileSet depending on the elements found in grid"""
        self.eggs: list[tuple[int, int]] = []
        gaps_holder: list[tuple[int, int]] = []
        for i in range(self.rows):
            for j in range(self.cols):
                try:
                    if self.grid[i][j] == '🥚' or self.grid[i][j] == '0':
                        self.eggs.append((i, j))
                    elif self.grid[i][j] == ' ':
                        gaps_holder.append((i, j))
                except IndexError:
                    gaps_holder.append((i, j))
        """This traverses the grid to populat eggs and gaps"""
        self.gaps = tuple(gaps_holder)
        return None

    def __str__(self) -> str:
        return '\n'.join(tuple(''.join(row) for row in self.grid))

    def get_grid(self) -> list[list[str]]:
        return self.grid

    def get_limit(self) -> int:
        return self.limit

    def get_rows(self) -> int:
        return self.rows

    def get_cols(self) -> int:
        return self.cols

    def get_key(self) -> TileSet:
        return self.key

    def _outside(self, i, j) -> bool:
        return not (0 <= i < self.get_rows() and 0 <= j < self.get_cols())

    def tilt(self, degree: str, moves_left: int
             ) -> tuple[list[str], int, list[str], bool]:
        """This is the main player interaction!

        :param degree: _description_
        :type degree: str
        :param moves_left: _description_
        :type moves_left: int
        :raises ValueError: _description_
        :raises ValueError: _description_
        :return: _description_
        :rtype: tuple[int, list[str], bool]
        """
        try:
            i_velocity, j_velocity = Level.freedom[degree.lower()]
        except KeyError:
            raise ValueError(f"Level.tilt received {degree}")
        increment_points: int = 0
        energy: int = 0 if moves_left == -1 else int(moves_left)
        """This will be used to add points when an egg reaches an empty nest"""
        tweens: list[str] = [str(self)]
        """This will be used to animate the eggs rolling"""
        roll_eggs: list[tuple[int, int]]
        if degree in 'fFlL':
            roll_eggs = sorted(self.eggs)
        elif degree in 'bBrR':
            roll_eggs = sorted(self.eggs)[::-1]
            """This is done to prevent multiple eggs in one tile"""
        else:
            raise ValueError(f"Level.tilt() received: {degree}")
        """All eggs are set to "roll" in roll_eggs at first,
        tilt is finished when no eggs are left or
        when all the eggs have "stopped" in wall_eggs.
        """
        wall_eggs: list[tuple[int, int]] = []

        debug_logs: list[str] = []

        while roll_eggs:
            for (i, j) in tuple(roll_eggs):
                # if DEBUG:  # debug info
                debug_logs.append(
                    f"# {i}, {j} -> {i+i_velocity}, {j+j_velocity}")
                debug_logs.append(
                    f"# {roll_eggs=}, {wall_eggs=}, {self.gaps=}")
                debug_logs.append(f"# {self} #")

                if (
                        self._outside(i + i_velocity, j + j_velocity)
                        or (i + i_velocity, j + j_velocity) in self.gaps
                        or (self.grid[i + i_velocity][j + j_velocity]
                            in self.key.wall_key
                            )
                        or (self.grid[i + i_velocity][j + j_velocity]
                            in self.key.full_key
                            )
                        or (i + i_velocity, j + j_velocity) in wall_eggs
                ):
                    roll_eggs.remove((i, j))
                    wall_eggs.append((i, j))
                elif (self.grid[i + i_velocity][j + j_velocity]
                        in self.key.pan_key):
                    roll_eggs.remove((i, j))
                    self.grid[i][j] = self.key.grass_key
                    increment_points -= 5
                elif (self.grid[i + i_velocity][j + j_velocity]
                        in self.key.empty_key):
                    roll_eggs.remove((i, j))
                    self.grid[i][j] = self.key.grass_key
                    self.grid[i + i_velocity][j + j_velocity] = (
                        self.key.full_key
                        )
                    increment_points += 10 + energy
                else:
                    roll_eggs.remove((i, j))
                    self.grid[i][j] = self.key.grass_key
                    roll_eggs.append((i + i_velocity, j + j_velocity))
                    self.grid[i + i_velocity][j + j_velocity] = (
                        self.key.egg_key
                        )
            tweens.append(str(self))

        if degree in 'lLfF':
            self.eggs = sorted(wall_eggs)
        elif degree in 'rRbB':
            self.eggs = sorted(wall_eggs)[::-1]
        """This re-sorts roll_eggs turned wall_eggs back to self.eggs"""

        return debug_logs, increment_points, tweens, not self.eggs


class Player:
    """_summary_

    :param file_name: _description_
    :type file_name: str
    :param moves_left: _description_
    :type moves_left: int
    :param current_level: _description_
    :type current_level: Level
    :param points: _description_
    :type points: int
    :param game_end: _description_
    :type game_end: bool
    :param past_moves: _description_
    :type past_moves: list[str]
    :param past_Levels: _description_
    :type past_Levels: list[Level]
    :param past_points: _description_
    :type past_points: list[int]
    :param current_input: _description_
    :type current_input: tuple[str, ...]
    :param debug: _description_
    :type debug: bool
    """

    move_to_name: dict[str, str] = {
        'f': "forward",
        'b': "backward",
        'r': "rightward",
        'l': "leftward",
    }

    move_to_symbol: dict[str, str] = {
        'f': '↑',
        'b': '↓',
        'r': '→',
        'l': '←',
    }

    def __init__(self, level_file: TextIOWrapper, is_debug: bool = False
                 ) -> None:
        num_of_rows: int = int(level_file.readline())
        moves_left_holder: str = level_file.readline().strip('\n')
        grid = tuple(
            tuple(str(level_file.readline()).strip('\n'))
            for i in range(num_of_rows)
            )

        self.file_name: str = level_file.name
        self.moves_left: int = (
            -1 if moves_left_holder == "inf"
            else int(moves_left_holder))
        self.current_level: Level = Level(grid, self.moves_left)
        self.points: int = 0
        self.game_end: bool = (self.moves_left == 0)
        self.past_moves: list[str] = []
        self.past_levels: list[Level] = [deepcopy(self.current_level)]
        self.past_points: list[int] = [self.points]
        self.current_input: tuple[str, ...] = ()
        self.debug: bool = is_debug
        return None

    def _set_current_input(self) -> None:
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
        self.game_end = True
        return None

    def _undo_scenario(self) -> None:
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

                time.sleep(
                    (1/self.current_level.get_rows())
                    * (not self.debug)
                    )
                """Makes animation faster for levels with more rows"""
        else:
            print("You can't go back any further...")
            time.sleep(2 * (not self.debug))
        return None

    def _character_scenario(self, char) -> None:
        if self.debug:  # debug info
            print(f"# Input to process: {char}")

        if char in "fFbBrRlL":
            self.past_moves.append(Player.move_to_symbol[char.lower()])

            debug_logs: list[str]
            temp_points: int
            wowaka: list[str]
            debug_logs, temp_points, wowaka, self.game_end = (
                self.current_level.tilt(char, self.moves_left))

            if self.debug:  # debug info
                for log in debug_logs:
                    print(log)

            if len(wowaka) > 1:
                wowaka = wowaka[:-1]
                """Removes buffer frame"""

            for frame in wowaka:
                clear_screen(self.debug)
                print(f"<Tilting {Player.move_to_name[char.lower()]}...>")
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
        print("<Currently playing from level file: ", end='')
        try:
            print(colored(f"{self.file_name}", attrs=["reverse"]), end='')
        except NameError:
            print((self.file_name), end='')
        print('>')
        print()

        print(self.current_level)
        print()

        print(
            "Controls:",
            "> [f] or [F] to tilt the board forward",
            "> [b] or [B] to tilt the board backward",
            "> [r] or [R] to tilt the board rightward",
            "> [l] or [L] to tilt the board leftward",
            "",
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
            elif self.moves_left <= self.current_level.limit//2:
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
        print("[!!!]")
        print()
        print(str(self.current_level))
        time.sleep(0.5 * (not self.debug))
        """Short lag for last frame to make end less abrupt"""

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

    def start_playing(self) -> tuple[Level, tuple[str, ...], int]:
        while not self.game_end and self.moves_left != 0:
            if self.debug:  # debug info
                print("# START OF UNDO CHECK")
                for i in range(len(self.past_levels)):
                    print(self.past_levels[i])
                    print(self.past_points[i])
                    print()
                print("# END OF UNDO CHECK")

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

    def get_state(self) -> tuple[Level, tuple[str, ...], int]:
        return self.current_level, tuple(self.past_moves), self.points


def clear_screen(is_debug: bool) -> None:
    """Clears the terminal screen, if any, while DEBUG is False"""
    if not is_debug:
        print()
        """This newline is here to handle prints(*args, end='')"""
        if sys.stdout.isatty():
            clear_cmd: str = 'cls' if os.name == 'nt' else 'clear'
            try:
                subprocess.run([clear_cmd])
            except Exception:
                os.system(clear_cmd)
    else:
        print("# clear_screen() called")


if __name__ == '__main__':
    is_debug = False

    if is_debug:  # debug info
        print("# egg_roll.py DEBUG IS ON")

    try:
        from termcolor import colored  # type: ignore
        if is_debug:  # debug info
            print("# termcolor loaded")
    except ImportError:
        if is_debug:  # debug info
            print("# termcolor NOT loaded")
        pass

    def argument_handling() -> None:
        print("<Welcome to EGG ROLL!>")
        print()
        try:
            while True:
                with open(sys.argv[1], encoding='utf-8') as level_file:
                    try:
                        game_state: Player = Player(level_file, is_debug)

                        level_end_state: Level
                        moves_made: tuple[str, ...]
                        score: int
                        level_end_state, moves_made, score = (
                            game_state.start_playing())

                    except FileNotFoundError:
                        clear_screen(is_debug)
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

    argument_handling()
