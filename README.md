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