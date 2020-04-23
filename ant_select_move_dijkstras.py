# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 18:42:07 2019

@author: Jonathan Lu
Update the ant select and move with dijkstras algorithm to include some brains into ant moving. That way you can add dirt and the ant has to move around it.
Drag to create selection box to select an ant. Once ant is selected, left-click on a location to transport ant instantaneously. Works with one button mouse.
Will try to have a fine grid as well as a course grid. The fine grid allows small resolution movement while course grid determines where the ant will land. 

"""
import pygame
from insects import Ant
import numpy as np

# --- constants --- (UPPER_CASE names)
DIRT = 1
AIR = 0
ANT = 2


#grid = np.zeros([50, 50])
grid = np.zeros([20,20])

grid[3:15,3:15] = DIRT
#BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
BROWN = (165,42,42)
FPS = 30

CELL_SIZE= 50

ANT_GRAPHIC_SIZE = 50

SCREEN_WIDTH = CELL_SIZE * np.shape(grid)[1]
SCREEN_HEIGHT = CELL_SIZE * np.shape(grid)[0]


#Graphics pixel should be converted to the grid coordinates for the ant.
def pixel_to_coor(pixel):
    return (np.floor(pixel / CELL_SIZE)).astype(int)

#Coor of ants can be converted to pixel units for plotting. Interface between ant grid world to the graphics world. Coor in this case can be integers, or also floats to indicate moving between grids.
def coor_to_pixel(coor):
    return CELL_SIZE/2 + coor * CELL_SIZE
    
class AntGraphic:
    def __init__(self,  ant):
        self.ant = ant
        self.selected = False #whether the ant is selected
        self.color = "Blue" 
        self.graphic = pygame.rect.Rect(coor_to_pixel((self.ant).return_x_current_pos())-np.floor(ANT_GRAPHIC_SIZE/2), coor_to_pixel((self.ant).return_y_current_pos())-np.floor(ANT_GRAPHIC_SIZE/2), ANT_GRAPHIC_SIZE, ANT_GRAPHIC_SIZE)
        
    def deselect(self):
        self.selected = False
    def select(self):
        self.selected = True
    def update_ant_graphic(self):
        self.graphic = pygame.rect.Rect(coor_to_pixel((self.ant).return_x_current_pos())-np.floor(ANT_GRAPHIC_SIZE/2), coor_to_pixel((self.ant).return_y_current_pos())-np.floor(ANT_GRAPHIC_SIZE/2), ANT_GRAPHIC_SIZE, ANT_GRAPHIC_SIZE)
    def is_selected(self):
        return self.selected
    def return_graphic(self):
        return self.graphic

class AntSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(AntSprite, self).__init__()
        #adding all the images to sprite array
        self.images = []
        self.images.append(pygame.image.load('ant_20_pix.png'))
        self.images.append(pygame.image.load('ant_20_pix-2.png'))

        #index value to get the image from the array
        #initially it is 0 
        self.index = 0

        #now the image that we will display will be the index from the image array 
        self.image = self.images[self.index]

        #creating a rect at position x,y (5,5) of size (150,198) which is the size of sprite 
        self.rect = pygame.Rect(5, 5, 20, 20)

    def update(self):
        #when the update method is called, we will increment the index
        self.index += 1

        #if the index is larger than the total images
        if self.index >= len(self.images):
            #we will make the index to 0 again
            self.index = 0
        
        #finally we will update the image that will be displayed
        self.image = self.images[self.index]

class UserInterface:
    def __init__(self, id):
        self.user_id = id
    def is_left_click(self, user_event):
        return user_event.button == 1
    def is_right_click(self, user_event):
        return user_event.button == 3

class SelectionBox:
    def __init__(self, start_pos_mouse_x, start_pos_mouse_y, size_x, size_y):
        self.rectangle = pygame.rect.Rect(start_pos_mouse_x, start_pos_mouse_y, size_x, size_y)
        self.visible = False
    def set_size(self, size_x, size_y):
        self.rectangle.w = size_x
        self.rectangle.h = size_y
    def set_origin(self, pos_x, pos_y):
        (self.rectangle).x = pos_x
        (self.rectangle).y = pos_y
    def set_invisible(self):
        self.visible = False
    def set_visible(self):
        self.visible = True
    def reset_box(self):
        self.set_invisible()
        self.set_size(0, 0)
    def is_visible(self):
        return self.visible
    def return_origin_x(self):
        return (self.rectangle).x
    def return_origin_y(self):
        return (self.rectangle).y
    def return_size_x(self):
        return (self.rectangle).w
    def return_size_y(self):
        return (self.rectangle).h
    def return_rectangle(self):
        return (self.rectangle)

pygame.init()
modes = pygame.display.list_modes(16)
#screen = pygame.display.set_mode((1920,1080),pygame.FULLSCREEN)
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Tracking System")

# - objects -
ant1 = Ant(np.array([2,2], dtype=float),'worker')
ant_graphic_1 = AntGraphic(ant1)
select_box = SelectionBox(0, 0, 0, 0)
ui = UserInterface(1)
# - mainloop -

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if ui.is_left_click(event):            
                if ant_graphic_1.is_selected():
                    downclick_x, downclick_y = event.pos
                if (not select_box.is_visible()): #creates a selection box, when nothing was selected
                    start_pos_mouse_x, start_pos_mouse_y = event.pos
                    select_box.set_origin(start_pos_mouse_x, start_pos_mouse_y)
                    select_box.set_visible()
            if ui.is_right_click(event):
                if ant_graphic_1.is_selected():
                    downclick_x, downclick_y = event.pos
                    dest_x_coor, dest_y_coor = pixel_to_coor(np.array([downclick_x, downclick_y]))
                    print('destination coor')
                    ##################WORKING HERE START HERE 04/14/2020
                    print([dest_x_coor, dest_y_coor])
                    ant1.set_destination(grid, np.array([dest_x_coor, dest_y_coor]))
        elif event.type == pygame.MOUSEBUTTONUP:
            if ui.is_left_click(event):
                if select_box.is_visible(): #makes sure selection box exists to detect collision
                    if select_box.return_rectangle().colliderect(ant_graphic_1.return_graphic()):
                        ant_graphic_1.select()
                    else:
                        ant_graphic_1.deselect()
                    select_box.reset_box()
                else: #click outside the ant1, ant1 not selected anymore
                    ant_graphic_1.select()
        elif event.type == pygame.MOUSEMOTION: #if the select box has been created from the mouse click, the motion will change the selection box size.
            if select_box.is_visible():
                current_pos_mouse_x, current_pos_mouse_y = event.pos
                select_box.set_size(current_pos_mouse_x - select_box.return_origin_x(), current_pos_mouse_y - select_box.return_origin_y()) 

    # - updates (without draws) -

    # empty
    ant1.advance_simple()
    
    ant_graphic_1.update_ant_graphic()

    # - draws (without updates) -

    screen.fill(WHITE)
    for x_grid in range(np.shape(grid)[1]):
        for y_grid in range(np.shape(grid)[0]):
            if (grid[y_grid,x_grid]==DIRT):
                pygame.draw.rect(screen, BROWN, pygame.rect.Rect(coor_to_pixel(x_grid)-np.floor(CELL_SIZE/2), coor_to_pixel(y_grid)-np.floor(CELL_SIZE/2), CELL_SIZE, CELL_SIZE))
    
    if (select_box.is_visible()):
        pygame.draw.rect(screen, RED, select_box.return_rectangle(), 1)
    if (ant_graphic_1.is_selected()):
        pygame.draw.rect(screen, (0, 0, 255), ant_graphic_1.return_graphic())
    else:
        pygame.draw.rect(screen, (125, 125, 125), ant_graphic_1.return_graphic())
    pygame.display.flip()
    # - constant game speed / FPS -

    clock.tick(FPS)

# - end -

pygame.quit()