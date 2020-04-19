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


