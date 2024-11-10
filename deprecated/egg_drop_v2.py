import os
import subprocess
import sys
import time

def clear_screen(debug):
    '''
    Clears the terminal screen, if any'''
    if not debug:
        if sys.stdout.isatty():
            clear_cmd = 'cls' if os.name == 'nt' else 'clear'
            subprocess.run([clear_cmd])
    else:
        pass

class Level:
    '''
    This is the main playing field that the user will see.
    Level takes a tuple of lists of characters: grid.
    '''
    def __init__(self, grid, limit):
        self.limit = limit
        self.grid = list(list(char for char in row if char != '\n') for row in grid)

        #Level.eggs stores the position of all active eggs on the grid
        self.eggs = set()
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                #print(i, j)
                if grid[i][j] == '0':
                    self.eggs.add((i, j))
        #print(self.eggs)
        
    def __str__(self):
        return '\n'.join(tuple(''.join(row) for row in self.grid))
    
    def tilt(self, degree):
        #Main player interaction
    
        #This will be used to monitor points made or lost due to this tilt action
        points = 0

        '''
        Tiles for reference:
        '0' - egg         (moves)
        '.' - floor       (empty)
        '#' - wall        (blocks egg)
        'P' - pan         (eats egg -5 points)
        'O' - empty nest  (eats egg +10 points)
        '@' - full nest   (blocks egg)
        '''
        roll_eggs = self.eggs
        wall_eggs = set()       #tracks eggs that have stopped moving
        super_eggs = set()      #tracks eggs that roll into each other
        while True:
            #print(str(self))
            for (i, j) in tuple(roll_eggs):
                #print(i, j)
                if debug:
                    print(f" roll_eggs: {roll_eggs}, wall_eggs: {wall_eggs}, super_eggs: {super_eggs}")
                    print(str(self))
                if degree in 'fF':
                    #Pitch Forward
                    if i == 0 or self.grid[i-1][j] in '#@' or (i-1, j) in wall_eggs or (i-2, j) in super_eggs:
                        roll_eggs.remove((i, j))
                        wall_eggs.add((i, j))
                        if (i, j) in super_eggs:
                            super_eggs.remove((i, j))
                            wall_eggs.add((i+1, j))
                            self.grid[i+1][j] = '0'
                    elif self.grid[i-1][j] in 'P':
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = '.'
                        points -= 5
                    elif self.grid[i-1][j] in 'O':
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = '.'
                        self.grid[i-1][j] = '@'
                        points += 10
                    else:
                        roll_eggs.remove((i, j))
                        if (i, j) not in super_eggs:
                            self.grid[i][j] = '.'
                        if (i-1, j) in roll_eggs:
                            super_eggs.add((i-1, j))
                        else:
                            roll_eggs.add((i-1, j))
                        self.grid[i-1][j] = '0'
                    
                elif degree in 'bB':
                    #Pitch Backward
                    if i+1 == len(self.grid) or self.grid[i+1][j] in '#@' or (i+1, j) in wall_eggs or (i+2, j) in super_eggs:
                        roll_eggs.remove((i, j))
                        wall_eggs.add((i, j))
                        if (i, j) in super_eggs:
                            super_eggs.remove((i, j))
                            wall_eggs.add((i-1, j))
                            self.grid[i-1][j] = '0'
                    elif self.grid[i+1][j] in 'P':
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = '.'
                        points -= 5
                    elif self.grid[i+1][j] in 'O':
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = '.'
                        self.grid[i+1][j] = '@'
                        points += 10
                    else:
                        roll_eggs.remove((i, j))
                        if (i, j) not in super_eggs:
                            self.grid[i][j] = '.'
                        if (i+1, j) in roll_eggs:
                            super_eggs.add((i+1, j))
                        else:
                            roll_eggs.add((i+1, j))
                        self.grid[i+1][j] = '0'

                elif degree in 'rR':
                    #Roll Rightward
                    if j+1 == len(self.grid[0]) or self.grid[i][j+1] in '#@' or (i, j+1) in wall_eggs or (i, j+2) in super_eggs:
                        roll_eggs.remove((i, j))
                        wall_eggs.add((i, j))
                        if (i, j) in super_eggs:
                            super_eggs.remove((i, j))
                            wall_eggs.add((i, j-1))
                            self.grid[i][j-1] = '0'
                    elif self.grid[i][j+1] in 'P':
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = '.'
                        points -= 5
                    elif self.grid[i][j+1] in 'O':
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = '.'
                        self.grid[i][j+1] = '@'
                        points += 10
                    else:
                        roll_eggs.remove((i, j))
                        if (i, j) not in super_eggs:
                            self.grid[i][j] = '.'
                        if (i, j+1) in roll_eggs:
                            super_eggs.add((i, j+1))
                        else:
                            roll_eggs.add((i, j+1))
                        self.grid[i][j+1] = '0'

                elif degree in 'lL':
                    #Roll Leftward
                    if j == 0 or self.grid[i][j-1] in '#@' or (i, j-1) in wall_eggs or (i, j-2) in super_eggs:
                        roll_eggs.remove((i, j))
                        wall_eggs.add((i, j))
                        if (i, j) in super_eggs:
                            super_eggs.remove((i, j))
                            wall_eggs.add((i, j+1))
                            self.grid[i][j+1] = '0'
                    elif self.grid[i][j-1] in 'P':
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = '.'
                        points -= 5
                    elif self.grid[i][j-1] in 'O':
                        roll_eggs.remove((i, j))
                        self.grid[i][j] = '.'
                        self.grid[i][j-1] = '@'
                        points += 10
                    else:
                        roll_eggs.remove((i, j))
                        if (i, j) not in super_eggs:
                            self.grid[i][j] = '.'
                        if (i, j-1) in roll_eggs:
                            super_eggs.add((i, j-1))
                        else:
                            roll_eggs.add((i, j-1))
                        self.grid[i][j-1] = '0'
                else:
                    raise ValueError(f"Received: {degree}")
            #if debug:
                #print(f"AFTER roll_eggs: {roll_eggs}, wall_eggs: {wall_eggs}, super_eggs: {super_eggs}")
                #print(str(self))

            if not roll_eggs:
                break
            else:
                clear_screen(debug)
                print(self)
                time.sleep(0.5) #0.5 second delay

                #for egg in super_eggs:
                    #if egg in roll_eggs:
                        
                roll_eggs = roll_eggs | super_eggs
                super_eggs = set()

        self.eggs = wall_eggs
        if not self.eggs:
            return self.grid, points, True
        else:
            return self.grid, points, False

