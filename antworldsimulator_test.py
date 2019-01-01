# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 10:45:16 2018

@author: jonyl
"""

from antworldsimulator import Ant
from antworldsimulator import AntWorld

if __name__=="__main__":
    print("Hello Ant World")
    ant_world_1 = AntWorld(10, 10, 1)
    for location in ant_world_1.ant_dict:
        for ant in ant_world_1.ant_dict[location]:
            print (ant)
    
    ant_world_1.move_all_ants_random()
    
    for location in ant_world_1.ant_dict:
        for ant in ant_world_1.ant_dict[location]:
            print (ant)
            
    ant_world_1.move_all_ants_random()
    
    for location in ant_world_1.ant_dict:
        for ant in ant_world_1.ant_dict[location]:
            print (ant)

    ant_world_1.move_all_ants_random()
    
    for location in ant_world_1.ant_dict:
        for ant in ant_world_1.ant_dict[location]:
            print (ant)

    ant_world_1.move_all_ants_random()
    
    for location in ant_world_1.ant_dict:
        for ant in ant_world_1.ant_dict[location]:
            print (ant)
            
    ant_world_1.move_all_ants_random()
    
    for location in ant_world_1.ant_dict:
        for ant in ant_world_1.ant_dict[location]:
            print (ant)    
    for i in range(0,10):
        ant_world_1.move_ant_random(ant)
        print (ant)
    
    #ant1 = Ant(5, 5, 'worker')
    #ant_world_1.place_ant(1, 1, ant1)
    #print ("all ants")
    
    
    #for location in ant_world_1.ant_dict:
    #    for ant in ant_world_1.ant_dict[location]:
    #        print (ant)
    
    """
    while (True):
        ant_world_1.move_all_ants_random()
        print('loop')
        for location in ant_world_1.ant_dict:
            for ant in ant_world_1.ant_dict[location]:
                print('new location')
                print (ant)
                print(len(ant_world_1.ant_dict))
    """