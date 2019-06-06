# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 10:45:16 2018

@author: jonyl
"""

from antworldsimulator import Ant
from antworldsimulator import AntWorld
from unittest import TestCase

class AntWorldCreationTest(TestCase):
    def setUp(self, x_dim, y_dim, num_ants):
        self.ant_world_1 = AntWorld(x_dim, y_dim, num_ants)
        
    def test_ant_properties(self, x_dim, y_dim, num_ants):
        self.assertEqual(x_dim, self.ant_world_1.ant_world_x_dim)
        self.assertEqual(y_dim, self.ant_world_1.ant_world_y_dim)
        self.assertEqual(num_ants, self.ant_world_1.ant_world_population)
        

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