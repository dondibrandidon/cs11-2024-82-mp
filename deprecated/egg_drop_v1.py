import os
import subprocess
import sys
import time

def clear_screen():
    '''
    Clears the terminal screen, if any'''
    if sys.stdout.isatty():
        clear_cmd = 'cls' if os.name == 'nt' else 'clear'
        subprocess.run([clear_cmd])

class Level:
    '''
    This is the main playing field that the user will see.
    Level takes a tuple of lists of characters: grid.
    '''
    def __init__(self, grid):
        self.grid = list(list(char for char in row if char != '\n') for row in grid)

        #Level.eggs stores the position of all active eggs on the grid
        self.eggs = set()
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                #print(i, j)
                if grid[i][j] == '🥚':
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
        '🥚' - egg         (moves)
        '🟩' - floor       (empty)
        '🧱' - wall        (blocks egg)
        '🍳' - pan         (eats egg -5 points)
        '🪹' - empty nest  (eats egg +10 points)
        '🪺' - full nest   (blocks egg)
        '''
        roll_eggs = self.eggs
        wall_eggs = set()       #tracks eggs that have stopped moving
        super_eggs = set()      #tracks eggs that roll into each other
        while True:
            #print(str(self))
            for (i, j) in tuple(roll_eggs):
                #print(i, j)
                if degree in 'fF':
                    #Pitch Forward
                    if i == 0 or self.grid[i-1][j] in '🧱🪺' or (i-1, j) in wall_eggs:
                        roll_eggs.remove((i, j))
                        wall_eggs.add((i, j))
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
                        if (i, j) not in super_eggs:
                            self.grid[i][j] = '🟩'
                        if (i-1, j) in roll_eggs:
                            super_eggs.add((i-1, j))
                        else:
                            roll_eggs.add((i-1, j))
                        self.grid[i-1][j] = '🥚'
                    
                elif degree in 'bB':
                    #Pitch Backward
                    if i+1 == len(self.grid) or self.grid[i+1][j] in '🧱🪺' or (i+1, j) in wall_eggs:
                        roll_eggs.remove((i, j))
                        wall_eggs.add((i, j))
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
                        if (i, j) not in super_eggs:
                            self.grid[i][j] = '🟩'
                        if (i+1, j) in roll_eggs:
                            super_eggs.add((i+1, j))
                        else:
                            roll_eggs.add((i+1, j))
                        self.grid[i+1][j] = '🥚'

                elif degree in 'rR':
                    #Roll Rightward
                    if j+1 == len(self.grid[0]) or self.grid[i][j+1] in '🧱🪺' or (i, j+1) in wall_eggs:
                        roll_eggs.remove((i, j))
                        wall_eggs.add((i, j))
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
                        if (i, j) not in super_eggs:
                            self.grid[i][j] = '🟩'
                        if (i, j+1) in roll_eggs:
                            super_eggs.add((i, j+1))
                        else:
                            roll_eggs.add((i, j+1))
                        self.grid[i][j+1] = '🥚'

                elif degree in 'lL':
                    #Roll Leftward
                    if j == 0 or self.grid[i][j-1] in '🧱🪺' or (i, j-1) in wall_eggs:
                        roll_eggs.remove((i, j))
                        wall_eggs.add((i, j))
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
                        if (i, j) not in super_eggs:
                            self.grid[i][j] = '🟩'
                        if (i, j-1) in roll_eggs:
                            super_eggs.add((i, j-1))
                        else:
                            roll_eggs.add((i, j-1))
                        self.grid[i][j-1] = '🥚'
                else:
                    raise ValueError()
            print(roll_eggs, wall_eggs, super_eggs)
            #clear_screen()
            print(self)
            time.sleep(0.5) #0.5 second delay

            roll_eggs = roll_eggs | super_eggs
            super_eggs = set()

            if not roll_eggs:
                print("out")
                break

        self.eggs = wall_eggs
        if not self.eggs:
            return self.grid, points, True
        else:
            return self.grid, points, False

def main():
    if len(sys.argv) < 2:
        print('The game requires a filename to start.', file=sys.stderr)
        return
    with open(sys.argv[1], encoding='utf-8') as f:
        #The following three lines process the level file
        num_of_rows = int(f.readline())

        #This decrements with each succesful tilt of the player
        moves_left = int(f.readline())

        grid = tuple(list(f.readline()) for i in range(num_of_rows))

        #This sets the current level for the game
        current_level = Level(grid)
        
        #This logs past moves player made
        past_moves = []
        
        #Player starts with zero points
        points = 0
        
        #This tracks player input
        player = ""
        
        #Start of gameplay
        #clear_screen()
        while moves_left >= 0:
            print(str(current_level))
            print()
            print(f"Controls:\n> [f] or [F] to tilt Forward\n> [b] or [B] to tilt backward\n> [r] or [R] to tilt rightward\n> [l] or [L] to tilt leftward")
            print()
            print(f"Moves made so far: {''.join(past_moves)}")
            print(f"Number of moves left: {moves_left}")
            print(f"Score: {points}")
            
            player = input("Next move: ")
            
            for char in player:
                if char in "fFbBrRlL":
                    current_level.grid, temp_points, game_end = current_level.tilt(char)
                    points += temp_points

                    if player in 'fF':
                        #Pitch Forward
                        past_moves.append('↑')
                    elif player in 'bB':
                        #Pitch Backward
                        past_moves.append('↓')
                    elif player in 'rR':
                        #Roll Rightward
                        past_moves.append('→')
                    elif player in 'lL':
                        #Roll Leftward
                        past_moves.append('←')

                    moves_left -= 1
                    current_level.grid, temp_points, game_end = current_level.tilt(player)
                    points += temp_points
                    #clear_screen()
                    if game_end:
                        break

                else:
                    pass
        
        #Game end state here
        print("[Game Over]")
        print(str(current_level))
        print(f"Moves made: {''.join(past_moves)}")
        print(f"Final Score: {points}")
        print()

#Game initialization
main()
#python3.12 egg_drop.py test_level.txt