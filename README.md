# ant-world
Created ant simulator.
Ant cloass

Hash table of ants
The key is the hash of the location of the ant. Then there can be no overlap. The value is the Ant object.
One bug: when moving ants, I used to just have a dictionary, take it out, and then change the coordinates between putting it back in, and then looping through all of the ants. However, this would cause one ant to have more than one motion during each time step. To fix this, I created an array that kept track of which ants I have already moved during each time step.
