# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 18:54:04 2018

@author: jonyl
"""
import numpy as np
import random
import time
import pygame

DIRT = 0
AIR = 1
ANT = 2
social_security = 0

"""
x_dim is in x-direction of array, y_dim is in y-direction of array. When 
calling array at location, you do array(y, x)

"""

        
class Ant:
    def __init__(self, x_start_loc, y_start_loc, ant_type = 'worker'):
        self.x_ant_loc = x_start_loc
        self.y_ant_loc = y_start_loc
        self.ant_type = ant_type
        global social_security
        self.ant_social_security = social_security
        social_security = social_security + 1
    def __str__(self):
        return ('(' + str(self.x_ant_loc) + ',' + str(self.y_ant_loc) + ')' + \
            ' ' + str(self.ant_social_security))
    
    def return_key(self):
        return (str(self.x_ant_loc) + ',' + str(self.y_ant_loc))

class AntWorld:
    def __init__(self, x_dim = 100, y_dim = 100, num_ants = 1):
        self.ant_world_x_dim = x_dim
        self.ant_world_y_dim = y_dim
        self.ant_world_population = num_ants
        self.ant_dict = dict()
        print ("Welcome to your new ant world a size of", x_dim, "by", y_dim, \
            "with a population of", num_ants)
        self.ant_world_array = np.zeros((y_dim, x_dim))
        # Create a mound dirt planet with air surrounding it
        for ind in range(x_dim):
            self.ant_world_array[0, ind] = AIR
            self.ant_world_array[y_dim-1, ind] = AIR
        for ind in range(y_dim):
            self.ant_world_array[ind, 0] = AIR
            self.ant_world_array[ind, x_dim-1] = AIR
        # Place the ant somewhere in air
        while(True):
            x_birth = random.randint(0, x_dim-1)
            y_birth = random.randint(0, y_dim-1)
            if ((self.ant_world_array[y_birth, x_birth]) == AIR):
                self.ant_world_array[y_birth, x_birth] = ANT 
                self.ant_dict[str(x_birth) + ',' + str(y_birth)] = [Ant(x_birth, y_birth, 'worker')]
                break
        print(self.ant_world_array)
        print("your ant is at", x_birth, y_birth)   
        

        #antlist make this a dictionary where hash is function of where it is? But then you need to change index constantly

#method to move ant within the world. Subtlety, after you lose ants from a location, there is still a spot in the dictionary with empty list as value         
    def add_ant_birth(self, x_loc, y_loc, ant_type = 'worker'):
        new_ant = Ant(x_loc, y_loc, ant_type)
        self.place_ant(x_loc, y_loc, new_ant)
        self.ant_world_population = self.ant_world_population + 1
        
    def remove_ant(self, ant):
        key_ant = ant.return_key()
        ant_array = self.ant_dict[key_ant]
        ant_array.remove(ant)
        if (not ant_array): #if no ants in that location, delete the dictionary entry
            del self.ant_dict[key_ant]
            
            
    #assume youre given a valid location on the board and the ant.
    def place_ant(self, x_loc, y_loc, ant):
        ant.x_ant_loc = x_loc
        ant.y_ant_loc = y_loc
        ant_key = ant.return_key()
        if ant_key in self.ant_dict:
            self.ant_dict[ant_key].append(ant)
        else:
            self.ant_dict[ant_key] = [ant]
            if self.ant_world_array[y_loc, x_loc] == DIRT:
                self.ant_world_array[y_loc, x_loc] = AIR
    
    def move_ant(self, ant, x_loc_final, y_loc_final):
        self.remove_ant(ant)
        self.place_ant(x_loc_final, y_loc_final, ant)
    
    def in_map(self, x_loc, y_loc):
        return (x_loc >= 0) and (x_loc < self.ant_world_x_dim) and (y_loc >= 0) and (y_loc < self.ant_world_y_dim)
            
    def move_ant_random(self, ant):
        while (True):
            #move = np.array([1, 0])
            move = random.randint(0,3)
            if (move == 0):
                if (self.in_map(ant.x_ant_loc + 1, ant.y_ant_loc + 0)):
                    self.move_ant(ant, ant.x_ant_loc + 1, ant.y_ant_loc + 0)
                    break
            elif (move == 1):
                if (self.in_map(ant.x_ant_loc, ant.y_ant_loc + 1)):
                    self.move_ant(ant, ant.x_ant_loc, ant.y_ant_loc + 1)
                    break
            elif (move == 2):
                if (self.in_map(ant.x_ant_loc - 1, ant.y_ant_loc)):
                    self.move_ant(ant, ant.x_ant_loc - 1, ant.y_ant_loc)
                    break
            else: 
                if (self.in_map(ant.x_ant_loc, ant.y_ant_loc - 1)):
                    self.move_ant(ant, ant.x_ant_loc, ant.y_ant_loc - 1)
                    break        
        
    def move_all_ants_random(self):
        ant_array = []
        for location in self.ant_dict:
            for ant in self.ant_dict[location]:
                ant_array.append(ant)
        for ant in ant_array:
            self.move_ant_random(ant)

if __name__=="__main__":
    print ("helloworld")
    block = 30
    pygame.init()
    ant_world_x_size = 15
    ant_world_y_size = 20
    ant_world_1 = AntWorld(ant_world_x_size, ant_world_y_size, 1)
    size = (ant_world_x_size * block, ant_world_y_size * block)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Ant Simulator")
    WHITE = (0xFF, 0xFF, 0xFF)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    screen.fill(WHITE)
    pygame.display.flip()
    for location in ant_world_1.ant_dict:
        for ant in ant_world_1.ant_dict[location]:
            print (ant)
    ant_world_1.add_ant_birth(1, 1)
    ant_world_1.add_ant_birth(1, 5)
    ant_world_1.add_ant_birth(1, 6)
    ant_world_1.add_ant_birth(1, 7)
    game_exit = False
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
        screen.fill(WHITE)
        pygame.draw.rect(screen, GREEN, [block, block, (ant_world_x_size - 2) * block, (ant_world_y_size -2) * block])
        for location in ant_world_1.ant_dict:
            for ant in ant_world_1.ant_dict[location]:
                print (ant)
                pygame.draw.rect(screen, BLACK, [block * ant.x_ant_loc, block * ant.y_ant_loc, block, block])
        pygame.display.update()
        time.sleep(1)
        ant_world_1.move_all_ants_random()