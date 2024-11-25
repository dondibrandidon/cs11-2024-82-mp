import os
import subprocess
import sys
import time

class Level:
    '''
    This is the main playing field that the user will see.
    Level takes a tuple of lists of characters: grid.
    '''
    def __init__(self, grid, limit):
        self.grid = list(list(char for char in row if char != '\n') for row in grid)
        self.limit = 0 if limit == "inf" else limit
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

        #Level.eggs stores the position of all active eggs on the grid
        self.eggs = []
        for i in range(self.rows):
            for j in range(self.cols):
                if grid[i][j] == '🥚' or grid[i][j] == '0':
                    self.eggs.append((i, j))
        
    def __str__(self):
        return '\n'.join(tuple(''.join(row) for row in self.grid))

    def copy(self):
        return Level(self.grid, self.limit)

    def tilt(self, degree, energy):
        '''
        This is the main player interaction.
        '''

        #text-based check (defaults to emoji version)
        try:
            if text_based:
                EGG_KEY = '0'
                GRASS_KEY = '.'
                WALL_KEY = '#'
                PAN_KEY = 'P'
                EMPTY_KEY = 'O'
                FULL_KEY = '@'
            else:
                raise Exception()
        except:
            EGG_KEY = '🥚'
            GRASS_KEY = '🟩'
            WALL_KEY = '🧱'
            PAN_KEY = '🍳'
            EMPTY_KEY = '🪹'
            FULL_KEY = '🪺'

        #This will be used to monitor points made or lost due to this tilt action
        points = 0

        #This will be used to add points when an egg reaches an empty nest
        try:
            energy = 0 + energy
        except:
            energy = 0

        #This will be used to animate the egg rolling, first frame is contingency for stuck eggs
        tweens = [str(self)]

        '''
        Tiles for reference:
        '🥚' or '0' - egg         (moves around or not)
        '🟩' or '.' - grass       (empty space)
        '🧱' or '#' - wall        (blocks egg)
        '🍳' or 'P' - pan         (eats egg -5 points)
        '🪹' or 'O' - empty nest  (eats egg +10 points then full nest)
        '🪺' or '@' - full nest   (blocks egg)
        '''

        #This tracks eggs that might still move
        if degree in 'fFlL':
            #During forward and leftward tilts, the grid is processed uppermost then leftmost first to prevent two eggs going into same spot
            roll_eggs = sorted(self.eggs)
        elif degree in 'bBrR':
            #During backward and rightward tilts, the grid is processed lowermost then rightmost first to prevent two eggs going into same spot
            roll_eggs = sorted(self.eggs)[::-1]

        #This tracks eggs that have stopped moving
        wall_eggs = []

        while True:
            for (i, j) in tuple(roll_eggs):
                if debug:
                    print(f"# roll_eggs: {roll_eggs}, wall_eggs: {wall_eggs}")#, super_eggs: {super_eggs}")
                    print('#' + str(self) + '#')
                if degree in 'fF':
                    #Tilt Forward
                    if i == 0 or self.grid[i-1][j] in WALL_KEY+FULL_KEY or (i-1, j) in wall_eggs:
                        roll_eggs.remove((i, j))
                        wall_eggs.append((i, j))
                    elif self.grid[i-1][j] in PAN_KEY:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = GRASS_KEY
                        points -= 5
                    elif self.grid[i-1][j] in EMPTY_KEY:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = GRASS_KEY
                        self.grid[i-1][j] = FULL_KEY
                        points += 10 + energy
                    else:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = GRASS_KEY
                        roll_eggs.append((i-1, j))
                        self.grid[i-1][j] = EGG_KEY
                    
                elif degree in 'bB':
                    #Tilt Backward
                    if i+1 == len(self.grid) or self.grid[i+1][j] in WALL_KEY+FULL_KEY or (i+1, j) in wall_eggs:
                        roll_eggs.remove((i, j))
                        wall_eggs.append((i, j))
                    elif self.grid[i+1][j] in PAN_KEY:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = GRASS_KEY
                        points -= 5
                    elif self.grid[i+1][j] in EMPTY_KEY:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = GRASS_KEY
                        self.grid[i+1][j] = FULL_KEY
                        points += 10 + energy
                    else:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = GRASS_KEY
                        roll_eggs.append((i+1, j))
                        self.grid[i+1][j] = EGG_KEY

                elif degree in 'rR':
                    #Tilt Rightward
                    if j+1 == len(self.grid[0]) or self.grid[i][j+1] in WALL_KEY+FULL_KEY or (i, j+1) in wall_eggs:
                        roll_eggs.remove((i, j))
                        wall_eggs.append((i, j))
                    elif self.grid[i][j+1] in PAN_KEY:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = GRASS_KEY
                        points -= 5
                    elif self.grid[i][j+1] in EMPTY_KEY:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = GRASS_KEY
                        self.grid[i][j+1] = FULL_KEY
                        points += 10 + energy
                    else:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = GRASS_KEY
                        roll_eggs.append((i, j+1))
                        self.grid[i][j+1] = EGG_KEY

                elif degree in 'lL':
                    #Tilt Leftward
                    if j == 0 or self.grid[i][j-1] in WALL_KEY+FULL_KEY or (i, j-1) in wall_eggs:
                        roll_eggs.remove((i, j))
                        wall_eggs.append((i, j))
                    elif self.grid[i][j-1] in PAN_KEY:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = GRASS_KEY
                        points -= 5
                    elif self.grid[i][j-1] in EMPTY_KEY:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = GRASS_KEY
                        self.grid[i][j-1] = FULL_KEY
                        points += 10 + energy
                    else:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = GRASS_KEY
                        roll_eggs.append((i, j-1))
                        self.grid[i][j-1] = EGG_KEY
                else:
                    raise ValueError(f"Level.tilt() received: {degree}")
            if not roll_eggs:
                #If there are no more moving eggs
                break
            else:
                #This appends the last state of the level
                tweens.append(str(self))

        #This "re-sorts" roll_eggs turned wall_eggs back to self.eggs
        if degree in 'lLfF':
                self.eggs = sorted(wall_eggs)
        elif degree in 'rRbB':
                self.eggs = sorted(wall_eggs)[::-1]

        #The boolean here returns game_end
        if not self.eggs:
            return self.grid, points, tweens, True
        else:
            return self.grid, points, tweens, False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def clear_screen(debug):
    '''
    Clears the terminal screen, if any, while debug is False
    '''
    if not debug:
        #This newline is important, if clear_screen is called after a print with end=''
        print()
        if sys.stdout.isatty():
            clear_cmd = 'cls' if os.name == 'nt' else 'clear'
            try:
                subprocess.run([clear_cmd])
            except:
                os.system(clear_cmd)
    else:
        print("# clear_screen() called")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def game_state(level_file):
    '''
    This is a SINGLE instance of level_file gameplay.
    The repeat prompt happens in the menu() call, to make it neater.
    '''
    num_of_rows = int(level_file.readline())

    #This decrements with each succesful tilt of the player
    moves_left = level_file.readline()
    if moves_left != "inf\n":
        moves_left = int(moves_left)
    else:
        moves_left = "inf"

    grid = tuple(list(level_file.readline()) for i in range(num_of_rows))

    #This sets the current level for the game
    current_level = Level(grid, moves_left)
    
    #This logs past moves the player has made
    past_moves = []

    #This converts arrow symbol to string
    move_name = {'↑':"forward", '↓':"backward", '→':"rightward", '←':"leftward"}
    
    #The player starts with zero points
    points = 0
    
    #This tracks the current player input
    player = ""
    
    #This tracks whether the game is finished
    game_end = False

    #This stores last level states as a Level
    undo_levels = [current_level.copy()]

    #This stores last scores (to be used with undo_levels)
    undo_points = [points]

    #Start of gameplay
    while moves_left == "inf" or moves_left >= 0:

        if debug:
            print("# START OF UNDO CHECK")
            for i in range(len(undo_levels)):
                print(undo_points[i])
                print(undo_levels[i])
                print()
            print("# END OF UNDO CHECK")

        #>>>>> START of gameplay terminal UI/UX
        try:
            clear_screen(debug)
        except NameError:
            print("# clear_screen(debug)")

        print("<Currently playing from level file: ", end='')
        try:
            print(colored(f"{level_file.name}", attrs=["reverse"]), end='')
        except NameError:
            print((level_file.name), end='')
        print('>')

        print()

        #This displays the grid to the player
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
            if moves_left == "inf":
                print(colored("∞", "red"))
            elif moves_left == 1:
                print(colored(moves_left, "red"))
            elif moves_left <= current_level.limit//2:
                print(colored(moves_left, "yellow"))
            else:
                print(colored(moves_left, "green"))
        except NameError:
            if moves_left == "inf":
                print("∞")
            else:
                print(moves_left)

        print(f"Points collected: {points}")

        try:
            player = tuple(char for char in input(colored("Next move/s:", attrs=["reverse"]) + ' '))
        except NameError:
            player = tuple(char for char in input("Next move/s: "))
        #END of gameplay terminal UI/UX <<<<<