def game_state():
    #if len(sys.argv) < 2:
        #print('The game requires a filename to start.', file=sys.stderr)
        #return
    #with open(sys.argv[1], encoding='utf-8') as f:
    if True:
        #The following three lines process the level file
        #num_of_rows = int(f.readline())

        #This decrements with each succesful tilt of the player
        moves_left = 99999

        #grid = ('########','#OO..00#','#.....P#','########')
        #grid = ('####', '#00#', '#00#', '####')
        grid = ('#####', '#000#', '#000#', '#000#', '#####')

        #This sets the current level for the game
        current_level = Level(grid, moves_left)
        
        #This logs past moves player made
        past_moves = []
        
        #Player starts with zero points
        points = 0
        
        #This tracks player input
        player = ""
        
        #This tracks whether the game is finished
        game_end = False
        
        #Start of gameplay
        #clear_screen()
        while moves_left >= 0:
            clear_screen(debug)
            print(str(current_level))
            print()
            print(f"Controls:\n> [f] or [F] to tilt Forward\n> [b] or [B] to tilt backward\n> [r] or [R] to tilt rightward\n> [l] or [L] to tilt leftward")
            print()
            print(f"Moves made so far: {', '.join(past_moves)}") if past_moves else print(f"Moves made so far: None")
            print(f"No. of turns left: {moves_left}")
            print(f"Points collected: {points}")
            
            player = tuple(char for char in input("Next move/s: "))
            
            for char in player:
                if char in "fFbBrRlL":
                    current_level.grid, temp_points, game_end = current_level.tilt(char)
                    points += temp_points

                    if char in 'fF':
                        #Pitch Forward
                        past_moves.append('↑')
                    elif char in 'bB':
                        #Pitch Backward
                        past_moves.append('↓')
                    elif char in 'rR':
                        #Roll Rightward
                        past_moves.append('→')
                    elif char in 'lL':
                        #Roll Leftward
                        past_moves.append('←')

                    moves_left -= 1
                    points += temp_points
                    clear_screen(debug)
                    if game_end or moves_left <= 0:
                        break
                else:
                    pass
            if game_end or moves_left <= 0:
                break
        
        #Game end state here
        clear_screen(debug)
        print(str(current_level))
        time.sleep(0.5)
        clear_screen(debug)
        print("[Game Over]")
        print()
        print(str(current_level))
        print()
        print(f"Moves made: {', '.join(past_moves)}")
        print(f"Final Score: {points}")
        print()
        
        #For highscore tracking
        return str(current_level), past_moves, points

def main():
    while True:
        #Game initialization
        game_state()
        print()
        while True:
            repeat = input("Play again [Y/N]?")
            if repeat == 'Y':
                break
            elif repeat == 'N':
                break
            else:
                clear_screen(debug)
                continue
        if repeat == 'Y':
            continue
        else:
            break

global debug
#Toggles insider info
debuf = False

main()
#python3.12 egg_drop.py test_level.txt