# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 21:34:19 2019

@author: jonyl
"""
import numpy as np
from antworldsimulator import Ant
from antworldsimulator import AntWorld
import pygame

def advance_simulator():
    print ("simulation advanced")
    

class Simulator:
    def __init__(self, start_loc = np.array([0, 0]), final_loc = np.array([0, 0])):
        self.is_blue = True
        self.current_loc = start_loc
        self.final_loc = final_loc
    def return_current_pos(self):
        return self.current_loc
    def return_final_pos(self):
        return self.final_loc
    def return_x_current(self):
        return self.current_loc[0]
    def return_y_current(self):
        return self.current_loc[1]
    def return_x_final(self):
        return self.final_loc[0]
    def return_y_final(self):
        return self.final_loc[1]
    
    def increment_x_current(self, incr):
        self.current_loc[0] += incr
    def increment_y_current(self, incr):
        self.current_loc[1] += incr
    
    def advance_simple(self):
        if self.return_x_current() < self.return_x_final():
            self.current_loc[0] += 1
        if self.return_x_current() > self.return_x_final():
            self.current_loc[0] -= 1
        if self.return_y_current() < self.return_y_final():
            self.current_loc[1] += 1
        if self.return_y_current() > self.return_y_final():
            self.current_loc[1] -= 1   
    def set_destination(self, final_loc):
        self.final_loc = final_loc
        
    def toggle_color(self):
        self.is_blue = not self.is_blue
        
if __name__=="__main__":
    pygame.init()
    screen = pygame.display.set_mode((1000, 500))
    done = False
    sim_1 = Simulator(np.array([30,30]), np.array([30,30]))

    clock = pygame.time.Clock()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                sim_1.toggle_color()
            #if event.type == pygame.MOUSEMOTION:
            #    print "mouse at (%d, %d)" % event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                sim_1.set_destination(np.array([event.pos[0], event.pos[1]]))
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: sim_1.increment_y_current(-3)
        if pressed[pygame.K_DOWN]: sim_1.increment_y_current(3)
        if pressed[pygame.K_LEFT]: sim_1.increment_x_current(-3) 
        if pressed[pygame.K_RIGHT]: sim_1.increment_x_current(3)
        
        sim_1.advance_simple()
        
        screen.fill((255, 255, 255))
        if sim_1.is_blue: color = (0, 0, 0)
        else: color = (255, 100, 0)
        ant_grid_size = 10 #must be even
        pygame.draw.rect(screen, color, pygame.Rect(sim_1.return_x_current()-ant_grid_size/2, sim_1.return_y_current()-ant_grid_size/2, ant_grid_size, ant_grid_size))      
        pygame.display.flip()
        clock.tick(60)