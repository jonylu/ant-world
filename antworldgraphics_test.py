# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 21:34:19 2019

@author: jonyl
"""

from antworldsimulator import Ant
from antworldsimulator import AntWorld
import pygame

def advance_simulator():
    print ("simulation advanced")
    

class Simulator:
    def __init__(self):
        self.is_blue = True
        self.x_current = 30
        self.y_current = 30
        self.x_final = 30
        self.y_final = 30
    
    def advance(self):
        if self.x_current < self.x_final:
            self.x_current += 1
        if self.x_current > self.x_final:
            self.x_current -= 1
        if self.y_current < self.y_final:
            self.y_current += 1
        if self.y_current > self.y_final:
            self.y_current -= 1
    
    def set_destination(self, x, y):
        self.x_final = x
        self.y_final = y
        
    def toggle_color(self):
        self.is_blue = not self.is_blue
        
if __name__=="__main__":
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    done = False
    sim_1 = Simulator()

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
                sim_1.set_destination(event.pos[0], event.pos[1])
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: sim_1.y_current -= 3
        if pressed[pygame.K_DOWN]: sim_1.y_current += 3
        if pressed[pygame.K_LEFT]: sim_1.x_current -= 3
        if pressed[pygame.K_RIGHT]: sim_1.x_current += 3
        
        sim_1.advance()
        
        screen.fill((0, 0, 0))
        if sim_1.is_blue: color = (0, 128, 255)
        else: color = (255, 100, 0)
        pygame.draw.rect(screen, color, pygame.Rect(sim_1.x_current-30, sim_1.y_current-30, 60, 60))
        
        pygame.display.flip()
        clock.tick(60)