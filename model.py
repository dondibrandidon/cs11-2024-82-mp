import os
import subprocess
import sys
import time
from dataclasses import dataclass, astuple
from copy import deepcopy


global DEBUG
DEBUG: bool = True


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
             ) -> tuple[int, list[str], bool]:
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
        energy: int = int(moves_left)
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

        while roll_eggs:
            for (i, j) in tuple(roll_eggs):
                if DEBUG:  # debug info
                    print(f"# {i}, {j} -> {i+i_velocity}, {j+j_velocity}")
                    print(f"# {roll_eggs=}, {wall_eggs=}, {self.gaps=}")
                    print(f"# {self} #")

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
                    print("Check 1")
                    roll_eggs.remove((i, j))
                    wall_eggs.append((i, j))
                elif (self.grid[i + i_velocity][j + j_velocity]
                        in self.key.pan_key):
                    print("Check 2")
                    roll_eggs.remove((i, j))
                    self.grid[i][j] = self.key.grass_key
                    increment_points -= 5
                elif (self.grid[i + i_velocity][j + j_velocity]
                        in self.key.empty_key):
                    print("Check 3")
                    roll_eggs.remove((i, j))
                    self.grid[i][j] = self.key.grass_key
                    self.grid[i + i_velocity][j + j_velocity] = (
                        self.key.full_key
                        )
                    increment_points += 10 + energy
                else:
                    print("Check 4")
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

        return increment_points, tweens, not self.eggs


class Player:

    def __init__(self, level_file, debug=False):
        


def clear_screen(DEBUG: bool) -> None:
    """Clears the terminal screen, if any, while DEBUG is False"""
    if not DEBUG:
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


