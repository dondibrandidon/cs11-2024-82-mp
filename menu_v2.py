import os
import time
import datetime
from egg_roll_v2 import clear_screen, Player, Level


def generate_highscore_files(
        levels: tuple[str, ...],
        is_debug: bool = False,
        ) -> None:
    """The format of a highscore file is as follows:

        player_score1: int
        player_score_datetime1: datetime.datetime
        player_score_name1: str
        ...
        player_score5: int
        player_score_datetime5: datetime.datetime
        player_score_name5: str

    *Note that only the TOP 5 mayors are kept in memory.

    :param levels: _description_
    :type levels: _type_
    """
    for level in levels:
        if os.path.isfile(f".{os.sep}levels{os.sep}_score_{level[:-3]}.txt"):
            pass
        else:
            if is_debug:  # debug info
                print(f"# highscore file made for {level}")

            with open(
                    f".{os.sep}levels{os.sep}_score_{level[:-3]}.txt",
                    'a') as score_file:
                hold_names: tuple[str, str, str, str, str] = (
                    "Stanley Aubudon",
                    "Nein Gizzard",
                    "Jefferyi Aves",
                    "Philip Ketupa",
                    "Yangyeom Yangyeom",
                    )
                for name in hold_names:
                    score_file.write(f"{name}\n")
                    score_file.write("0\n")
                    score_file.write(f"{datetime.datetime.today()}\n")
    return None


def highscore_handling(
        level_file: str,
        score: int,
        is_debug: bool = False,
        ) -> None:
    """This is called after game_state is returned to main_menu
    """
    with open(
            f".{os.sep}levels{os.sep}_score_{str(level_file)[:-3]}.txt"
            ) as score_file:
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

        clear_screen(is_debug)

        score_hold: list[tuple[str, int, datetime.datetime]] = [(
            player_name,
            score,
            datetime.datetime.today()
            )]
        for _ in range(5):
            score_hold.append((
                str(score_file.readline())[:-1],
                int(score_file.readline()),
                datetime.datetime.strptime(
                    str(score_file.readline())[:-1],
                    '%Y-%m-%d %H:%M:%S.%f',
                    )
            ))

        if is_debug:  # debug info
            print(f"# BEFORE: {score_hold}")

        # The TOP 5 mayors are ordered by of highest score,
        # then oldest datetime, then alphabetically

        score_hold.sort(key=lambda x: (-int(x[1]), x[2], x[0]))
        score_hold.pop()
        if is_debug:  # debug info
            print(f"# AFTER: {score_hold}")

        longest_score: int = max(
            max(
                len(str(hold[1]))
                for hold
                in score_hold
            ), 6)  # 6 here is "SCORES"
        longest_name: int = max(
            max(
                len(hold[0])
                for hold
                in score_hold
            ) + 6, 18)  # 18 here is "CHICKENCITY_MAYORS"

        if is_debug:  # debug info
            print(f"# {longest_score=}")
            print(f"# {longest_name=}")

        print(f"~ ChickenCity *HALL OF FAME* for {level_file} ~")
        print()
        time.sleep(1 * (not is_debug))

        print("SCORES"
              + " "*(longest_score-6)
              + " | CHICKENCITY MAYORS"
              + " "*(longest_name-18)
              + " | TIME")
        time.sleep(0.5 * (not is_debug))

        for (name, score, date) in score_hold:
            print(f'{score}{' '*(longest_score-len(str(score)))} '
                  f'| Mayor {name}{' '*(longest_name-len(str(name))-6)} '
                  f'| {date}')
            time.sleep(0.5 * (not is_debug))

        time.sleep(0.5 * (not is_debug))

    with open(
            f".{os.sep}levels{os.sep}_score_{str(level_file)[:-3]}.txt",
            'w') as score_file:
        for (name, score, date) in score_hold:
            score_file.write(f"{name}\n")
            score_file.write(f"{score}\n")
            score_file.write(f"{date}\n")

    return None


