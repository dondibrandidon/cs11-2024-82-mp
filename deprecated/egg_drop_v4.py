import os
import subprocess
import sys
import time

global debug
debug = False #This toggles insider info

try:
    from termcolor import colored, cprint
    if debug:
        print("termcolor loaded")
except:
    if debug:
        print("termcolor NOT loaded")
    pass

def clear_screen(debug):
    '''
    Clears the terminal screen, if any, while debug is False
    '''
    if not debug:
        if sys.stdout.isatty():
            clear_cmd = 'cls' if os.name == 'nt' else 'clear'
            subprocess.run([clear_cmd])
    else:
        print("clear_screen() called")

class Level:
    '''
    This is the main playing field that the user will see.
    Level takes a tuple of lists of characters: grid.
    '''
    def __init__(self, grid, limit):
        self.grid = list(list(char for char in row if char != '\n') for row in grid)
        self.limit = limit
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

        #Level.eggs stores the position of all active eggs on the grid
        self.eggs = []
        for i in range(self.rows):
            for j in range(self.cols):
                if grid[i][j] == '🥚':
                    self.eggs.append((i, j))
        
    def __str__(self):
        return '\n'.join(tuple(''.join(row) for row in self.grid))

    def tilt(self, degree):
        #Main player interaction
    
        #This will be used to monitor points made or lost due to this tilt action
        points = 0

        '''
        Tiles for reference:
        '🥚' - egg         (moves)
        '🟩' - floor       (empty)
        '🧱' - wall        (blocks egg)
        '🍳' - pan         (eats egg -5 points)
        '🪹' - empty nest  (eats egg +10 points)
        '🪺' - full nest   (blocks egg)
        '''

        #This tracks eggs that might still move
        if degree in 'fFlL':
            #During forward and leftward tilts, the grid is processed uppermost then leftmost first to prevent two eggs going into same spot
            roll_eggs = self.eggs
        elif degree in 'bBrR':
            #During backward and rightward tilts, the grid is processed lowermost then rightmost first to prevent two eggs going into same spot
            roll_eggs = list(self.eggs)[::-1]

        #This tracks eggs that have stopped moving
        wall_eggs = []

        while True:
            for (i, j) in tuple(roll_eggs):
                if debug:
                    print(f"roll_eggs: {roll_eggs}, wall_eggs: {wall_eggs}")#, super_eggs: {super_eggs}")
                    print('/' + str(self) + '/')
                if degree in 'fF':
                    #Tilt Forward
                    if i == 0 or self.grid[i-1][j] in '🧱🪺' or (i-1, j) in wall_eggs:
                        roll_eggs.remove((i, j))
                        wall_eggs.append((i, j))
                    elif self.grid[i-1][j] in '🍳':
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = '🟩'
                        points -= 5
                    elif self.grid[i-1][j] in '🪹':
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = '🟩'
                        self.grid[i-1][j] = '🪺'
                        points += 10
                    else:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = '🟩'
                        roll_eggs.append((i-1, j))
                        self.grid[i-1][j] = '🥚'
                    
                elif degree in 'bB':
                    #Tilt Backward
                    if i+1 == len(self.grid) or self.grid[i+1][j] in '🧱🪺' or (i+1, j) in wall_eggs:
                        roll_eggs.remove((i, j))
                        wall_eggs.append((i, j))
                    elif self.grid[i+1][j] in '🍳':
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = '🟩'
                        points -= 5
                    elif self.grid[i+1][j] in '🪹':
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = '🟩'
                        self.grid[i+1][j] = '🪺'
                        points += 10
                    else:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = '🟩'
                        roll_eggs.append((i+1, j))
                        self.grid[i+1][j] = '🥚'

                elif degree in 'rR':
                    #Tilt Rightward
                    if j+1 == len(self.grid[0]) or self.grid[i][j+1] in '🧱🪺' or (i, j+1) in wall_eggs:
                        roll_eggs.remove((i, j))
                        wall_eggs.append((i, j))
                    elif self.grid[i][j+1] in '🍳':
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = '🟩'
                        points -= 5
                    elif self.grid[i][j+1] in '🪹':
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = '🟩'
                        self.grid[i][j+1] = '🪺'
                        points += 10
                    else:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = '🟩'
                        roll_eggs.append((i, j+1))
                        self.grid[i][j+1] = '🥚'

                elif degree in 'lL':
                    #Tilt Leftward
                    if j == 0 or self.grid[i][j-1] in '🧱🪺' or (i, j-1) in wall_eggs:
                        roll_eggs.remove((i, j))
                        wall_eggs.append((i, j))
                    elif self.grid[i][j-1] in '🍳':
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = '🟩'
                        points -= 5
                    elif self.grid[i][j-1] in '🪹':
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = '🟩'
                        self.grid[i][j-1] = '🪺'
                        points += 10
                    else:
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = '🟩'
                        roll_eggs.append((i, j-1))
                        self.grid[i][j-1] = '🥚'
                else:
                    raise ValueError(f"Level.tilt() received: {degree}")

            if not roll_eggs:
                #If there are no more moving eggs
                break
            else:
                #This is where the "animation" of the eggs rolling happens
                clear_screen(debug)
                print(self)
                time.sleep(0.5)

        #This "re-sorts" roll_eggs turned wall_eggs back to self.eggs
        if degree in 'lLfF':
                self.eggs = wall_eggs
        elif degree in 'rRbB':
                self.eggs = wall_eggs[::-1]

        #The boolean here returns game_end
        if not self.eggs:
            return self.grid, points, True
        else:
            return self.grid, points, False

