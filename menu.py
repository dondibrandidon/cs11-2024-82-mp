import os       # for file handling
import time     # for delay
import datetime # for highscore time logging
from egg_roll import clear_screen, game_state

global DEBUG
DEBUG: bool = False # This toggles debugging prints and disables clear_screens for menu.py


# The format of a highscore file is as follows:
'''
player_score1: int
player_score_datetime1: datetime.datetime
player_score_name1: str
...
player_score5: int
player_score_datetime5: datetime.datetime
player_score_name5: str
'''
# Note that only the TOP 5 mayors are kept in memory
def generate_highscore_files(levels) -> None:
    for level in levels:
        if os.path.isfile(f".{os.sep}levels{os.sep}_score_{level[:-3]}.txt"):
            pass
        else:
            if DEBUG:
                print(f"# highscore file made for {level}")
            
            with open(f".{os.sep}levels{os.sep}_score_{level[:-3]}.txt", 'a') as score_file:
                hold_names = ("Stanley Aubudon", "Nein Gizzard", "Jefferyi Aves", "Philip Ketupa", "Yangyeom Yangyeom")
                for name in hold_names:
                    score_file.write(f"{name}\n")
                    score_file.write("0\n")
                    score_file.write(f"{datetime.datetime.today()}\n")

# This is called after game_state is returned to main_menu
def highscore_handling(level_file, score) -> None:
    with open(f".{os.sep}levels{os.sep}_score_{str(level_file)[:-3]}.txt") as score_file:
        player_name: str = input("""\
 ______________________________________...
(______________________________________...
 |
 | Thank you for your hard work mayor!
 |
 |
 |
 |
 |
 .
 . Please sign your name below,
 . \
""")

        try:
            clear_screen(DEBUG)
        except NameError:
            print("# clear_screen(DEBUG)")

        score_hold: list[tuple[str, int, datetime.datetime]] = [(player_name, score, datetime.datetime.today())]
        for _ in range(5):
            score_hold.append((str(score_file.readline())[:-1], int(score_file.readline()), datetime.datetime.strptime(str(score_file.readline())[:-1], '%Y-%m-%d %H:%M:%S.%f')))
        
        if DEBUG:
            print(f"# BEFORE: {score_hold}")
        
        # The TOP 5 mayors are ordered by of highest score, then oldest datetime, then alphabetically
        score_hold.sort(key = lambda x: (-int(x[1]), x[2], x[0]))
        score_hold.pop()
        if DEBUG:
            print(f"# AFTER: {score_hold}")

        longest_score: int = max(max(len(str(hold[1])) for hold in score_hold), 6)
        longest_name: int = max(max(len(hold[0]) for hold in score_hold) + 6, 18)

        if DEBUG:
            print(f"# longest_score: {longest_score}")
            print(f"# longest_name: {longest_name}")
        
        print(f"~ ChickenCity *HALL OF FAME* for {level_file} ~")
        print()
        time.sleep(1)

        print("SCORES" + " "*(longest_score-6) + " | CHICKENCITY MAYORS" + " "*(longest_name-18) + " | TIME")
        time.sleep(0.5)

        for (name, score, date) in score_hold:
            print(f"{score}{' '*(longest_score-len(str(score)))} | Mayor {name}{' '*(longest_name-len(str(name))-6)} | {date}")
            time.sleep(0.5)
        
        time.sleep(0.5)

    with open(f".{os.sep}levels{os.sep}_score_{str(level_file)[:-3]}.txt", 'w') as score_file:
        for (name, score, date) in score_hold:
            score_file.write(f"{name}\n")
            score_file.write(f"{score}\n")
            score_file.write(f"{date}\n")

def main_menu() -> None:
    '''
    This is the game's MAIN MENU.
    '''
    while True:
        try:
            #This lists ALL of the contents of the ./levels folder valid for egg_roll or not
            level_list = tuple(file for file in os.listdir(f".{os.sep}levels") if file[-3:] == ".in")
            generate_highscore_files(level_list)

            if DEBUG:
                print("# level_list initialized")
        except FileNotFoundError:
            print('Sorry but please run the application from the egg_roll folder!')
            print()
            return

        # Gameplay initialization
        if not level_list:
            # End program if no level_file can be loaded
            print("<Welcome to EGG ROLL!>")
            print()
            print('No level files available...')
            print('Please restart the game with a valid file location argument or populated .|levels folder')
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
                    with open(f".{os.sep}levels{os.sep}{choice}", encoding='utf-8') as level_file:
                        level_end_state, moves_made, score = game_state(level_file)

                        repeat = input("Type [Yes] to try the level again, else log your highscore and go back to main menu: ")
                        if repeat.lower() == 'yes':
                            continue
                        else:
                            clear_screen(DEBUG)
                            highscore_handling(choice, score)
                            print()
                            input("Press [ENTER] to continue...")

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
# Program initialization

# This is to prevent main_menu from running when imported for unit testing
if __name__ == '__main__':
    if DEBUG:
        print("# menu.py DEBUG IS ON")

    try:
        #from termcolor import colored, cprint
        if DEBUG:
            print("# termcolor loaded")
    except ImportError:
        if DEBUG:
            print("# termcolor NOT loaded")
        pass

    main_menu()