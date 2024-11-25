# **[_#82_] CS11 Machine Problem**
Submission of Group **#82** (_daegu_original_) from class WFJ (_WFJ/MUV1_):\
&nbsp;&nbsp;&nbsp;&nbsp;(_2024-10322_) **Mendoza, Martin C. M.**\
&nbsp;&nbsp;&nbsp;&nbsp;(_2024-05352_) **Sayo, Brandon E.** 

## [📃] Table of Contents
<!-- no toc -->
- [[📂] Files](#📂-files)
- [[🥚] How to Play](#🥚-how-to-play)
- [[🎯] Mechanics](#🎯-mechanics)
- [[🤓] Implementation](#🤓-implementation)
- [[🧪] Unit Testing](#🧪-unit-testing)
- [[💞] Bonus Features](#💞-bonus-features)

## [📂] Files

- `.\egg_roll.py` - **main program for playing _egg_roll_**
- `.\levels\` - stores all gameplay levels for _egg_roll_ level select
  - `.\levels\level_file.in` (sample level file)
- `.\unit_tester.py` - **unit testing program**
- `.\unit_testing\` - stores all testing files for _egg_roll_ functionalities
  - `.\unit_testing\_test_Level_Tilt\test_case.in` (sample test case file for Level.tilt())
  - `.\unit_testing\_test_game_state\test_case.in` (sample test case file for game_state())


## [🥚] How to Play

1. _Terminal_

   - Go to the egg_roll release folder.
   - Two methods to play levels:\
     a. **Recommended**, through the Main Menu: `python3.12 egg_roll.py`\
     b. Direct-to-level, with a level file: `python3.12 egg_roll.py valid_location/level_file.in`

2. _Main Menu_
   - To play, input an available level's full `file_name.in` from the selection.
   - To quit the game, type `quit` then `yes`.

3. _Level Interface_
   - To move the eggs in the board, type a sequence of any valid characters:
     - `F` / `f` to tilt the board forwards    (moving the eggs up)
     - `B` / `b` to tilt the board backwards   (moving the eggs down)
     - `L` / `l` to tilt the board leftwards   (moving the eggs left)
     - `R` / `r` to tilt the board rightwards  (moving the eggs right)
   - To undo your last move at the cost of energy, type `undo`.
   - To exit the level, type `exit`.


## [🎯] Mechanics

You are the mayor of ChickenCity tasked to give all of the city's egg a safe home for a safe future...

**~ Beware These Tiles ~**
1. 🥚 / `0` [Eggs]
   - "_Ang Itloogan ay ang pag-asa ng ating bayan_" (lit. 'Eggs are the hope of our nation' by Jose Rizal)
   - Eggs are the future of our species, cherish them, protect them, and bring them to an empty nest.
   - A smart mayor can save most of the eggs, but the pragmatic mayor can sacrifice one egg to save the rest.
2. 🟩 / `.` [Grass]
   - "_The Green Green Grass of Home_" (Hit Single of Tom "Yum" Jones)
   - One of the few spaces that can be bring about just as much of a comfort as a nest.
   - Though, eggs on grass get so excited that they continue rolling until they are physically stopped.
3. 🧱 / `#` [Walls]
   - "_Walls_"
   - Walls stop eggs.
   - Walls contain our reality from the void of the beyond.
4. 🍳 / `P` [Pans]
   - "_You can't cook an omelette without breaking a few eggs..._" (by unknown)
   - The _Ferricarbus panluto_, known colloquially as the "pan", is the natural predator of the egg.
   - Although pans have no locomotive ability, pans have an insatiable appetite that can consume as much eggs as it can be fed. Because of this, pans thrive in grass-filled biomes where unsuspecting eggs, in their excitement, might accidentally directly roll into the gaping mouth of an awaiting pan. After which, the pan starts to secret a special type of oil that prevents the egg from escaping, as well as, conducts the heat eminating from the pan in order to digest the trapped egg.
   - Metallic weapons called "Metal Utensils" where created to help defend against pans, although a single unit is still too expensive to be widespread in the public.
5. 🪹 / `O` [Empty Nests]
   - "_You haven't had a good night's rest, until you've tried these M.T. Nests!_" (from old candidacy campaign)
   - "Maturation Turkish Nests" (M.T. Nests) was a project originally initiated by the 3rd mayor of ChickenCity, Stanley Aubudon, after negotiation with a nest production company from Turkey. This provided eggs from all around ChickenCity with incredibly cheap but sustainable housing that also decreased hatching time ten-fold. The program was so successful that other cities across the plane have adopted the same project. Nowadays, these nests have become so ubiqutous that the common folk has come to simply know them as "empty nests."
6. 🪺 / `@` [Full Nests]
   - "_DO YOUR PART! Don't share M.T. Nests with other eggs._" (from old health poster)
   - These are fully occupied empty nests.
   - Originally, M.T. Nests could actually hold up to a dozen eggs at a time. This helped make nest maintenance easier and cheaper as it was split among 12 tenants. Although after a _bird flu_ epidemic that put the entire plane on quarantine, the Lord Chicken, passed a law that required nest manufacturers to allow for only one egg to fit per nest. Even after the end of the pandemic, progress in the field of Nestic Engineering actually made single-type M.T. Nests a lot more affordable to the common nest-owner.


## [🤓] Implementation

Lorem ipsum


## [🧪] Unit Testing

Lorem ipsum


## [💞] Bonus Features

Lorem ipsum
