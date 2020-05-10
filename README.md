# ant-world
Created ant simulator.
Ant cloass

Hash table of ants
The key is the hash of the location of the ant. Then there can be no overlap. The value is the Ant object.
One bug: when moving ants, I used to just have a dictionary, take it out, and then change the coordinates between putting it back in, and then looping through all of the ants. However, this would cause one ant to have more than one motion during each time step. To fix this, I created an array that kept track of which ants I have already moved during each time step.



-select_box (made specifically for only one click mouse, rather than a mouse with two buttons)
left click or create selection box to “select” an ant and change its color. Click somewhere else to change its location instantaneously. If you click outside the ant when it is not selected, nothing happens.
The selection box is a rectangle that is created during a mouse click down and then changed to none once you have a mouse click up. One bug that happened early on was that the selection box was not turned into None inside the mouse click up function, causing the ant to constantly be selected and moving even if you wanted to click outside to deselect it.

 Bug: if ant1_selected: #the ant is selected, and this will click on the location for the ant to move. ADD IF YOU CLICK ON IT AGAIN WITH LEFT CLICK.
                #    ant1_selected = False #the ant is in a new position and no longer selected
                #    rectangle = None #otherwise the following rectangle code will run and change ant1_selected to True. You will then always have a selected ant that moves around
     
colliderect() in pygame does not allow for rectangle of negative width and height.

7/27/2019
collectrect() does return an int but also can be used as a boolean. The documentation says boolean.
I thought there was bug here but it turns out I set the ant_selected variable with a - sign instead of = sign.
Managed to create an AntGraphics class in attempts to separate the ant class from the graphics. 

3/21/2020
In notebook, drew out the three steps we have to take.
Note: I want to properly distinguish user clicks/user actions, from the User Inputs (which is the structure that will store these actions)
1. User Input Occurs (a function)
Inputs: User clicks and selection, current simulation object structure
Outputs: User Inputs saved in an object/structure, simulation objects structure changes (ie final destination of selected ants change if selected)