#-----------------------------------------------------------------#
        #Start of input processing
        if ''.join(player).lower() == 'exit':
            #EXIT SCENARIO
            game_end = True
            break

        elif ''.join(player).lower() == 'undo':
            #UNDO SCENARIO
            if len(undo_levels) > 1:
                past_moves.append('⎌')

                undo_temp_grid = str(undo_levels.pop()).split('\n')
                undo_points.pop()
                current_level = undo_levels[-1].copy()
                points = undo_points[-1]
                try:
                    moves_left -= 1
                except:
                    pass

                #Undo animation happens here
                try:
                    if text_based:
                        MAGIC_KEY = 'X'
                    else:
                        raise Exception()
                except:
                    MAGIC_KEY = '✨'
                
                for i in range(current_level.rows+1):
                    if debug:
                        print(f"i: {i}")
                    
                    try:
                        clear_screen(debug)
                    except NameError:
                        print("# clear_screen(debug)")
                
                    print("<Undoing...>")
                    print()

                    for _ in range(i):
                        print(MAGIC_KEY*current_level.cols)
                    for j in range(i, current_level.rows):
                        if debug:
                            print(f"j: {j}")

                        print(undo_temp_grid[j])

                    time.sleep(1/current_level.rows)

            else:
                print("You can't go back any further...")
                time.sleep(2)
                continue

        else:
            #INPUT SCENARIO
            for char in player:

                if debug:
                    print(f"# Input to process: {char}")

                if char in "fFbBrRlL":

                    #THIS WHERE THE TILT RETURNS VALUES
                    current_level.grid, temp_points, wowaka, game_end = current_level.tilt(char, moves_left)

                    #Logging of move to past_moves list
                    if char in 'fF':
                        #Tilt Forward
                        past_moves.append('↑')
                    elif char in 'bB':
                        #Tilt Backward
                        past_moves.append('↓')
                    elif char in 'rR':
                        #Tilt Rightward
                        past_moves.append('→')
                    elif char in 'lL':
                        #Tilt Leftward
                        past_moves.append('←')

                    #This checks if any eggs rolled (if none display same frame else remove buffer frame)
                    if len(wowaka) > 1:
                        wowaka = wowaka[1:]

                    #Rolling animation happens here
                    for frame in wowaka:
                        try:
                            try:
                                clear_screen(debug)
                            except NameError:
                                print("# clear_screen(debug)")

                            print(f"<Tilting {move_name[past_moves[-1]]}...>")
                            print()
                            print(frame)
                            time.sleep(0.3)
                        except:
                            if debug:
                                print("# Animation failed")

                    if debug:
                        print(f"temp_points: {temp_points}")
                    points += temp_points

                    try:
                        moves_left -= 1
                    except:
                        pass
                    
                    try:
                        clear_screen(debug)
                    except NameError:
                        print("# clear_screen(debug)")

                    #Undo processing here
                    undo_levels.append(current_level.copy())
                    undo_points.append(points)

                    #Game state check (per individual move)
                    if game_end or (moves_left != "inf" and moves_left <= 0):
                        break
                else:
                    pass

        #Game state check (per player input)
        if game_end or (moves_left != "inf" and moves_left <= 0):
            break
    
    #Start of GAME END STATE here

    try:
        #Short last game state lag to not make end too abrupt
        clear_screen(debug)
        print("[!!!]")
        print()
        print(str(current_level))
        time.sleep(0.5)
        clear_screen(debug)
    except NameError:
        if debug:
            print("# Game over screen")
    
    #Game Over Screen here
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
    #End of game_state()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def menu():
    '''
    This is the game's MAIN MENU.
    '''
    while True:
        try:
            #This lists ALL of the contents of the ./levels folder valid for egg_roll or not
            level_list = os.listdir("./levels")
            if debug:
                print("# level_list initialized")
        except FileNotFoundError:
            print('Sorry but please run the application from the egg_roll folder!')
            print()
            return

        #Gameplay initialization
        if not level_list and len(sys.argv) < 2:
            #End program if no level_file can be loaded
            print("<Welcome to EGG ROLL!>")
            print()
            print('No level files available...')
            print('Please restart the game with a valid file location argument or populated ./levels folder')
            print()
            return None

        elif len(sys.argv) == 2:
            #This program prioritizes level_file argument over Level Selection
            while True:
                with open(sys.argv[1], encoding='utf-8') as level_file:
                    try:
                        game_state(level_file)
                    except FileNotFoundError:
                        #End program if argument level_file invalid

                        try:
                            clear_screen(debug)
                        except NameError:
                            print("# clear_screen(debug)")

                        print("<Welcome to EGG ROLL!>")
                        print()
                        print("File argument invalid! Please open game with valid file location...")
                        print()
                        return
                    repeat = input("Type [Yes] to replay level, else go back to main menu: ")
                    if repeat.lower == 'yes':
                        continue
                    else:
                        break
                break

        else:
            while True:

                try:
                    clear_screen(debug)
                except NameError:
                    print("# clear_screen(debug)")

                print(
                    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
                    "",
                    " _|_|_|_/                        _|_|_|_\\            _|    _|",
                    " _|          _|_|\\     _|_|\\     _|     _|   ▓▓▒░░   _|    _|",
                    " _|_|_|    _/    _|  _/    _|    _|_|_|_/   ▓▓▒▒▒▒░  _|    _|",
                    " _|        _\\    _|  _\\    _|    _|    _\\   █▓▓▒▒▒░  _|    _|",
                    " _|_|_|_\\    _|_|_|    _|_|_|    _|     _\\   █▓▓▒░   _|_\\  _|_\\",
                    "                  |         |",
                    "             _|_|/     _|_|/",
                    "",
                    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
                    sep='\n')
                print()

                print("<Level Selection>")
                for i in range(1, len(level_list)+1):
                    print(f"{i}. {level_list[i-1]}")
                print()
                
                print("Type [Quit] to exit program or")
                try:
                    choice = input(colored("Enter a valid level_file.in:", attrs=["reverse"]) + " ")
                except NameError:
                    choice = input("Enter a valid level_file.in: ")

                if choice.lower() == "quit":
                    break
                elif choice not in level_list:
                    print("Invalid level_file, please try again...")
                    time.sleep(2)
                    continue
                else:
                    pass
                
                while True:
                    with open("./levels/" + choice, encoding='utf-8') as level_file:
                        game_state(level_file)
                        repeat = input("Type [Yes] to replay level, else go back to main menu: ")
                        if repeat.lower() == 'yes':
                            continue
                        else:
                            try:
                                clear_screen(debug)
                            except NameError:
                                print("# clear_screen(debug)")
                            break
                    break
        
        while True:
            quit = input("Really quit EGG ROLL [Yes]? ")
            if quit.lower() == "yes":
                print()
                print("<Thank you for playing egg_roll.py by Martin Mendoza (2024-10322) & Brandon Sayo (2024-05352)!>")
                print()
                return None
            else:
                pass
            break
        continue

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#Program initialization

global debug, text_based
debug = False #This toggles insider info print and disables clear_screen calls
text_based = False #This disables emojis and utilizes ASCII instead (WARNING!: REQUIRES ASCII-BASED LEVEL_FILE)

if debug:
    print("~~~~~~~~~~~~~~~~~")
    print("# EGG ROLL STARTED: DEBUG IS ON")

try:
    from termcolor import colored, cprint
    if debug:
        print("# termcolor loaded")
except ImportError:
    if debug:
        print("# termcolor NOT loaded")
    pass

#This is to prevent menu from running when imported for unit testing
if __name__ == '__main__':
    menu()