def game_state(level_file, factor=1) -> tuple[Level, list[str], int]:
    """This is an instance of level_file gameplay.
    The repeat prompt happens in the main_menu call, to make it neater.

    :param level_file: _description_
    :type level_file: _type_
    :param factor: _description_, defaults to 1
    :type factor: int, optional
    :return: _description_
    :rtype: tuple[Level, list[str], int]
    """

    num_of_rows: int = int(level_file.readline())
    moves_left_holder: str = level_file.readline()
    moves_left: int = (
        -1 if moves_left_holder == "inf\n"
        else int(moves_left_holder))
    grid = tuple(
        tuple(str(level_file.readline()).strip('\n'))
        for i in range(num_of_rows))
    current_level: Level = Level(grid, moves_left)
    past_moves: list[str] = []
    move_name: dict[str, str] = {
        '↑': "forward",
        '↓': "backward",
        '→': "rightward",
        '←': "leftward",
        }
    points: int = 0
    game_end: bool = (moves_left == 0)
    undo_levels: list[Level] = [deepcopy(current_level)]
    undo_points: list[int] = [points]
    player: tuple[str, ...]

    while not game_end and moves_left != 0:
        if DEBUG:  # debug info
            print("# START OF UNDO CHECK")
            for i in range(len(undo_levels)):
                print(undo_points[i])
                print(undo_levels[i])
                print()
            print("# END OF UNDO CHECK")

        clear_screen(DEBUG)
        print("<Currently playing from level file: ", end='')
        try:
            print(colored(f"{level_file.name}", attrs=["reverse"]), end='')
        except NameError:
            print((level_file.name), end='')
        print('>')
        print()

        print(current_level)
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

        if past_moves:
            print(f"Moves made so far: {', '.join(past_moves)}")
        else:
            print("Moves made so far: None")

        print("Energy left: ", end='')
        try:
            if moves_left == -1:
                print(colored("∞", "red"))
            elif moves_left == 1:
                print(colored(moves_left, "red"))
            elif moves_left <= current_level.limit//2:
                print(colored(moves_left, "yellow"))
            else:
                print(colored(moves_left, "green"))
        except NameError:
            if moves_left == -1:
                print("∞")
            else:
                print(moves_left)

        print(f"Points collected: {points}")

        try:
            player = tuple(
                str(char)
                for char
                in input(colored("Next move/s:", attrs=["reverse"]) + ' ')
                )
        except NameError:
            player = tuple(
                str(char)
                for char
                in input("Next move/s: ")
                )

        if ''.join(player).lower() == 'exit':
            # EXIT SCENARIO
            game_end = True
            break

        elif ''.join(player).lower() == 'undo':
            # UNDO SCENARIO
            if len(undo_levels) > 1:
                past_moves.append('⎌')
                undo_temp_grid: list[str] = str(undo_levels.pop()).split('\n')
                current_level = deepcopy(undo_levels[-1])
                undo_points.pop()
                points = undo_points[-1]
                moves_left -= 1 if moves_left > 0 else 0

                for i in range(current_level.get_rows()+1):
                    if DEBUG:  # debug info
                        print(f"# {i=}")

                    clear_screen(DEBUG)
                    print("<Undoing...>")
                    print()

                    for _ in range(i):
                        print(current_level.get_key().magic_key
                              * current_level.get_cols())
                    for k in range(i, current_level.get_rows()):
                        if DEBUG:
                            print(f"# {k=}")

                        print(undo_temp_grid[k])

                    time.sleep((1/current_level.get_rows()) * factor)
                    """Makes animation faster for levels with more rows"""
            else:
                print("You can't go back any further...")
                time.sleep(2 * factor)
                continue

        else:
            # INPUT SCENARIO
            for char in player:
                if DEBUG:
                    print(f"# Input to process: {char}")

                if char in "fFbBrRlL":
                    temp_points, wowaka, game_end = (
                        current_level.tilt(char, moves_left))
                    if DEBUG:
                        print(f"# {game_end=}")
                    if char in 'fF':
                        # Tilt Forward
                        past_moves.append('↑')
                    elif char in 'bB':
                        # Tilt Backward
                        past_moves.append('↓')
                    elif char in 'rR':
                        # Tilt Rightward
                        past_moves.append('→')
                    elif char in 'lL':
                        # Tilt Leftward
                        past_moves.append('←')

                    if len(wowaka) > 1:
                        wowaka = wowaka[1:]
                        """Removes buffer frame"""

                    for frame in wowaka:
                        clear_screen(DEBUG)
                        print(f"<Tilting {move_name[past_moves[-1]]}...>")
                        print()
                        print(frame)
                        time.sleep(0.3 * factor)

                    if DEBUG:
                        print(f"temp_points: {temp_points}")

                    points += temp_points
                    moves_left -= 1 if moves_left > 0 else 0

                    clear_screen(DEBUG)

                    undo_levels.append(deepcopy(current_level))
                    undo_points.append(points)

                    if game_end or moves_left == 0:
                        break
                    else:
                        pass

    clear_screen(DEBUG)

    print("[!!!]")
    print()
    print(str(current_level))
    time.sleep(0.5 * factor)
    """Short lag for last frame to make end less abrupt"""

    clear_screen(DEBUG)
    print("<Game Over>")
    print()

    print(str(current_level))
    print()

    if past_moves:
        print(f"Moves made: {', '.join(past_moves)}")
    else:
        print("Moves made: None")

    print("Final Score: ", end='')

    if not points:
        print('0')
    try:
        if points < 0:
            print(colored(points, "red"))
        elif points > 0:
            print(colored(points, "green"))
    except NameError:
        print(points)
    print()

    return current_level, past_moves, points


if __name__ == '__main__':
    if DEBUG:  # debug info
        print("# egg_roll.py DEBUG IS ON")

    try:
        from termcolor import colored  # type: ignore
        if DEBUG:  # debug info
            print("# termcolor loaded")
    except ImportError:
        if DEBUG:  # debug info
            print("# termcolor NOT loaded")
        pass

    def argument_handling() -> None:
        print("<Welcome to EGG ROLL!>")
        print()
        try:
            while True:
                with open(sys.argv[1], encoding='utf-8') as level_file:
                    try:
                        game_state(level_file)
                    except FileNotFoundError:
                        clear_screen(DEBUG)
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
                'Martin Mendoza (2024-10322) & Brandon Sayo (2024-05352)!'
                '>'
                )
            print()
        except Exception:
            print(
                'No file argument! '
                'Please open file with valid file location argument...'
                )

    argument_handling()