2. Time Step Happens (a function is run)
Inputs: User Inputs (ie info on rectangle selection box, which ants are selected), current simulation object structure
Outputs: User inputs (shouldn't change though), current simulation is updated (ie current position changes to move closer to final destination., fine grid position changes)

3. Drawing Happens
Inputs: User Inputs, Current simulation structure
Output: Plot on screen.
Draw the ants and the environment (needs environemnt)
Drawing health bar on ants that are selected (needs User inputs structure and environment)
Draw selection box if user is in middle of dragging

Command list will be a stack.  Will it also be a state, should we just look at a bug's command list to know its state? That might be better.


Ant world 4/18/2020
Bug. switched order of arguments.
Make conscious decision. Grid input is a numpy array of numbers, with numbers representing the grid type
the state_array for the ants is an array, but not a numpy array
The state of an ant is a two element tuple
Bugs where I switched y and x coordinates

4/4/2020 commit
Implemented and got dijkstras_alg.py working and modified the edge matrix to be more efficient.

4/18/2020 commit
Made a bunch of changes.
Made a pathfinder class to include dijkstras so it can be used as a package outside the python file.
Created a concept of a grid of the ant to be different from the concept of pixels used to draw.
Integrated pathfinding algorithm to be used in a click and move that integrates the ant class as well.
Changed Ant class inside insect.py file to have a stack of states, that would be used to command the ant to move.
Modified the dijkstras algorithm to figure out the x, y ordering of coordinates in the representation. For instance, the 2d matrix uses the 1st coor as the vertical coordinate and 2nd coor as the horizontal coordinate. Got to hash these out.
 
Run ant_select_move_dijkstras.py to see the ant move around the dirt mound.


5/3/2020 commit
fixed A* algorithm, added debugging flag. Note that we have a variable hack added into the string overload function inside PathNode, that converts an index to coordinates in graphelem.py. You'll see when you look.

Timing tests:
(antenv) C:\Users\jonyl\Documents\AntSimulator\ant-world>python dijkstrasalg.py
Running simple uniform cost search
[array([9, 4]), array([9, 3]), array([8, 3]), array([8, 2]), array([7, 2]), array([7, 1]), array([6, 1]), array([6, 0]), array([5, 0]), array([4, 0]), array([3, 0]), array([2, 0]), array([1, 0]), array([0, 0])]
0.020175457000732422
Running simple dijkstras test
[array([9, 4]), array([8, 4]), array([7, 4]), array([6, 4]), array([5, 4]), array([4, 4]), array([3, 4]), array([2, 4]), array([1, 4]), array([0, 4]), array([0, 3]), array([0, 2]), array([0, 1]), array([0, 0])]
0.030042171478271484
Running simple a star
[array([9, 4]), array([8, 4]), array([8, 3]), array([7, 3]), array([7, 2]), array([6, 2]), array([6, 1]), array([5, 1]), array([5, 0]), array([4, 0]), array([3, 0]), array([2, 0]), array([1, 0]), array([0, 0])]
0.023241043090820312
Running large uniform cost
[array([18, 25]), array([17, 25]), array([17, 24]), array([16, 24]), array([16, 23]), array([15, 23]), array([15, 22]), array([14, 22]), array([14, 21]), array([13, 21]), array([13, 20]), array([12, 20]), array([11, 20]), array([10, 20]), array([ 9, 20]), array([ 8, 20]), array([ 8, 19]), array([ 7, 19]), array([ 7, 18]), array([ 6, 18]), array([ 6, 17]), array([ 5, 17]), array([ 5, 16]), array([ 4, 16]), array([ 4, 15]), array([ 3, 15]), array([ 3, 14]), array([ 2, 14]), array([ 2, 13]), array([ 1, 13]), array([ 0, 13]), array([ 0, 12]), array([ 0, 11]), array([ 0, 10]), array([0, 9]), array([0, 8]), array([0, 7]), array([0, 6]), array([0, 5]), array([0, 4]), array([0, 3]), array([0, 2]), array([0, 1]), array([0, 0])]
10.171260118484497
Running large dijkstras test
[array([18, 25]), array([17, 25]), array([16, 25]), array([15, 25]), array([14, 25]), array([13, 25]), array([12, 25]), array([11, 25]), array([10, 25]), array([ 9, 25]), array([ 8, 25]), array([ 7, 25]), array([ 6, 25]), array([ 5, 25]), array([ 4, 25]), array([ 3, 25]), array([ 3, 24]), array([ 3, 23]), array([ 2, 23]), array([ 1, 23]), array([ 0, 23]), array([ 0, 22]), array([ 0, 21]), array([ 0, 20]), array([ 0, 19]), array([ 0, 18]), array([ 0, 17]), array([ 0, 16]), array([ 0, 15]), array([ 0, 14]), array([ 0, 13]), array([ 0, 12]), array([ 0, 11]), array([ 0, 10]), array([0, 9]), array([0, 8]), array([0, 7]), array([0, 6]), array([0, 5]), array([0, 4]), array([0, 3]), array([0, 2]), array([0, 1]), array([0, 0])]
13.845412015914917
Running larger a star test
[array([18, 25]), array([17, 25]), array([17, 24]), array([16, 24]), array([16, 23]), array([15, 23]), array([15, 22]), array([14, 22]), array([14, 21]), array([13, 21]), array([13, 20]), array([12, 20]), array([11, 20]), array([10, 20]), array([ 9, 20]), array([ 9, 19]), array([ 9, 18]), array([ 9, 17]), array([ 9, 16]), array([ 8, 16]), array([ 8, 15]), array([ 7, 15]), array([ 7, 14]), array([ 6, 14]), array([ 6, 13]), array([ 5, 13]), array([ 5, 12]), array([ 4, 12]), array([ 4, 11]), array([ 3, 11]), array([ 3, 10]), array([ 2, 10]), array([2, 9]), array([1, 9]), array([1, 8]), array([0, 8]), array([0, 7]), array([0, 6]), array([0, 5]), array([0, 4]), array([0, 3]), array([0, 2]), array([0, 1]), array([0, 0])]
10.449854373931885

(antenv) C:\Users\jonyl\Documents\AntSimulator\ant-world>python dijkstrasalg.py
Running simple dijkstras test
[array([9, 4]), array([8, 4]), array([7, 4]), array([6, 4]), array([5, 4]), array([4, 4]), array([3, 4]), array([2, 4]), array([1, 4]), array([0, 4]), array([0, 3]), array([0, 2]), array([0, 1]), array([0, 0])]
0.020318984985351562
Running simple uniform cost search
[array([9, 4]), array([9, 3]), array([8, 3]), array([8, 2]), array([7, 2]), array([7, 1]), array([6, 1]), array([6, 0]), array([5, 0]), array([4, 0]), array([3, 0]), array([2, 0]), array([1, 0]), array([0, 0])]
0.023639917373657227
Running simple a star
[array([9, 4]), array([8, 4]), array([8, 3]), array([7, 3]), array([7, 2]), array([6, 2]), array([6, 1]), array([5, 1]), array([5, 0]), array([4, 0]), array([3, 0]), array([2, 0]), array([1, 0]), array([0, 0])]
0.027362585067749023
Running large dijkstras test
[array([18, 25]), array([17, 25]), array([16, 25]), array([15, 25]), array([14, 25]), array([13, 25]), array([12, 25]), array([11, 25]), array([10, 25]), array([ 9, 25]), array([ 8, 25]), array([ 7, 25]), array([ 6, 25]), array([ 5, 25]), array([ 4, 25]), array([ 3, 25]), array([ 3, 24]), array([ 3, 23]), array([ 2, 23]), array([ 1, 23]), array([ 0, 23]), array([ 0, 22]), array([ 0, 21]), array([ 0, 20]), array([ 0, 19]), array([ 0, 18]), array([ 0, 17]), array([ 0, 16]), array([ 0, 15]), array([ 0, 14]), array([ 0, 13]), array([ 0, 12]), array([ 0, 11]), array([ 0, 10]), array([0, 9]), array([0, 8]), array([0, 7]), array([0, 6]), array([0, 5]), array([0, 4]), array([0, 3]), array([0, 2]), array([0, 1]), array([0, 0])]
10.183300495147705
Running large uniform cost
[array([18, 25]), array([17, 25]), array([17, 24]), array([16, 24]), array([16, 23]), array([15, 23]), array([15, 22]), array([14, 22]), array([14, 21]), array([13, 21]), array([13, 20]), array([12, 20]), array([11, 20]), array([10, 20]), array([ 9, 20]), array([ 8, 20]), array([ 8, 19]), array([ 7, 19]), array([ 7, 18]), array([ 6, 18]), array([ 6, 17]), array([ 5, 17]), array([ 5, 16]), array([ 4, 16]), array([ 4, 15]), array([ 3, 15]), array([ 3, 14]), array([ 2, 14]), array([ 2, 13]), array([ 1, 13]), array([ 0, 13]), array([ 0, 12]), array([ 0, 11]), array([ 0, 10]), array([0, 9]), array([0, 8]), array([0, 7]), array([0, 6]), array([0, 5]), array([0, 4]), array([0, 3]), array([0, 2]), array([0, 1]), array([0, 0])]
13.248298406600952
Running larger a star test
[array([18, 25]), array([17, 25]), array([17, 24]), array([16, 24]), array([16, 23]), array([15, 23]), array([15, 22]), array([14, 22]), array([14, 21]), array([13, 21]), array([13, 20]), array([12, 20]), array([11, 20]), array([10, 20]), array([ 9, 20]), array([ 9, 19]), array([ 9, 18]), array([ 9, 17]), array([ 9, 16]), array([ 8, 16]), array([ 8, 15]), array([ 7, 15]), array([ 7, 14]), array([ 6, 14]), array([ 6, 13]), array([ 5, 13]), array([ 5, 12]), array([ 4, 12]), array([ 4, 11]), array([ 3, 11]), array([ 3, 10]), array([ 2, 10]), array([2, 9]), array([1, 9]), array([1, 8]), array([0, 8]), array([0, 7]), array([0, 6]), array([0, 5]), array([0, 4]), array([0, 3]), array([0, 2]), array([0, 1]), array([0, 0])]
11.689187288284302 

I don't know why A* is so slow. It clearly goes through less iterations.