def game_state(level_file):
    '''
    This is a SINGLE instance of level_file gameplay.
    The repeat prompt happens in the main() call, to make it neater if we process highscores.
    '''

    num_of_rows = int(level_file.readline())

    #This decrements with each succesful tilt of the player
    moves_left = int(level_file.readline())

    grid = tuple(list(level_file.readline()) for i in range(num_of_rows))

    #This sets the current level for the game
    current_level = Level(grid, moves_left)
    
    #This logs past moves the player has made
    past_moves = []
    
    #The player starts with zero points
    points = 0
    
    #This tracks the current player input
    player = ""
    
    #This tracks whether the game is finished
    game_end = False

    #Start of gameplay
    while moves_left >= 0:
        #>>>>> START of gameplayterminal UI/UX
        clear_screen(debug)

        #The [9:] removes "./levels/"
        print(f"[Currently playing: {(level_file.name)[9:]}]")
        print()

        print(current_level)
        print()

        print("Controls:",
            "> [f] or [F] to tilt the board Forward",
            "> [b] or [B] to tilt the board backward",
            "> [r] or [R] to tilt the board rightward",
            "> [l] or [L] to tilt the board leftward",
            #!!!TO BE ADDED: "> [Exit] to quit this level",!!!
            sep="\n")

        print(f"Moves made so far: {', '.join(past_moves)}") if past_moves else print(f"Moves made so far: None")
        print()

        print("No. of turns left: ", end='')
        try:
            if moves_left == 1:
                print(colored(moves_left, "red"))
            elif moves_left <= current_level.limit//2:
                print(colored(moves_left, "yellow"))
            else:
                print(colored(moves_left, "green"))
        except:
            print(moves_left)

        print(f"Points collected: {points}")
        
        player = tuple(char for char in input("Next move/s: "))
        #END of gameplay terminal UI/UX <<<<<
        
        #Start of input processing
        for char in player:
            if debug:
                print(f"Input to process: {char}")

            if char in "fFbBrRlL":
                #Level.tilt() call here
                current_level.grid, temp_points, game_end = current_level.tilt(char)
                points += temp_points
                moves_left -= 1

                #Logging of move processed to past_moves
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
                
                clear_screen(debug)

                #Game state check (per individual move)
                if game_end or moves_left <= 0:
                    break
            else:
                pass

        #Game state check (per player input)
        if game_end or moves_left <= 0:
            break
    
    #Start of GAME END STATE here

    #Short last game state lag to not make end too abrupt
    clear_screen(debug)
    print(str(current_level))
    time.sleep(0.5)

    #Game Over Screen here
    clear_screen(debug)

    print("[Game Over]")
    print()

    print(str(current_level))
    print()

    print(f"Moves made: {', '.join(past_moves)}")

    print("Final Score: ", end='')
    try:
        if points < 0:
            print(colored(points, "red"))
        elif points > 0:
            print(colored(moves_left, "green"))
    except:
        print(points)
    print()

    return str(current_level), past_moves, points
    #End of game_state()

def main():
    '''
    This is the game MAIN MENU.
    '''
    while True:
        #Initial title screen
        clear_screen(debug)
        print("[Welcome to EGG DR🥚P!]")
        print()

        #This lists ALL of the contents of the ./levels folder valid for egg_drop or not
        level_list = os.listdir("./levels")

        #Gameplay initialization
        if not level_list and len(sys.argv) < 2:
            #End program if no level_file can be loaded
            print('No level files available...')
            print('Please restart the game with a valid level_file argument or populated ./levels folder')
            return None

        elif len(sys.argv) == 2:
            #This program prioritizes level_file argument over Level Selection
            with open(sys.argv[1], encoding='utf-8') as level_file:
                while True:
                    game_state(level_file)

                    repeat = input("Type [Yes] to replay level, else go back to main menu: ")
                    if repeat.lower == 'yes':
                        continue
                    else:
                        break
                continue
        else:
            while True:
                clear_screen(debug)
                print("[Welcome to EGG DR🥚P!]")
                print()
                print("Level Selection: ")
                for i in range(1, len(level_list)+1):
                    print(f"{i}: {level_list[i-1]}")
                print()

                choice = input("Enter a valid level_file.xx: ")
                if choice not in level_list:
                    print("Invalid level_file, please try again...")
                    time.sleep(2)
                    continue
                else:
                    pass

                with open("./levels/" + choice, encoding='utf-8') as level_file:
                    while True:
                        game_state(level_file)
                        repeat = input("Type [Yes] to replay level, else go back to main menu: ")
                        if repeat.lower == 'yes':
                            continue
                        else:
                            clear_screen(debug)
                            break
                    continue
        
        repeat = input("Exit EGG DR🥚P [Y/N]? ")
        if repeat in 'Yy':
            break
        elif repeat in 'Nn':
            break
        else:
            clear_screen(debug)
            continue
        if repeat == 'Y':
            continue
        else:
            print("Thank you for playing egg_drop.py!")
            break

#Program initialization
main()