def main_menu(is_debug: bool = False) -> None:
    """This is the game's MAIN MENU.

    :param is_debug: _description_, defaults to False
    :type is_debug: bool, optional
    :return: _description_
    :rtype: _type_
    """
    while True:
        try:
            # This lists ALL of the .in contents
            # of the .|levels folder valid level or not
            level_list: tuple[str, ...] = tuple(
                file
                for file
                in os.listdir(f".{os.sep}levels")
                if file[-3:] == ".in"
                )
            generate_highscore_files(level_list, is_debug)

            if is_debug:  # debug info
                print("# level_list initialized")

        except FileNotFoundError:
            print(
                'Sorry but please run the application '
                'from the egg_roll folder!'
                )
            print()
            return

        # Gameplay initialization
        if not level_list:
            # End program if no level_file can be loaded
            print("<Welcome to EGG ROLL!>")
            print()
            print('No level files available...')
            print('Please restart the game with a '
                  'valid file location argument '
                  'or a populated .|levels folder')
            print()
            return None

        else:
            while True:
                clear_screen(is_debug)
                print("""\
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 _|_|_|_/                        _|_|_|_\\            _|    _|
 _|          _|_|\\     _|_|\\     _|     _|   ▓▓▒░░   _|    _|
 _|_|_|    _/    _|  _/    _|    _|_|_|_/   ▓▓▒▒▒▒░  _|    _|
 _|        _\\    _|  _\\    _|    _|    _\\   █▓▓▒▒▒░  _|    _|
 _|_|_|_\\    _|_|_|    _|_|_|    _|     _\\   █▓▓▒░   _|_\\  _|_\\
                  |         |
             _|_|/     _|_|/

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
""")
                print()

                print("<Level Selection>")
                for i in range(1, len(level_list)+1):
                    print(f"{i}. {level_list[i-1][:-3]}")
                print()

                print("Type [Quit] to exit program or")

                choice: str
                try:
                    choice = input(
                        colored("Enter a valid level:",
                                attrs=["reverse"])
                        + " "
                        )
                except NameError:
                    choice = input("Enter a valid level: ")

                choice += ".in"

                if choice.lower() == "quit":
                    break
                elif choice not in level_list:
                    print("Invalid level_file, please try again...")
                    time.sleep(2 * (not is_debug))
                    continue
                else:
                    pass

                while True:
                    with open(
                            f".{os.sep}levels{os.sep}{choice}",
                            encoding='utf-8') as level_file:
                        game_state: Player = Player(level_file, is_debug)

                        level_end_state: Level
                        moves_made: tuple[str, ...]
                        score: int
                        level_end_state, moves_made, score = (
                            game_state.start_playing())

                        repeat = input('Type [Yes] to try the level again, '
                                       'else log your highscore '
                                       'and go back to main menu: ')
                        if repeat.lower() == 'yes':
                            continue
                        else:
                            clear_screen(is_debug)
                            highscore_handling(choice, score, is_debug)
                            print()
                            input("Press [ENTER] to continue...")

                            clear_screen(is_debug)

                            break
                    break

        while True:
            quit = input("Really quit EGG ROLL [Yes]? ")
            if quit.lower() == "yes":
                print()
                print('<Thank you for playing egg_roll.py by '
                      'Martin Mendoza (2024-10322) '
                      '& Brandon Sayo (2024-05352)!>')
                print()
                return None
            else:
                pass
            break
        continue


# This is to prevent main_menu from running when imported for unit testing
if __name__ == '__main__':
    is_debug: bool = False

    if is_debug:  # debug info
        print("# menu.py DEBUG IS ON")

    try:
        from termcolor import colored
        if is_debug:  # debug info
            print("# termcolor loaded")
    except ImportError:
        if is_debug:  # debug info
            print("# termcolor NOT loaded")
        pass

    main_menu(is_debug)
