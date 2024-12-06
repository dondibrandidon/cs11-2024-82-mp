import os, subprocess                       # for clear_screen
import sys                                  # for clear_screen and file handling
import time                                 # for delay
from dataclasses import dataclass, astuple  # for TileSet

@dataclass
class TileSet:
    egg_key: str
    grass_key: str
    wall_key: str
    pan_key: str
    empty_key: str
    full_key: str
    magic_key: str

global DEBUG, EMOJI_SET, ASCII_SET
DEBUG: bool = False # This toggles debugging prints and disables clear_screens for egg_roll.py
EMOJI_SET: TileSet = TileSet(egg_key='🥚', grass_key='🟩', wall_key='🧱', pan_key='🍳', empty_key='🪹', full_key='🪺', magic_key='✨')
ASCII_SET: TileSet = TileSet(egg_key='0', grass_key='.', wall_key='#', pan_key='P', empty_key='O', full_key='@', magic_key='*')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class Level:
    '''
    Each Level object has:
    1. main gameplay interactible 'grid' of tiles
    2. level maker's set move 'limit'
    3. a list of the postions of the 'eggs' in (i, j)
    4. number of grid's 'rows'
    5. number of grid's 'cols'
    6. the 'key' for the relevant graphic
    '''

    def __init__(self, grid: tuple[tuple[str, ...], ...], max_moves: int | str) -> None:
        self.grid: list[list[str]] = list(list(char for char in row if char != '\n') for row in grid)
        self.limit: int = 0 if max_moves == "inf" else int(max_moves)
        self.rows: int = len(self.grid)
        self.cols: int = max(len(row) for row in self.grid)

        # This sets the appropriate TileSet depending on the grid
        self.key: TileSet = EMOJI_SET if any(char in astuple(EMOJI_SET) for row in self.grid for char in row) else ASCII_SET

        # This stores the position of all active eggs on the grid
        self.eggs: list[tuple[int, int]] = []
        for i in range(self.rows):
            for j in range(self.cols):
                try:
                    if grid[i][j] == '🥚' or grid[i][j] == '0':
                        self.eggs.append((i, j))
                except:
                    pass

        
    def __str__(self) -> str:
        return '\n'.join(tuple(''.join(row) for row in self.grid))

    def get_copy(self): # -> Level
        return Level(self.grid, self.limit)
    
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

    # This is the main player interaction!
    def tilt(self, degree: str, moves_left: int | str) -> tuple[int, list[str], bool]:
        assert degree in 'fFbBrRlL'

        # This will be used to monitor points made or lost due to this tilt action
        points: int = 0

        # This will be used to add points when an egg reaches an empty nest
        energy: int = 0 if moves_left == "inf" else int(moves_left)

        # This will be used to animate the egg rolling, first frame is contingency for stuck eggs
        tweens: list[str] = [str(self)]

        '''
        Tiles for reference:
        '🥚' or '0' - egg         (moves around or not)
        '🟩' or '.' - grass       (empty space)
        '🧱' or '#' - wall        (blocks egg)
        '🍳' or 'P' - pan         (eats egg -5 points)
        '🪹' or 'O' - empty nest  (eats egg +10 points then full nest)
        '🪺' or '@' - full nest   (blocks egg)
        '''

        # This list tracks eggs that might still move
        if degree in 'fFlL':
            # During forward and leftward tilts, the grid is processed uppermost then leftmost first to prevent two eggs from going into same spot
            roll_eggs: list[tuple[int, int]] = sorted(self.eggs)
        elif degree in 'bBrR':
            # During backward and rightward tilts, the grid is processed lowermost then rightmost first to prevent two eggs from going into same spot
            roll_eggs = sorted(self.eggs)[::-1]
        else:
            raise ValueError(f"Level.tilt() received: {degree}")

        # This list tracks eggs that have stopped moving
        wall_eggs: list[tuple[int, int]] = []

        while True:
            for (i, j) in tuple(roll_eggs): # tuple-ized since roll_eggs might change

                if DEBUG:
                    print(f"# roll_eggs: {roll_eggs}, wall_eggs: {wall_eggs}")#, super_eggs: {super_eggs}")
                    print('#' + str(self) + '#')
                
                if degree in 'fF':
                    # Tilt Forward
                    if i == 0 or self.grid[i-1][j] in self.key.wall_key + self.key.full_key or (i-1, j) in wall_eggs:
                        roll_eggs.remove((i, j))
                        wall_eggs.append((i, j))
                    elif self.grid[i-1][j] in self.key.pan_key:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = self.key.grass_key
                        points -= 5
                    elif self.grid[i-1][j] in self.key.empty_key:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = self.key.grass_key
                        self.grid[i-1][j] = self.key.full_key
                        points += 10 + energy
                    else:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = self.key.grass_key
                        roll_eggs.append((i-1, j))
                        self.grid[i-1][j] = self.key.egg_key
                    
                elif degree in 'bB':
                    # Tilt Backward
                    if i+1 == len(self.grid) or self.grid[i+1][j] in self.key.wall_key + self.key.full_key or (i+1, j) in wall_eggs:
                        roll_eggs.remove((i, j))
                        wall_eggs.append((i, j))
                    elif self.grid[i+1][j] in self.key.pan_key:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = self.key.grass_key
                        points -= 5
                    elif self.grid[i+1][j] in self.key.empty_key:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = self.key.grass_key
                        self.grid[i+1][j] = self.key.full_key
                        points += 10 + energy
                    else:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = self.key.grass_key
                        roll_eggs.append((i+1, j))
                        self.grid[i+1][j] = self.key.egg_key

                elif degree in 'rR':
                    # Tilt Rightward
                    if j+1 == len(self.grid[0]) or self.grid[i][j+1] in self.key.wall_key + self.key.full_key or (i, j+1) in wall_eggs:
                        roll_eggs.remove((i, j))
                        wall_eggs.append((i, j))
                    elif self.grid[i][j+1] in self.key.pan_key:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = self.key.grass_key
                        points -= 5
                    elif self.grid[i][j+1] in self.key.empty_key:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = self.key.grass_key
                        self.grid[i][j+1] = self.key.full_key
                        points += 10 + energy
                    else:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = self.key.grass_key
                        roll_eggs.append((i, j+1))
                        self.grid[i][j+1] = self.key.egg_key

                elif degree in 'lL':
                    # Tilt Leftward
                    if j == 0 or self.grid[i][j-1] in self.key.wall_key + self.key.full_key or (i, j-1) in wall_eggs:
                        roll_eggs.remove((i, j))
                        wall_eggs.append((i, j))
                    elif self.grid[i][j-1] in self.key.pan_key:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = self.key.grass_key
                    elif self.grid[i][j-1] in self.key.empty_key:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = self.key.grass_key
                        self.grid[i][j-1] = self.key.full_key
                        points += 10 + energy
                    else:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = self.key.grass_key
                        roll_eggs.append((i, j-1))
                        self.grid[i][j-1] = self.key.egg_key
                else:
                    raise ValueError(f"Level.tilt() received: {degree}")
                
            if not roll_eggs:
                # If there are no more moving eggs,
                break
            else:
                # This appends the current state of the Level
                tweens.append(str(self))

        # This properly re-sorts roll_eggs turned wall_eggs back to self.eggs
        if degree in 'lLfF':
                self.eggs = sorted(wall_eggs)
        elif degree in 'rRbB':
                self.eggs = sorted(wall_eggs)[::-1]

        # The returned raw boolean is whether there are any eggs left
        if not self.eggs:
            return points, tweens, True
        else:
            return points, tweens, False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def clear_screen(DEBUG: bool) -> None:
    '''
    Clears the terminal screen, if any, while DEBUG is False
    '''

    if not DEBUG:
        # This newline is here for whenever clear_screen is called after a print(*args, end='')
        print()
        if sys.stdout.isatty():
            clear_cmd: str = 'cls' if os.name == 'nt' else 'clear'
            try:
                subprocess.run([clear_cmd])
            except:
                os.system(clear_cmd)
    else:
        print("# clear_screen() called")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def game_state(level_file, factor=1) -> tuple[Level, list[str], int]:
    '''
    This is an instance of level_file gameplay.
    The repeat prompt happens in the main_menu call, to make it neater.

    The factor multiplies the time.sleep arg, for testing
    '''

    num_of_rows: int = int(level_file.readline())

    # This decrements with each succesful tilt of the player, accepts "inf" as an input
    moves_left: int | str = level_file.readline()

    if moves_left != "inf\n":
        moves_left = int(moves_left)
    else:
        moves_left = "inf"

    # This is the grid of tiles for Level, still has '\n'
    grid = tuple(tuple(str(level_file.readline())) for i in range(num_of_rows))

    # This sets the current level for the game
    current_level: Level = Level(grid, moves_left)
    
    # This logs past moves the player has made
    past_moves: list[str] = []

    # This converts arrow symbol to string
    move_name: dict[str, str] = {'↑':"forward", '↓':"backward", '→':"rightward", '←':"leftward"}
    
    # The player starts with zero points
    points: int = 0
    
    # This tracks the current player input
    player: tuple[str, ...]
    
    # This tracks whether the game is finished
    game_end: bool = False

    # This stores last level states as a Level
    undo_levels: list[Level] = [current_level.get_copy()]

    # This stores last scores (to be used with undo_levels)
    undo_points: list[int] = [points]

    # >>> Start of gameplay <<<
    while str(moves_left) == "inf" or int(moves_left) >= 0:

        if DEBUG:
            print("# START OF UNDO CHECK")
            for i in range(len(undo_levels)):
                print(undo_points[i])
                print(undo_levels[i])
                print()
            print("# END OF UNDO CHECK")

        # >> START of gameplay terminal UI/UX <<
        try:
            clear_screen(DEBUG)
        except NameError:
            print("# clear_screen(DEBUG)")

        print("<Currently playing from level file: ", end='')
        try:
            print(colored(f"{level_file.name}", attrs=["reverse"]), end='')
        except NameError:
            print((level_file.name), end='')
        print('>')

        print()

        print(current_level)
        print()
        
        print("Controls:",
            "> [f] or [F] to tilt the board forward",
            "> [b] or [B] to tilt the board backward",
            "> [r] or [R] to tilt the board rightward",
            "> [l] or [L] to tilt the board leftward",
            "",
            "> [\"Undo\"] to use energy to undo last move",
            "> [\"Exit\"] to quit this level",
            sep="\n")
        print()

        print(f"Moves made so far: {', '.join(past_moves)}") if past_moves else print(f"Moves made so far: None")

        print("Energy left: ", end='')
        try:
            if str(moves_left) == "inf":
                print(colored("∞", "red"))
            elif int(moves_left) == 1:
                print(colored(moves_left, "red"))
            elif int(moves_left) <= current_level.limit//2:
                print(colored(moves_left, "yellow"))
            else:
                print(colored(moves_left, "green"))
        except NameError:
            if str(moves_left) == "inf":
                print("∞")
            else:
                print(moves_left)

        print(f"Points collected: {points}")

        try:
            player = tuple(str(char) for char in input(colored("Next move/s:", attrs=["reverse"]) + ' '))
        except NameError:
            player = tuple(str(char) for char in input("Next move/s: "))

        # >> END of gameplay terminal UI/UX <<


        # >> Start of input processing <<

        if ''.join(player).lower() == 'exit':
            # EXIT SCENARIO
            game_end = True
            break

        elif ''.join(player).lower() == 'undo':
            # UNDO SCENARIO
            if len(undo_levels) > 1:
                past_moves.append('⎌')

                undo_temp_grid: list[str] = str(undo_levels.pop()).split('\n')
                current_level = undo_levels[-1].get_copy()
                undo_points.pop()
                points = undo_points[-1]

                try:
                    moves_left -= 1
                except:
                    pass

                # Undo animation happens here
                for i in range(current_level.get_rows()+1):
                    if DEBUG:
                        print(f"i: {i}")
                    
                    try:
                        clear_screen(DEBUG)
                    except NameError:
                        print("# clear_screen(DEBUG)")
                
                    print("<Undoing...>")
                    print()

                    for _ in range(i):
                        print(current_level.get_key().magic_key*current_level.get_cols())
                    for k in range(i, current_level.get_rows()):
                        if DEBUG:
                            print(f"# k: {k}")

                        print(undo_temp_grid[k])

                    time.sleep((1/current_level.get_rows()) * factor)

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

                    # THIS WHERE THE TILT RETURNS VALUES
                    temp_points, wowaka, game_end = current_level.tilt(char, moves_left)

                    # Logging of move to past_moves list
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

                    # This checks if any eggs rolled (if none display same frame, else remove buffer frame)
                    if len(wowaka) > 1:
                        wowaka = wowaka[1:]

                    # Rolling animation happens here
                    for frame in wowaka:
                        try:
                            try:
                                clear_screen(DEBUG)
                            except NameError:
                                print("# clear_screen(DEBUG)")

                            print(f"<Tilting {move_name[past_moves[-1]]}...>")
                            print()
                            print(frame)
                            time.sleep(0.3 * factor)
                        except:
                            if DEBUG:
                                print("# Animation failed")

                    if DEBUG:
                        print(f"temp_points: {temp_points}")
                    points += temp_points

                    try:
                        moves_left -= 1
                    except:
                        pass
                    
                    try:
                        clear_screen(DEBUG)
                    except NameError:
                        print("# clear_screen(DEBUG)")

                    # Undo processing here
                    undo_levels.append(current_level.get_copy())
                    undo_points.append(points)

                    # Game state check (per individual move)
                    if game_end or (moves_left != "inf" and int(moves_left) <= 0):
                        break
                else:
                    pass

        # Game state check (per player input)
        if game_end or (moves_left != "inf" and int(moves_left) <= 0):
            break
    

    # >>> Start of GAME END STATE here <<<

    try:
        clear_screen(DEBUG)
    except NameError:
        print("# clear_screen(DEBUG)")

    # Short lag for last frame to make end less abrupt
    print("[!!!]")
    print()
    print(str(current_level))
    time.sleep(0.5 * factor)

    try:
        clear_screen(DEBUG)
    except NameError:
        print("# clear_screen(DEBUG)")
    
    # Game Over Screen here
    print("<Game Over>")
    print()

    print(str(current_level))
    print()

    print(f"Moves made: {', '.join(past_moves)}") if past_moves else print(f"Moves made: None")

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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def argument_handling() -> None:
    # Gameplay initialization
    print("<Welcome to EGG ROLL!>")
    print()
    try:
        while True:
            with open(sys.argv[1], encoding='utf-8') as level_file:
                try:
                    game_state(level_file)
                except FileNotFoundError:
                    # End program if argument level_file invalid
                    try:
                        clear_screen(DEBUG)
                    except NameError:
                        print("# clear_screen(DEBUG)")
                    print("File argument invalid! Please open game with valid file location...")
                    print()
                    return
                repeat: str = input("Type [Yes] to replay level, else exit game: ")
                if repeat.lower() == 'yes':
                    continue
                else:
                    break
        print()
        print("<Thank you for playing egg_roll.py by Martin Mendoza (2024-10322) & Brandon Sayo (2024-05352)!>")
        print()

    except:
        print("No file argument! Please open file with valid file location argument...")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Program initialization

# This is to prevent argument_handling from running when imported for unit testing
if __name__ == '__main__':
    if DEBUG:
        print("# egg_roll.py DEBUG IS ON")

    try:
        from termcolor import colored, cprint
        if DEBUG:
            print("# termcolor loaded")
    except ImportError:
        if DEBUG:
            print("# termcolor NOT loaded")
        pass

    argument_handling()