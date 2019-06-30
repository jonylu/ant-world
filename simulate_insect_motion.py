# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 21:34:19 2019

@author: jonyl
"""
import numpy as np
import pygame

DIRT = 0
AIR = 1
ANT = 2
social_security = 0


def advance_simulator():
    print ("simulation advanced")

class Ant:
    def __init__(self,  start_pos = np.array([0, 0]), ant_type = 'worker'):
        self.current_pos = start_pos
        self.is_blue = True
        self.current_pos = start_pos
        self.final_pos = start_pos
        self.ant_type = ant_type
        self.is_selected = False
        global social_security
        self.ant_social_security = social_security
        social_security = social_security + 1
        
    def __str__(self):
        return ('(' + str(self.current_pos[0]) + ',' + str(self.current_pos[1]) + ')' + \
            ' ' + str(self.ant_social_security))
    
    def return_key(self):
        return (str(self.current_pos))
    
    def return_x_current_pos(self):
        return self.current_pos[0]
    
    def return_y_current_pos(self):
        return self.current_pos[1]
    
    def return_x_final_pos(self):
        return self.final_pos[0]
    
    def return_y_final_pos(self):
        return self.final_pos[1]

    def increment_x_current_pos(self, incr):
        self.current_pos[0] += incr
        
    def increment_y_current_pos(self, incr):
        self.current_pos[1] += incr
    
    def advance_simple(self):
        if self.return_x_current_pos() < self.return_x_final_pos():
            self.current_pos[0] += 1
        if self.return_x_current_pos() > self.return_x_final_pos():
            self.current_pos[0] -= 1
        if self.return_y_current_pos() < self.return_y_final_pos():
            self.current_pos[1] += 1
        if self.return_y_current_pos() > self.return_y_final_pos():
            self.current_pos[1] -= 1   
            
    def set_destination(self, final_pos):
        self.final_pos = final_pos
        
    def toggle_color(self):
        self.is_blue = not self.is_blue
    
    def toggle_selected(self):
        self.is_selected = not self.is_selected
        
if __name__=="__main__":
    pygame.init()
    ant_init_pos_x = 30
    ant_init_pos_y = 30
    ant_final_pos_x = 30
    ant_final_pos_y = 30
    screen = pygame.display.set_mode((1000, 500))
    done = False
    ant_1 = Ant(np.array([ant_init_pos_x, ant_init_pos_y]))
    clock = pygame.time.Clock()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                ant_1.toggle_color()
            #if event.type == pygame.MOUSEMOTION:
            #    print "mouse at (%d, %d)" % event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                ant_1.set_destination(np.array([event.pos[0], event.pos[1]]))
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: ant_1.increment_y_current_pos(-3)
        if pressed[pygame.K_DOWN]: ant_1.increment_y_current_pos(3)
        if pressed[pygame.K_LEFT]: ant_1.increment_x_current_pos(-3) 
        if pressed[pygame.K_RIGHT]: ant_1.increment_x_current_pos(3)
        
        ant_1.advance_simple()
        
        screen.fill((255, 255, 255))
        if ant_1.is_blue: color = (0, 0, 0)
        else: color = (255, 100, 0)
        ant_grid_size = 10 #must be even
        pygame.draw.rect(screen, color, pygame.Rect(ant_1.return_x_current_pos()-ant_grid_size/2, ant_1.return_y_current_pos()-ant_grid_size/2, ant_grid_size, ant_grid_size))      
        pygame.display.flip()
        clock.tick(60)