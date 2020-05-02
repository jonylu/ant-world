# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 21:34:19 2019
#File that includes the Ant class as well as other creatures that we might include into our world.


@author: jonyl
"""
import numpy as np
import pygame
from dijkstrasalg import PathFind as pf

DIRT = 0
AIR = 1
ANT = 2
social_security = 0

#List of states
IDLE="idle"
MOVE="move"
DIG="dig"

def advance_simulator():
    print ("simulation advanced")

class Ant:
    def __init__(self,  start_pos = np.array([0, 0], dtype=np.float), ant_type = 'worker'):
        self.current_pos = start_pos
        self.is_blue = True
        self.ant_type = ant_type
        self.is_selected = False
        self.states = []
        global social_security
        self.ant_social_security = social_security
        social_security = social_security + 1
        
    def __str__(self):
        return ('(' + str(self.current_pos[0]) + ',' + str(self.current_pos[1]) + ')' + \
            ' ' + str(self.ant_social_security))
    
    
    def add_state(self, states):
        self.states.append(states)        
    
    def clear_states(self):
        self.states = []
    
    #if states list is empty.
    def is_idle(self):
        return (not self.states)
    
    def pop_next_state(self):
        if (self.states==[]):
            print("no commands left")
            return 0
        else:
            return (self.states.pop())
    def return_current_state(self):
        if (self.is_idle()):
            return IDLE
        return (self.states[-1][0])
    
    def return_next_dest(self):
        if (self.is_idle()):
            return self.current_pos
        else:
            return self.states[-1][1]
    
    def return_x_next_dest(self):
        coor = self.states[-1][1]
        return coor[0]
    
    def return_y_next_dest(self):
        coor = self.states[-1][1]
        return coor[1]
    
    def print_commands(self):
        print(self.states)
    
    def return_key(self):
        return (str(self.current_pos))

    def return_current_pos(self):
        return self.current_pos
    
    def return_x_current_pos(self):
        return self.current_pos[0]
    
    def return_y_current_pos(self):
        return self.current_pos[1]
    
    #def return_x_final_pos(self):
    #    return self.final_pos[0]
    
    #def return_y_final_pos(self):
    #    return self.final_pos[1]

    def increment_x_current_pos(self, incr):
        self.current_pos[0] += incr
        
    def increment_y_current_pos(self, incr):
        self.current_pos[1] += incr
    #only move one direction per advance simple
    def advance_simple(self):
        increment = 0.5
        print(self.current_pos)
        if (self.return_current_state() == MOVE):
            print(self.return_x_current_pos())
            print(self.return_x_next_dest())
            print(self.return_y_current_pos())
            print(self.return_y_next_dest())
            if self.return_x_current_pos() < self.return_x_next_dest():
                self.current_pos[0] += increment
                return
            if self.return_x_current_pos() > self.return_x_next_dest():
                self.current_pos[0] -= increment
                return
            if self.return_y_current_pos() < self.return_y_next_dest():
                self.current_pos[1] += increment
                print(self.return_current_state())
                return
            if self.return_y_current_pos() > self.return_y_next_dest():
                self.current_pos[1] -= increment
                return
            if (np.array_equal(self.current_pos, self.return_next_dest())):
                self.pop_next_state()      
        print(self.current_pos)
        return
    
    def add_path_to_states(self, path):
        for coor in path:
            self.states.append((MOVE, coor))
            
    def set_destination(self, grid, final_pos):
        p= pf(self.current_pos.astype(int), final_pos, grid)
        #path = p.uniform_cost_search()
        path = p.a_star_search()
        self.clear_states()
        self.add_path_to_states(path)
        self.final_pos = final_pos
    
    def set_current_pos(self, new_pos):
        self.current_pos = new_pos

"""
Running the game involves three different steps that must be done for this game. One is taking in user input. The second is updating the world in time. The third is the draw this world.
It relies on two different classes. The class that represents the ant world and the class that represents the user input.
"""     
def run_game():
    #start simulator
    #ant world
    input_ui(user_interface, ant_world)
    time_step(user_interface, ant_world)
    draw_world(user_interface, ant_world)
     
def ant_command_test(): 
    ant = Ant(np.array([100, 100]))
    ant.add_state((IDLE, np.array([98,98])))
    ant.add_state((MOVE, np.array([99,100])))
    ant.add_state((MOVE, np.array([98,100])))
    ant.add_state((MOVE, np.array([98,99])))
    ant.add_state((MOVE, np.array([98,98])))   
      
    ant.print_commands()
    print(ant.return_current_state())
    ant.print_commands()
    print(ant.return_current_state())
    ant.pop_next_state()
    ant.print_commands()
    print(ant.return_current_state())

def ant_add_path():
    ant = Ant(np.array([0,0]), 'worker')
    grid = np.zeros([5,10])
    grid[0:4,2:3]=DIRT
    last = np.array([9,4])
    ant.set_destination(grid, last)
    ant.print_commands()

def ant_add_path_medium():
    ant = Ant(np.array([0,0]), 'worker')
    grid = np.zeros([50,50])
    grid[0:4,2:3]=DIRT
    last = np.array([10,12])
    ant.set_destination(grid, last)
    ant.print_commands()

def ant_increment():
    ant = Ant(np.array([0,0], dtype= float), 'worker')    
    print(ant.return_current_pos())
    ant.increment_x_current_pos(3.5)
    print(ant.return_current_pos())
    
#if __name__=="__main__":
#    ant_increment()
     #ant_add_path_medium()   
#    ant_command_test()
#    #ant_add_path()
#    
#    pygame.init()
#    ant_init_pos_x = 30
#    ant_init_pos_y = 30
#    ant_final_pos_x = 30
#    ant_final_pos_y = 30
#    screen = pygame.display.set_mode((1000, 500))
#    done = False
#    ant_1 = Ant(np.array([ant_init_pos_x, ant_init_pos_y]))
#    clock = pygame.time.Clock()
#    while not done:
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                done = True
#            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
#                ant_1.toggle_color()
#            #if event.type == pygame.MOUSEMOTION:
#            #    print "mouse at (%d, %d)" % event.pos
#            if event.type == pygame.MOUSEBUTTONDOWN:
#                ant_1.set_destination(np.array([event.pos[0], event.pos[1]]))
#        pressed = pygame.key.get_pressed()
#        if pressed[pygame.K_UP]: ant_1.increment_y_current_pos(-3)
#        if pressed[pygame.K_DOWN]: ant_1.increment_y_current_pos(3)
#        if pressed[pygame.K_LEFT]: ant_1.increment_x_current_pos(-3) 
#        if pressed[pygame.K_RIGHT]: ant_1.increment_x_current_pos(3)
#        
#        ant_1.advance_simple()
#        
#        screen.fill((255, 255, 255))
#        if ant_1.is_blue: color = (0, 0, 0)
#        else: color = (255, 100, 0)
#        ant_grid_size = 10 #must be even
#        pygame.draw.rect(screen, color, pygame.Rect(ant_1.return_x_current_pos()-ant_grid_size/2, ant_1.return_y_current_pos()-ant_grid_size/2, ant_grid_size, ant_grid_size))      
#        pygame.display.flip()
#        clock.tick(60)