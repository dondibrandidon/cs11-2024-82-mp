# **[*#82*] CS11 Machine Problem**
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


- `egg_roll.py` - **main program for playing _egg_roll_**

- `.|levels|*` - stores all gameplay levels for _egg_roll_ level select
  - `.|levels|level_file.in` (sample level file)

- `unit_tester.py` - **unit testing program**
- `.|unit_testing|*` - stores all testing files for _egg_roll_ functionalities
  - `.|unit_testing|_test_Level_Tilt|test_case.in`\
      (sample test case file for Level.tilt())
  - `.|unit_testing|_test_game_state|test_case.in`\
      (sample test case file for game_state())


## [🥚] How to Play

1. Via *Terminal*
   - Go to the egg_roll release folder.
   - Two methods to play levels:\
     a. **Recommended**, through the Main Menu: `python3.12 menu.py`\
     b. Direct-to-level, with a level file: `python3.12 egg_roll.py .|valid_location|level_file.in`\
      &nbsp;&nbsp;&nbsp;&nbsp;*Method (b) is primarily for testing and does NOT save highscores.

2. Via _Main Menu_
   - To play, input an available level's full `file_name.in` from the selection.
   - To quit the game, type `quit` then `yes`.

3. Via _Level Interface_
   - To move the eggs on the board, type a sequence of any valid characters:
     - `F` or `f` to tilt the board forwards    (moving the eggs up)
     - `B` or `b` to tilt the board backwards   (moving the eggs down)
     - `L` or `l` to tilt the board leftwards   (moving the eggs left)
     - `R` /or `r` to tilt the board rightwards  (moving the eggs right)
   - To undo your last move at the cost of energy, type the word `undo`.
   - To exit the level, type the word `exit`.


## [🎯] Mechanics

You are the mayor of ChickenCity tasked to give all of the city's egg a safe home...

### **Eggs** [🥚 / `0`]
> "*Ang Itloogan ay ang pag-asa ng ating bayan*" - Jose Rizal\
> (lit. 'Eggs are the hope of our nation')
   - Eggs are the future of our species, cherish them, protect them, and bring them to an empty nest.
   - A wise birdie once said  that the smart mayor can save most of the eggs, but the pragmatic mayor can sacrifice one egg to save the all the eggs.


### **Grass** [🟩 / `.`]
> "*The Green Green Grass of Home*" (hit single of Tom "Yum" Jones)
   - One of the few spaces that can be bring about just as much of a comfort as a nest.
   - Though, eggs on grass get so excited that they continue rolling until they are physically stopped...


### **Walls** [🧱 / `#`]
> "*Walls, the all in one solution to ethereal effusion*" (by unknown)
   - Walls stop rolling eggs.
   - Walls contain our reality from the void of the beyond.

### **Pans** [🍳 / `P`]
> "*You can't cook an omelette without breaking a few eggs...*" (by unknown)
   - Prevent eggs, especially a flock of them, from rolling into these\
*prominent painfully-proficient pugnacious and profane predatory pans*.
   - Excerpt from *Chickipedia*:
      > The _Ferricarbus panluto_, known colloquially as the "pan", is the natural predator of the egg. [...]
      > ### Behavior
      > ---
      > Although pans have no locomotive ability, pans have an insatiable appetite that can consume as much eggs as it can be fed; because of this, pans thrive in grass-filled biomes where unsuspecting eggs, in their excitement, might accidentally directly roll into the gaping mouth of an awaiting pan. After which, the pan starts to secrete a special type of oil<sup>[2]</sup> that prevents the egg from escaping, as well as, conducts the heat eminating from the pan in order to digest the trapped egg.[...]
      > ### Relationship with bird-kind ###
      > ---
      > Metallic weapons called "Metal Utensils" where created to help defend against pans, although a single unit is still too expensive<sup>[9]</sup> to be widespread in the public. [...]

### **Empty Nests** [🪹 / `O`]
> "*You haven't had a good night's rest, until you've tried these M.T. Nests!*" (from old candidacy campaign)
   - The dream resting place of any egg.
   - Excerpt from *Chickipedia*:
      > [The distribution of] "Maturation Turkish Nests" (M.T. Nests) was a project originally initiated by the 3rd mayor of ChickenCity, Stanley Aubudon<sup>[3]</sup>, after negotiation with a nest production company from Turkey<sup>[4]</sup>. This provided eggs from all around ChickenCity with incredibly cheap but sustainable housing that also decreased hatching time ten-fold. The program was so successful that other cities across the plane have adopted the same project. Nowadays, these nests have become so ubiqutous that the common folk has come to simply know them as "empty nests."

### **Full Nests** [🪺 / `@`]
> "*DO YOUR PART! Don't share M.T. Nests with other eggs.*" (from old health poster)
   - These are fully occupied empty nests.
   - Excerpt from *Chickipedia*:
      > Originally, M.T. Nests could actually hold up to a dozen eggs at a time. This helped make nest maintenance easier and cheaper as it was split among 12 tenants. Although after a _bird flu_ epidemic<sup>[16]</sup> that put the entire plane on quarantine, the Lord Chicken<sup>[17]</sup>, passed a law that required nest manufacturers to allow for only one egg to fit per nest. Even after the end of the pandemic, progress in the field of Nestic Engineering<sup>[18]</sup> actually made single-type M.T. Nests a lot more affordable to the common nest-owner.


## [🤓] Implementation

1. egg_roll.py
   ```python
   pass
   ```
2. menu.py
   ```python
   pass
   ```


## [🧪] Unit Testing

Lorem ipsum


## [💞] Bonus Features

### **Main Menu**
lorem ipsum

### **Move Undo**
lorem ipsum

### **Highscore Tracking**
lorem ipsum

### **Restart**
lorem ipsum


## [🗺️] Level Submissions

1. **ULTIMATE MAZE** (`daegu_original_ultimate_maze.in`)
   > Maze semi-inspired by the tomb of the mask, it's fun :)

2. **Nested oops** (`daegu_original_nested_oops.in`)
   > Very compact puzzle, hope "Nested oops" don't take too much time XD

3. ***CS11 2024 WFJ*** (`daegu_original_cs11_2024_wfj.in`)
   > A small tribute to our CS11 lecturers, thank you sirs!