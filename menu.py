import os
import sys
import time

from egg_roll import Level, clear_screen, game_state

def menu():
    '''
    This is the game's MAIN MENU.
    '''
    while True:
        try:
            #This lists ALL of the contents of the ./levels folder valid for egg_roll or not
            level_list = os.listdir("./levels")
            if DEBUG:
                print("# level_list initialized")
        except FileNotFoundError:
            print('Sorry but please run the application from the egg_roll folder!')
            print()
            return

        #Gameplay initialization
        if not level_list:
            #End program if no level_file can be loaded
            print("<Welcome to EGG ROLL!>")
            print()
            print('No level files available...')
            print('Please restart the game with a valid file location argument or populated ./levels folder')
            print()
            return None

        else:
            while True:
                try:
                    clear_screen(DEBUG)
                except NameError:
                    print("# clear_screen(DEBUG)")

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
                                clear_screen(DEBUG)
                            except NameError:
                                print("# clear_screen(DEBUG)")
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

global DEBUG
DEBUG = False #This toggles insider info print and disables clear_screen calls

if DEBUG:
    print("~~~~~~~~~~~~~~~~~")
    print("# MAIN MENU STARTED: DEBUG IS ON")

try:
    from termcolor import colored, cprint
    if DEBUG:
        print("# termcolor loaded")
except ImportError:
    if DEBUG:
        print("# termcolor NOT loaded")
    pass

#This is to prevent menu from running when imported for unit testing
if __name__ == '__main__':
    menu()