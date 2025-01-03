import os
import time
import datetime
from egg_roll_v2 import clear_screen, Player, Level


class Menu:
    """This is the class handling all menu displays,
    and highscore functionalities.

    :param is_debug: Makes debugging more convenient if True,
                     defaults to False
    :type is_debug: bool, optional

    :ivar debug: Enables printing of debug info and disables
                 `time.sleep()` if True
    :vartype debug: bool
    :ivar level_list: Array containing the names of all `.in` files in
                      the `.|levels` folder when it was last checked
    :vartype level_list: tuple[str]
    :ivar freedom: Returns set valid characters for each word direction
    :vartype freedom: dict[str, str]
    """

    directions: tuple[str, str, str, str] = (
        "forward",
        "backward",
        "rightward",
        "leftward",
        )

    def __init__(self, is_debug: bool = False) -> None:
        """This initializes all of the attributes of
        the :class:`~menu_v2.Menu` instance.

        :param is_debug: Makes debugging more convenient if True,
                         defaults to False
        :type is_debug: bool, optional
        """
        self.debug: bool = is_debug
        try:
            # This lists ALL of the .in contents
            # of the .|levels folder valid level or not
            self.level_list: tuple[str, ...] = tuple(
                file
                for file
                in os.listdir(f".{os.sep}levels")
                if file.endswith(".in")
                )

            if self.debug:  # debug info
                print("# self.level_list initialized")

            self.freedom = {
                "forward": 'Ff',
                "backward": 'Bb',
                "rightward": 'Rr',
                "leftward": 'Ll',
            }

            if os.path.isfile(
                f".{os.sep}controls.in",
            ):
                pass  # do nothing if controls.in already exists
            else:
                with open(
                        f".{os.sep}controls.in",
                        'w'
                        ) as settings:
                    # in order of: forward, backward, rightward, leftward
                    settings.write("""\
fF
bB
rR
lL
""")
        except FileNotFoundError:
            raise FileNotFoundError
        super().__init__()

    def _update_level_list(self) -> None:
        """This updates the array of level files
        by checking the contents of the `.|levels` folder.
        """
        try:
            self.level_list = tuple(
                    file
                    for file
                    in os.listdir(f".{os.sep}levels")
                    if file[-3:] == ".in"
                    )
            return None
        except FileNotFoundError:
            raise FileNotFoundError

    def _update_freedom(self) -> None:
        """Updates the `freedom` dictionary
        by checking the `.|controls.in` file.
        """
        with open(
                f".{os.sep}controls.in",
                'r') as settings:
            i = 0
            for setting in settings:
                self.freedom[Menu.directions[i]] = setting.strip('\n')
                i += 1
        return None

    def _update_settings_file(self) -> None:
        """Updates the `.|controls.in` file
        from the instance's current `freedom` dictionary.
        """
        with open(
                f".{os.sep}controls.in",
                'w') as settings:
            for key, value in self.freedom.items():
                settings.write(f"{value}\n")
        return None

    def _generate_blank_highscore_files(
            self,
            ) -> None:
        """Generates a `_score_level_file.txt` for each level in `level_list`.

        The format of a highscore file is as follows::

            player_score1: int
            player_score_datetime1: datetime.datetime
            player_score_name1: str
            ...
            player_score5: int
            player_score_datetime5: datetime.datetime
            player_score_name5: str

        Note that only the TOP 5 mayors are kept in memory.
        """
        for level in self.level_list:
            if os.path.isfile(
                f'.'
                f'{os.sep}levels'
                f'{os.sep}_score_'
                f'{level[:-3]}.txt'
            ):
                pass  # do nothing if _score_level_file.txt already exists
            else:
                if self.debug:  # debug info
                    print(f"# highscore file made for {level}")

                with open(
                        f".{os.sep}levels{os.sep}_score_{level[:-3]}.txt",
                        'w') as score_file:
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

    def _update_highscore(
            self,
            file_played: str,
            score: int,
            ) -> None:
        """Updates the relevant `_score_level_file.txt` file
        from what :func:`~egg_roll_v2.Player.start_playing` returns.
        """
        with open(
                f'.'
                f'{os.sep}levels'
                f'{os.sep}_score_{str(file_played)[:-3]}.txt'
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

            clear_screen(self.debug)

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

            if self.debug:  # debug info
                print(f"# BEFORE: {score_hold}")

            # The TOP 5 mayors are ordered by of highest score,
            # then oldest datetime, then alphabetically
            score_hold.sort(key=lambda x: (-int(x[1]), x[2], x[0]))
            score_hold.pop()

            if self.debug:  # debug info
                print(f"# AFTER: {score_hold}")

            longest_score: int = max(
                max(
                    len(str(hold[1]))
                    for hold
                    in score_hold
                ), 6)  # 6 here is the len of str "SCORES"
            longest_name: int = max(
                max(
                    len(hold[0])
                    for hold
                    in score_hold
                ) + 6, 18)  # 18 here is the len of str "CHICKENCITY_MAYORS"

            if self.debug:  # debug info
                print(f"# {longest_score=}")
                print(f"# {longest_name=}")

            print(f"~ ChickenCity *HALL OF FAME* for {file_played} ~")
            print()
            time.sleep(1 * (not self.debug))

            print(
                "SCORES"
                + " "*(longest_score-6)
                + " | CHICKENCITY MAYORS"
                + " "*(longest_name-18)
                + " | TIME"
                )
            time.sleep(0.5 * (not self.debug))

            for (name, score, date) in score_hold:
                print(
                    f'{score}{" "*(longest_score-len(str(score)))} '
                    f'| Mayor {name}{" "*(longest_name-len(str(name))-6)} '
                    f'| {date}'
                    )
                time.sleep(0.5 * (not self.debug))
        time.sleep(3 * (not self.debug))

        with open(
                f'.'
                f'{os.sep}levels'
                f'{os.sep}_score_{str(file_played)[:-3]}.txt',
                'w') as score_file:
            for (name, score, date) in score_hold:
                score_file.write(f"{name}\n")
                score_file.write(f"{score}\n")
                score_file.write(f"{date}\n")
        return None

    def _print_logo(self) -> None:
        """This handles anytime the logo needs to be printed."""
        print("""\
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_|_|_|_/                        _|_|_|_\\            _|    _|
_|          _|_|\\     _|_|\\     _|     _|   ▓▓▒░░   _|    _|
_|_|_|    _/    _|  _/    _|    _|_|_|_/   ▓▓▒▒▒▒░  _|    _|
_|        _\\    _|  _\\    _|    _|    _\\   █▓▓▒▒▒░  _|    _|
_|_|_|_\\    _|_|_|    _|_|_|    _|     _\\   █▓▓▒░   _|_\\  _|_\\
                |         |
            _|_|/     _|_|/
                                          II: Electric Boogaloo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
""")
        return None

    def _levels_submenu(self) -> None:
        """This handles the [Levels] menu."""
        choice: str = ''
        while choice.lower() != "back":
            clear_screen(self.debug)
            self._print_logo()
            print()

            print("<Level Selection>")
            for i in range(1, len(self.level_list)+1):
                print(f"{i}. {self.level_list[i-1]}")
            print()

            print("Type [Back] to return to main menu or")
            choice
            try:
                choice = input(
                    colored("Enter a valid_level.in:",
                            attrs=["reverse"])
                    + " "
                    )
            except NameError:
                choice = input("Enter a valid_level.in: ")

            if choice in self.level_list:
                self._game_submenu(choice)
            elif choice.lower() != "back":
                print()
                print("Invalid input...")
                time.sleep(2 * (not self.debug))
        return None

    def _controls_submenu(self) -> None:
        """This handles the [Controls] menu."""
        choice: str = ''
        while choice.lower() != "back":
            clear_screen(self.debug)
            self._print_logo()
            print()

            print("<Controls Settings>")
            with open(
                    f".{os.sep}controls.in",
                    'r') as settings:
                i = 0
                for setting in settings:
                    print(Menu.directions[i], end='')
                    print(" = '", end='')
                    print(setting.strip('\n'), end="'\n")
                    i += 1

            print()
            print(
                "* To change something type [direction = 'valid_characters']")
            """This format should be strictly followed by user!"""
            print()

            print("Type [Back] to return to main menu or")
            try:
                choice = input(
                    colored("Enter a control change you'd like to make:",
                            attrs=["reverse"])
                    + " "
                )
            except NameError:
                choice = input("Enter a control change you'd like to make: ")

            if (
                    choice.endswith("'")
                    and any(map(
                        lambda x: choice.startswith(x + " = '"),
                        self.freedom))):
                hold_key, hold_setting = choice.split(' = ')
                valids = set(
                        char
                        for key in self.freedom
                        if key != hold_key
                        for char in self.freedom[key])
                self.freedom[hold_key] = ''.join(
                        sorted(
                            sorted(
                                set(
                                    char for char in hold_setting[1:-1]
                                    if char not in valids),
                                reverse=True),
                            key=lambda x: x.lower()))
                self._update_settings_file()
            elif choice.lower() != "back":
                print()
                print("Invalid input...")
                time.sleep(2 * (not self.debug))
        return None

    def _game_submenu(self, selected_level: str) -> None:
        """This handles the menu for displaying
        :class:`~egg_roll_v2.Player.start_playing`."""
        repeat: str = "yes"
        while repeat.lower() == "yes":
            clear_screen(self.debug)
            with open(
                    f".{os.sep}levels{os.sep}{selected_level}",
                    encoding='utf-8') as level_file:
                try:
                    game_state: Player = Player(
                        level_file,
                        freedom=self.freedom,
                        is_debug=self.debug,
                        )
                except ValueError:
                    self._print_logo()
                    print()
                    print("[!!!]")
                    print(
                        f"Sorry but the level '{selected_level}' is invalid!"
                        )
                    time.sleep(3 * (not self.debug))
                    return None

                final_level_state: Level  # unused here
                moves_made: tuple[str, ...]  # unused here
                score: int
                final_level_state, moves_made, score = (
                    game_state.start_playing())

                repeat = input(
                    'Type [Yes] to try the level again, '
                    'else log your highscore '
                    'and go back to main menu: '
                )
        clear_screen(self.debug)
        self._update_highscore(selected_level, score)
        return None

    def main_menu(self) -> None:
        """This is from where the game handles all of the sub-menus!"""
        while True:
            clear_screen(self.debug)
            self._print_logo()
            print()

            try:
                self._update_freedom()
                self._update_level_list()
                self._generate_blank_highscore_files()
            except FileNotFoundError:
                # Error might happen since relative folder locations are used
                print("Please run this file from the menu_v2's folder.")

            if not self.level_list:
                # End program if no level_file can be loaded
                print("No level files available...")
                print(
                    'Please try to restart the game with a '
                    'a populated .|levels folder')
                print()
                return None

            else:
                print("> [Levels]")
                print("> [Controls]")
                print()
                choice: str
                try:
                    choice = input(
                        colored("Type your chosen menu or [Quit]:",
                                attrs=["reverse"])
                        + " "
                        )
                except NameError:
                    choice = input("Type your chosen menu or [Quit]: ")

                if choice.lower() == "quit":
                    really_quit = input("Really quit EGG ROLL [Yes]? ")
                    if really_quit.lower() == "yes":
                        print()
                        print(
                            '<Thank you for playing egg_roll.py by '
                            'Martin Mendoza (2024-10322) '
                            '& Brandon Sayo (2024-05352)!>')
                        print("{extended to v2 by Brandon Sayo}")
                        print()
                        break
                elif choice.lower() == "levels":
                    self._levels_submenu()
                elif choice.lower() == "controls":
                    self._controls_submenu()
                else:
                    continue
        return None


# This is to prevent main_menu from running when imported for unit testing
if __name__ == '__main__':
    debug: bool = False

    if debug:  # debug info
        print("# menu.py DEBUG IS ON")

    try:
        # "type: ignore"-ed since no mypy support
        from termcolor import colored  # type: ignore
        if debug:  # debug info
            print("# termcolor loaded")
    except ImportError:
        if debug:  # debug info
            print("# termcolor NOT loaded")
        pass

    egg_roll = Menu(is_debug=debug)
    egg_roll.main_menu()
