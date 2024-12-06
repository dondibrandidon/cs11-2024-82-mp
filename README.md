# **[*#82*] CS11 Machine Problem 🥚**
Submission of Group **#82** (*daegu_original*) from class WFJ/MUV1:\
&nbsp;&nbsp;&nbsp;&nbsp;(2024-10322) **Mendoza, Martin C. M.**\
&nbsp;&nbsp;&nbsp;&nbsp;(2024-05352) **Sayo, Brandon E.** 


## [📃] Table of Contents
<!-- no toc -->
1. [[📂] Files](#📂-files)
2. [[🥚] How to Play](#🥚-how-to-play)
3. [[🎯] Mechanics](#🎯-mechanics)
4. [[🤓] Implementation](#🤓-implementation)
5. [[🧪] Unit Testing](#🧪-unit-testing)
6. [[💞] Bonus Features](#💞-bonus-features)
7. [[🗺️] Level Submissions](#🗺️-level-submissions)


## [📂] Files


- `egg_roll.py` - **main program for playing egg_roll**

- `.|levels|*` - stores all `.in` gameplay levels for egg_roll level select
  - `.|levels|level_file.in` (sample valid level file)

- `test_er.py` - **unit testing program**
- `.|unit_testing|*` - stores all testing files for egg_roll functionalities
  - `.|unit_testing|_test_Level_tilt|test_case.in`\
      (sample test case file for Level.tilt())
  - `.|unit_testing|_test_game_state|test_case.in`\
      (sample test case file for game_state())


## [🥚] How to Play

1. Opening the file: *Terminal*
   - Go to the egg_roll release folder.
   - Two methods to play levels:\
     a. **Recommended**, through the Main Menu: `python3.12 menu.py`\
     b. Direct-to-level, with a level file: `python3.12 egg_roll.py .|valid_location|level_file.in`\
      &nbsp;&nbsp;&nbsp;&nbsp;*Method (b) is primarily for testing and does NOT save highscores.

2. Navigating the: *Main Menu*
   - To play, input an available level's full `file_name.in` from the selection.
   - To quit the game, type `quit` then `yes`.

3. Playing a level: *Level Interface*
   - To move the eggs on the board, type a sequence of any valid characters:
     - `F` or `f` to tilt the board forwards    (moving the eggs up)
     - `B` or `b` to tilt the board backwards   (moving the eggs down)
     - `L` or `l` to tilt the board leftwards   (moving the eggs left)
     - `R` /or `r` to tilt the board rightwards  (moving the eggs right)
   - To undo your last move at the cost of energy, type the word `undo`.
   - To exit the level, type the word `exit`.
   - To retry the level after reaching the end, type the word `yes` to the prompt.


## [🎯] Mechanics

You are the mayor of ChickenCity [🐔] tasked to give all of the city's egg a safe home...

### **Eggs** [🥚 / `0`]
> "*Ang Itloogan ay ang pag-asa ng ating bayan*" (said by Jose Rizal)\
> (lit. 'Eggs are the hope of our nation')
   - Eggs are the future of our species, cherish them, protect them, and bring them to an empty nest.
   - A wise birdie once said  that the smart mayor can save most of the eggs, but the pragmatic mayor can sacrifice one egg to save the all the eggs.


### **Grass** [🟩 / `.`]
> "*The Green Green Grass of Home*" (hit single of Tom "Yum" Jones)
   - One of the few spaces that can provide almost as much comfort as a nest.
   - Though, eggs on grass get so excited that they continue rolling until they are physically stopped...


### **Walls** [🧱 / `#`]
> "*Walls, the all in one solution to ethereal effusion*" (from ████████)
   - Walls stop rolling eggs.
   - Walls contain ███████████ from the ██████████████████ and protect us from the ancient ████.

### **Pans** [🍳 / `P`]
> "*You can't cook an omelette without breaking a few eggs...*" (ancient proverb)
   - Prevent eggs, especially a whole line of them, from rolling into these\
*prominent painfully-proficient pugnacious and profane predatory pans*.
   - Excerpt from the *Chickipedia* article, "pan":
      > The _Ferricarbus panluto_, known colloquially as the "pan", is the natural predator of the egg. [...]
      > ### Behavior
      > ---
      > Although pans have no locomotive ability, pans have an insatiable appetite that can consume as much eggs as it can be fed; because of this, pans thrive in grass-filled biomes where unsuspecting eggs, in their excitement, might accidentally directly roll into the gaping mouth of an awaiting pan. After which, the pan starts to secrete a special type of oil<sup>[2]</sup> that prevents the egg from escaping, as well as, conducts the heat eminating from the pan in order to digest the trapped egg.[...]
      > ### Relationship with bird-kind ###
      > ---
      > Metallic weapons called "Metal Utensils" where created to help defend against pans, although a single unit is still too expensive<sup>[9]</sup> to be widespread in the public. [...]

### **Empty Nests** [🪹 / `O`]
> "*You haven't had a good night's rest, until you've tried these M.T. Nests!*" (old candidacy campaign)
   - The dream resting place of any egg.
   - Excerpt from the *Chickipedia* article, "M.T. Nests":
      > [The distribution of] "Maturation Turkish Nests" (M.T. Nests) was a project originally initiated by the 3rd mayor of ChickenCity, Stanley Aubudon<sup>[3]</sup>, after negotiation with a nest production company from Turkey<sup>[4]</sup>. This provided eggs from all around ChickenCity with incredibly cheap but sustainable housing that also decreased hatching time ten-fold. The program was so successful that other cities across the plane have adopted the same project. These nests have become so ubiqutous in the past century that any available nests have simply been referred to as "emti" nests (see genericization<sup>[5]</sup>). A trend in 2024, popularized by the younger generations in the social media app ClickCluck, has fancified the term to the now colloquially accepted term, "empty" nests.

### **Full Nests** [🪺 / `@`]
> "*DO YOUR PART! Don't share M.T. Nests with other eggs.*" (old health poster)
   - These are fully occupied empty nests.
   - Excerpt from the *Chickipedia* article, "M.T. Nests":
      > Originally, M.T. Nests could actually hold up to a dozen eggs at a time. This helped make nest maintenance easier and cheaper as it was split among 12 tenants. Although after a _bird flu_ epidemic<sup>[16]</sup> that put the entire plane on quarantine, the Lord Chicken<sup>[17]</sup>, passed a law that required nest manufacturers to allow for only one egg to fit per nest. Even after the end of the pandemic, progress in the field of Nestic Engineering<sup>[18]</sup> actually made single-type M.T. Nests a lot more affordable to the common nest-owner.


## [🤓] Implementation

1. egg_roll.py
   ```python
   class Level:
      def def __init__(self, grid: tuple[tuple[str, ...], ...], max_moves: int | str) -> None
      def tilt(self, degree: str, moves_left: int | str) -> tuple[int, list[str], bool]
   
   def clear_screen(DEBUG: bool) -> None

   def game_state(level_file, factor=1) -> tuple[Level, list[str], int]

   def argument_handling() -> None
   ```
2. menu.py
   ```python
   def generate_highscore_files(levels) -> None

   def highscore_handling(level_file, score) -> None

   def main_menu() -> None
   ```


## [🧪] Unit Testing

### **Overview**
The `test_er.py` script is designed to test the functionality of the `egg_roll` module, specifically the `Level` class and `game_state` function. It utilizes the `pytest` framework to automate the unit testing.

### **Directory**
The script uses the following directory structure for input test files:
```
unit_testing/
│
├── _test_Level_tilt/
│   ├── file1.in
│   ├── file2.in
│   └── ...
│
└── _test_game_state/
    ├── file1.in
    ├── file2.in
    └── ...
```

### **`test_Level_tilt`**
- **Purpose**: Tests the `tilt` method.
- **Input**: Reads from test files in:
    `unit_testing/_test_Level_tilt`
- **Assertions:**
  - Final grid matches expected grid.
  - Point increment matches expected points.
  - Egg presence matches expected value.
**Test Level File Format:**
```
level_rows: int
moves_left: int
row_1: str <input level>
row_2: str
...
row_level_rows: str
valid_character_input: str (character_input validation happens in game_state)
row_1 <expected output level>
row_2
...
row_level_rows 
expected_points: int
expected_no_eggs: bool (int: 0 or 1)
```

### **`test_game_state`**
- **Purpose**: Tests the `game_state` function.
- **Input**: Reads from test files in:
    `unit_testing/_test_game_state`
- **Assertions:**
  - Final grid matches expected grid.
  - List of moves matches expected moves.
  - Total points match expected points.
**Test Level File Format:**
```
string_input: str    #IMPORTANT: len(string_input) >= moves_left
level_rows: int
moves_left: int
row_1: str <input level>
row_2: str
...
row_1: str <expected output level>
row_2: str
...
row_level_rows: str
expected_moves: str
expected_total_points: int
```



### **Test Levels**
#### **in `_test_Level_Tilt`**
*(arranged alphabetically/how it would appear inside the folder)*

  1. `basic_level`
     - Tests all basic functions of a level (tilt, movement, scoring).
     - Simulates a basic environment for levels.
  2. `blurred_lines`
     - Tests how the egg will behave when there is no grass per alternating column and how empty spaces `" "` affect the grid and the egg's movement.
  3. `collision`
     - Tests the collision physics of the egg and walls.
  4. `egg_in_nest`
     - Tests the interaction and scoring function of when an egg goes in an empty nest.
     - Simulates a condition when an egg interacts with an empty nest.
  5. `egg_in_pan`
     - Tests the interaction and scoring function of when an egg goes in a pan.
     - Simulates a condition when an egg interacts with a pan.
  6. `hor_three_egg`
     - Tests the movements of 3 horizontally adjacent eggs across different movements.
     - Simulates how 3 horizontally adjacent eggs would behave. 
  7. `hor_two_egg`
     - Tests the movements of 2 horizontally adjacent eggs across different movements.
     - Simulates how 2 horizontally adjacent eggs would behave.
  8. `one_move`
     - Tests the egg's horizontal (lL/rR) and vertical (fF/bB) movement.
  9. `plus_remaining_moves`
     - Tests how the number of remaining moves is computed to the score when an egg goes in an empty nest.
     - Simulates a condition where an egg goes in an empty nest while having leftover moves.
  10. `running_bond`
      - Tests how levels and the grid are affected by empty spaces `" "` and how it affects the movement of the egg.
      - Level is named after the alternating pattern formed by the empty spaces. (https://www.dimensions.com/element/running-bond)
  11. `stuck`
      - Tests how the egg confined by walls will behave when made to move.
  12. `ver_three_egg`
      - Tests the movements of 3 vertically adjacent eggs across different movements.
      - Simulates how 3 vertically adjacent eggs would behave.
      a. `ver_three_egg_down_pan`
        - Simulates how 3 vertically adjacent eggs would behave and interact with a single pan.
  13. `ver_two_egg`
      - Tests the movements of 2 vertically adjacent eggs across different movements.
      - Simulates how 2 vertically adjacent eggs would behave.
      
#### **in `_test_game_state`**
*(arranged alphabetically/how it would appear inside the folder)*

  1. `basic_level`
     - Tests all basic functions of a level (tilt, movement, scoring).
     - Simulates a basic environment for levels.
  2. `blurred_lines`
     - Tests how the egg will behave when there is no grass per alternating column and how empty spaces `" "` affect the grid and the egg's movement.
  3. `collision`
     - Tests the collision physics of the egg and walls.
  4. `egg_in_nest`
     - Tests the interaction and scoring function of when an egg goes in an empty nest.
     - Simulates a condition when an egg interacts with an empty nest.
  5. `egg_in_pan`
     - Tests the interaction and scoring function of when an egg goes in a pan.
     - Simulates a condition when an egg interacts with a pan.
  6. `plus_remaining_moves`
     - Tests how the number of remaining moves is computed to the score when an egg goes in an empty nest.
     - Simulates a condition where an egg goes in an empty nest while having leftover moves. 
  7. `test_all_directions`
     - Tests all the movements.

   
## [💞] Bonus Features

### **Main Menu**
lorem ipsum

### **Move Undo**
lorem ipsum

### **Highscore Tracking**
lorem ipsum

### **Restart**
lorem ipsum

## **Tile Sets**
lorem ipsum


## [🗺️] Level Submissions

1. **ULTIMATE MAZE** (`daegu_original_ultimate_maze.in`)
   > Maze semi-inspired by the tomb of the mask, it's fun :)

2. **Nested oops** (`daegu_original_nested_oops.in`)
   > Very compact puzzle, hope "Nested oops" don't take too much time XD

3. ***CS11 2024 WFJ*** (`daegu_original_cs11_2024_wfj.in`)
   > A small tribute to our CS11 lecturers, thank you sirs!
