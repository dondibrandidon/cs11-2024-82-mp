# **[*#82*] CS11 Machine Problem 🥚**
Submission of Group **#82** (*daegu_original*) from class WFJ/MUV1:\
&nbsp;&nbsp;&nbsp;&nbsp;(2024-10322) **Mendoza, Martin C. M.**\
&nbsp;&nbsp;&nbsp;&nbsp;(2024-05352) **Sayo, Brandon E.** 


## [📃] Table of Contents
<!-- no toc -->
1. [[📂] Files](#📂-files)
2. [[🎯] Mechanics](#🎯-mechanics)
3. [[🥚] How to Play](#🥚-how-to-play)
4. [[💞] Features](#💞-features)
5. [[🤓] Implementation](#🤓-implementation)
6. [[🧪] Unit Testing](#🧪-unit-testing)
7. [[🗺️] Levels](#🗺️-levels)


## [📂] Files

The included files in the submission are laid out as:
```python
.|
├── menu.py                         # The main program for playing egg_roll_v2
├── egg_roll_v2.py                  # Bulk of the gameplay logic code
|
├── levels|                         # Contains level files
│   ├── valid_level.in              # Example valid level file
│   └── ...
│
├── test_er_v2.py                   # Unit testing program for egg_roll_v2.py
|
└── unit_testing_v2|                # More on this in "[🧪] Unit Testing"
    ├── _test_Player_start_playing| # Folder containing test cases for game_state
    └── _test_Level_tilt|           # Folder containing test cases for Level.tilt
```


## [🎯] Mechanics

<h3 style="text-align:center;"> ~ Welcome to EGG ROLL! ~ <br/>
<br/>
🧱🧱🧱🧱🚪🧱🧱🧱🧱<br/>
🧱🪴⬜🟦🟦🟦⬜🪴🧱<br/>
🧱⬜⬜⬜⬜⬜⬜⬜🧱<br/>
🧱⬜⬜⬜⬜⬜⬜⬜🧱<br/>
🧱⬜⬜📋🖥️🥤⬜⬜🧱<br/>
🧱🖨️⬜⬜🐔⬜⬜🗑️🧱<br/>
🧱🗄️🗄️⬜⬜⬜🗄️🗄️🧱<br/>
🧱🪟🪟🪟🪟🪟🪟🪟🧱<br/>
<br/>
As of today, you are the proud mayor of <i>ChickenCity</i> tasked to give all of the city's eggs an available safe nesting place. Below is a short dossier to familiarize yourself with the things you'll need to know for the job...
</h3>
<hr>

### **Eggs** [🥚/ `0`]
> "*Ang Itloogan ay ang pag-asa ng ating bayan*" (said by Jose Rizal)\
> (lit. 'Eggs are the hope of our nation')
   - Eggs are the future of our species, cherish them, protect them, and bring them to an empty nest.
   - A wise birdie once said  that the smart mayor can save most of the eggs, but the pragmatic mayor can sacrifice one egg to save all the eggs.


### **Grass** [🟩/ `.`]
> "*The Green Green Grass of Home*" (hit single of Tom "Yum" Jones)
   - One of the few spaces that can provide almost as much comfort as a nest.
   - Though, eggs on grass get so excited that they continue rolling until they are physically stopped...


### **Walls** [🧱/ `#`]
> "*Walls, the all-in-one solution to ethereal effusion*" (from ████████)
   - Walls stop rolling eggs.
   - Walls contain our reality from the ███ █████ ██████ and protect us from the ancient ████.
   - Walls are made of the ██████ of dead ████.

### **Pans** [🍳/ `P`]
> "*You can't cook an omelette without breaking a few eggs...*" (ancient proverb)
   - Prevent eggs, especially a whole line of them, from rolling into these\
*prominent painfully-proficient pugnacious and profane predatory pans*.
   - Excerpt from the *Chickipedia* article, "pan":
      > The _Ferricarbus panluto_, known colloquially as the "pan", is the natural predator of the egg. [...]
      > ### Behavior
      > ---
      > Although pans have no locomotive ability, pans have an insatiable appetite that can consume as many eggs as it can be fed; because of this, pans thrive in grass-filled biomes where unsuspecting eggs, in their excitement, might accidentally directly roll into the gaping mouth of an awaiting pan. After which, the pan starts to secrete a special type of oil<sup>[2]</sup> that prevents the egg from escaping, as well as, conducts the heat emanating from the pan in order to digest the trapped egg.[...]
      > ### Relationship with bird-kind ###
      > ---
      > Metallic weapons called "Metal Utensils" were created to help defend against pans, although a single unit is still too expensive<sup>[9]</sup> to be widespread in the public. [...]

### **Empty Nests** [🪹/ `O`]
> "*You haven't had a good night's rest, until you've tried these M.T. Nests!*" (old candidacy campaign)
   - The dream resting place of any egg.
   - Excerpt from the *Chickipedia* article, "M.T. Nests":
      > [The distribution of] "Maturation Turkish Nests" (M.T. Nests) was a project originally initiated by the 3rd mayor of ChickenCity, Stanley Aubudon<sup>[3]</sup>, after negotiation with a nest production company from Turkey<sup>[4]</sup>. This provided eggs from all around ChickenCity with incredibly cheap but sustainable housing that also decreased hatching time ten-fold. The program was so successful that other cities across the plane have adopted the same project. These nests have become so ubiquitous in the past century that any available nests have simply been referred to as "emti" nests (see genericization<sup>[5]</sup>). A trend in 2024, popularized by the younger generations in the social media app ClickCluck, has fancified the term to the now colloquially accepted term, "empty" nests.

### **Full Nests** [🪺/ `@`]
> "*DO YOUR PART! Don't share M.T. Nests with other eggs.*" (old health poster)
   - These are fully occupied empty nests.
   - Excerpt from the *Chickipedia* article, "M.T. Nests":
      > Originally, M.T. Nests could actually hold up to a dozen eggs at a time. This helped make nest maintenance easier and cheaper as it was split among 12 tenants. Although after a _bird flu_ epidemic<sup>[16]</sup> that put the entire plane on quarantine, the Lord Chicken<sup>[17]</sup>, passed a law that required nest manufacturers to allow for only one egg to fit per nest. Even after the end of the pandemic, progress in the field of Nestic Engineering<sup>[18]</sup> actually made single-type M.T. Nests a lot more affordable to the common nest owner.


## [🥚] How to Play

1. Opening the program: *Terminal*
   - First, go to the egg_roll release folder.
   - Then choose between the two methods to play levels:\
     a. **Recommended**, through the Main Menu:
     ```bash
     python3.12 menu_v2.py
     ```
     b. Direct-to-level, with a level file: (*does not save highscore!*)
     ```bash
     python3.12 egg_roll_v2.py .|valid_location|level_file.in
     ```
   - Also highly recommended to `pip install` the module `termcolor` for much more colorful interfaces.

2. Navigating: *Main Menu*
   - To play, input an available valid level's full `file_name.in` from the selection.
   - To quit the game, type `quit`, then `yes` to the prompt.

3. Playing a level: *Level Interface*
   - To move the eggs on the board, type a sequence of any valid characters:
     - `F` or `f` to tilt the board forwards (*moving the eggs up*)
     - `B` or `b` to tilt the board backwards (*moving the eggs down*)
     - `L` or `l` to tilt the board leftwards   (*moving the eggs left*)
     - `R` or `r` to tilt the board rightwards  (*moving the eggs right*)
   - To undo your last move at the cost of energy, type the word `undo`.
   - To exit the level, type the word `exit`.
   - To play the same level again after reaching the end, type the word `yes` to the retry prompt.


## [💞] Features

- #### 📃 **Main Menu**
  A simple intuitive main menu, providing mayors with easy access to the list of levels they can play. The display allows level selection and program quitting.

- #### ⌛ **Move Undo**
  Mayors are able to undo any of the moves they've done at the cost of losing a chance to play another move.

- #### 🎖️ **Highscore Tracking**
  The Hall of Fame displays after finishing a level and before going back to the main menu. It tracks the top 5 mayors for each level. The cream of the crop are decided by the highest score, with ties broken by when it was accomplished. After all, the earliest bird catches the worm.

- #### ♻️ **Restart**
  Allows the mayors to reset the current level and start from scratch, if they weren't satisified with your previous run through the level. Useful if you're trying to beat the highscore!

- #### 📐 **Tile Sets**
  The game accepts both emoji-based and text-based levels seemlesly. Advanced TileSet-swapping technology was implemented, although mixing the two tile sets will not work.


## [🤓] Implementation

1. *Implementing* `egg_roll_v2.py`\
   The main logic of the gameplay uses a Level class for the main player interaction logic.
   ```python
   class Level:
      ...
   ```
   This class initializes with values for its main playing `grid`, set move `limit`, list of `eggs`, number of `rows`, maximum number of `cols`, list of `gaps`, and the TileSet `key`. With the main tilting action accomplished through: 

   ```python
      ...
      def tilt(self, degree, moves_left):
         ...
   ```
   As for the main user interface, the following function is used:
   ```python
   def clear_screen(DEBUG):
      ...
   ```
   along with the controller Player class:
   ```python
   class Player:
      ...
   ```
   This class processess all of the contents of the chosen `level_file`, and tracks of the players current info. The main interaction method is:
   ```python
      ...
      def start_playing(self):
         ...
   ```
   A backup function was also defined to handle egg_roll direct-to-file requests:
   ```python
   def argument_handling():
      ...
   ```
2. *Implementing* `menu.py`\
   Next, all of the main menu interface and highscore tracking is done in this file. A placeholder highscore file is immediately created for each level file found in the `.|levels` folder, which is handled by:
   ```python
   def generate_highscore_files(levels):
      ...
   ```
   The highscore logging after a level is done by:
   ```python
   def highscore_handling(level_file, score):
      ...
   ```
   The main menu interface is run through:
   ```python
   def main_menu():
      ...
   ```
   This function displays the level select, calls game_state, and prompts the mayor if they want to play the level again.

3. *Implementing everything*\
   For this project, `Python3.12` was used in Sublime Text and VSCode.\
   Autodocumentation was done with the help of `Sphinx`.\
   The `mypy` module was used for type checking.\
   Finally, unit testing was done with the help of `pytest`:


## [🧪] Unit Testing

### **Overview**
The `test_er_v2.py` script is designed to test the functionality of the `egg_roll_v2` module, specifically the `Level.tilt` and `Class.start_playing`/`Class.get_state` interactions. It utilizes the `pytest` framework to automate the unit testing.

### **Directory**
The script uses the following directory structure for input test files:
```python
.|unit_testing|
│
├── _test_Level_tilt|
│   ├── test_case1.in
│   ├── test_case2.in
│   └── ...
│
└── _test_Player_start_playing|
    ├── test_case1.in
    ├── test_case2.in
    └── ...
```
### **Prerequisites**
- A testing method:\
      - Download and use the `pytest` module for much more convenient and detailed tracking of bugs.\
      - Otherwise, run the file through Python as it has built-in assertions to run the testcases, though bugs will not be tracked easily.
- Follow the prescribed [directory](https://github.com/dondibrandidon/cs11-2024-82-mp/blob/main/README.md#directory) and file structure.

### **Functions**

### > **`test_Level_tilt`**
- **Purpose**: Tests the `Level.tilt` method.
- **Input**: Reads from test files in:
    `.|unit_testing|_test_Level_tilt`
- **Assertions:**
  - Final grid matches expected grid.
  - Point increment matches expected points.
  - Egg presence matches expected value.

**Test Level File Format:**

File name: `test_file_name.in`
```
level_rows: int
moves_left: int
row_1: str                 # the initial grid state
row_2: str
...
row_n: str
valid_character_input: str # validation happens in game_state not here
row_1: str                 # the expected final state
row_2: str  
...
row_n: str  
expected_points: int
expected_no_eggs: 0 | 1    # acts as bool
```

### > **`test_Player_start_playing`**
- **Purpose**: Simulates an interaction with `Player`.
- **Input**: Reads from test files in:
    `.|unit_testing|_Player_start_playing`
- **Assertions:**
  - Final grid matches expected grid.
  - List of moves matches expected moves.
  - Total points match expected points.

**Test Level File Format:**

File name: `test_file_name.in`

> NOTE: This tests `Player.start_playing` specifically for `string_input`s that would be enough to "finish" the game so that `start_playing` would be able to `return` the final states properly. Because of this, `Player.get_state` was used for cases where used to handle `EOFError`s where the `string_input` was not enough.

```
string_input: str
level_rows: int
moves_left: int
row_1: str                 # the initial grid state
row_2: str
...
row_n: str
row_1: str                 # the expected final state
row_2: str
...
row_n: str
expected_moves: str
expected_total_points: int
```

### **Test Levels**
#### **in `_test_Level_tilt`**
*(arranged alphabetically/how it would appear inside the folder)*

1. **`ascii_`**
   - Tests the levels in `ASCII` format for the monospace format.

2. **`basic_level`**
   - Tests all basic functions of a level (tilt, movement, scoring).
   - Simulates a basic environment for levels.

3. **`blurred_lines`**
   - Tests how the egg will behave when there is no grass per alternating column and how empty spaces (`" "`) affect the grid and the egg's movement.

4. **`collision`**
   - Tests the collision physics of the egg and walls.

5. **`egg_in_nest`**
   - Tests the interaction and scoring function of when an egg goes in an empty nest.
   - Simulates a condition when an egg interacts with an empty nest.

6. **`egg_in_pan`**
   - Tests the interaction and scoring function of when an egg goes in a pan.
   - Simulates a condition when an egg interacts with a pan.

7. **`hor_n_egg`**
   - Tests the movements of `n` horizontally adjacent eggs across different movements.
   - Simulates how `n` horizontally adjacent eggs would behave.

8. **`one_move`**
    - Tests the egg's horizontal (`lL/rR`) and vertical (`fF/bB`) movement.

9. **`plus_remaining_moves`**
    - Tests how the number of remaining moves is computed into the score when an egg goes in an empty nest.
    - Simulates a condition where an egg goes in an empty nest while having leftover moves.

10. **`running_bond`**
    - Tests how levels and the grid are affected by empty spaces (`" "`) and how they affect the movement of the egg.
    - Level is named after the alternating pattern formed by the empty spaces. ([Running Bond](https://www.dimensions.com/element/running-bond))

11. **`stuck`**
    - Tests how the egg confined by walls will behave when made to move.

11. **`ver_n_egg`**
    - Tests the movements of `n` vertically adjacent eggs across different movements.
    - Simulates how `n` vertically adjacent eggs would behave.

12. **`_pan`**
    - This is tested in conjunction with the `hor` and `ver` cases for multiple eggs rolling into a pan in one turn.

13. **`n`**
    - For the `n` cases, the values tested were 2, 3, and 100.

      
#### **in `_test_Player_start_playing`**
*(arranged alphabetically/how it would appear inside the folder)*

1. **`ascii_`**  
   - Tests the levels in `ASCII` format for the monospace format.

2. **`basic_level`**  
   - Tests all basic functions of a level (tilt, movement, scoring).  
   - Simulates a basic environment for levels.  

3. **`block`**  
   - Tests how eggs behave when moved in 2x2 and 3x3 formations.  

4. **`collision_nxn`**  
   - Tests the collision physics of an `n` x `n` block of eggs with walls.
   - An early bug was eggs "eating" each other, in cases like this.

5. **`egg_in_nest`**  
   - Tests the interaction and scoring function of when an egg goes in an empty nest.  
   - Simulates a condition when an egg interacts with an empty nest.  

6. **`egg_in_pan`**  
   - Tests the interaction and scoring function of when an egg goes in a pan.  
   - Simulates a condition when an egg interacts with a pan.  

7. **`no_wall_stuck_egg`**  
   - Tests how eggs behave in a 1 x 1 grid with no surrounding walls.  

8. **`plus_remaining_moves`**  
   - Tests how the number of remaining moves is computed into the score when an egg goes in an empty nest.  
   - Simulates a condition where an egg goes in an empty nest while having leftover moves.  

9. **`repeating`**  
   - Tests how eggs behave with repeated inputs.  

10. **`test_all_directions`**  
    - Tests all the movements.  

11. **`with_invalids`**
    - Tests graceful handling of invalid inputs.
    - The invalid inputs are:
      ```python
      invalid_inputs = "thequickownoxjumpedovetheazydogTHEQUICKOWNOXJUMPEDOVETHEAZYDOG1234567890`-=[]\;',./~!@#$%^&*()_+{}|:"<>?"
      ```

12. **`n`**
    - For the `n` cases, the values tested were 2, and 3.

13. **`undo`**
    - Tests the `undo` input functionality.

14. **`incomplete`**
    - Tests `Player.get_state`'s handling of incomplete `string_inputs`.
    
### *Notes*
- Ensure that test files are properly formatted: `test_file_name.in`.


## [🗺️] Levels

1. **Example Level** (`example.in`)
   > The simple example level

2. **Text-based Example Level** (`ascii_example.in`)
   > A text-based version of the example level with infinite moves

2. **ULTIMATE MAZE** (`ultimate_maze.in`)
   > Maze semi-inspired by the tomb of the mask, it's fun :)

3. **Nested oops** (`nested_oops.in`)
   > Very compact puzzle, hope "Nested oops" doesn't take too much time XD

4. ***CS11 2024 WFJ*** (`cs11_2024_wfj.in`)
   > A small tribute to our CS11 lecturers, thank you sirs!
