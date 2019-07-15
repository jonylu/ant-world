# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 19:11:58 2019

@author: jonyl
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 18:42:07 2019
drag and select
@author: jonyl
"""
import pygame

# --- constants --- (UPPER_CASE names)

SCREEN_WIDTH = 430
SCREEN_HEIGHT = 410

#BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

FPS = 30

# --- classses --- (CamelCase names)

# empty

# --- functions --- (lower_case names)

# empty

# --- main ---

# - init -

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#screen_rect = screen.get_rect()

pygame.display.set_caption("Tracking System")

# - objects -
ant1 = pygame.rect.Rect(176, 134, 17, 17)
ant1_selected = False

rectangle_draging = False
rectangle_appearing = False
rectangle = None
hand_jitter_x_lim = 5
hand_jitter_y_lim = 5
# - mainloop -

clock = pygame.time.Clock()

running = True

while running:

    # - events -

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:            
                if ant1_selected:
                    downclick_x, downclick_y = event.pos
                if (not rectangle_appearing): #creates a selection box, when nothing was selected
                    start_pos_mouse_x, start_pos_mouse_y = event.pos
                    rectangle = pygame.rect.Rect(start_pos_mouse_x, start_pos_mouse_y, 0, 0)
                    rectangle_appearing = True
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if ant1_selected: #the ant is selected, and this will click on the location for the ant to move.
                    end_pos_mouse_x, end_pos_mouse_y = event.pos
                    hand_jitter_x = abs(end_pos_mouse_x - downclick_x)
                    hand_jitter_y = abs(end_pos_mouse_y - downclick_y)
                    if (hand_jitter_x < hand_jitter_x_lim and hand_jitter_y < hand_jitter_y_lim):
                        ant1.centerx = end_pos_mouse_x
                        ant1.centery = end_pos_mouse_y
                    ant1_selected = False #the ant is in a new position and no longer selected
                    rectangle = None #otherwise the following rectangle code will run and change ant1_selected to True. You will then always have a selected ant that moves around
                if rectangle is not None: #makes sure selection box exists to detect collision
                    if rectangle.colliderect(ant1):
                        ant1_selected = True
                rectangle_appearing = False
                rectangle = None
        elif event.type == pygame.MOUSEMOTION: #if the select box has been created from the mouse click, the motion will change the selection box size.
            if rectangle_appearing:
                current_pos_mouse_x, current_pos_mouse_y = event.pos
                rectangle.w = current_pos_mouse_x - start_pos_mouse_x
                rectangle.h = current_pos_mouse_y - start_pos_mouse_y

                    

    # - updates (without draws) -

    # empty

    # - draws (without updates) -

    screen.fill(WHITE)
    if (rectangle is not None):
        pygame.draw.rect(screen, RED, rectangle, 1)
    if (ant1_selected):
        pygame.draw.rect(screen, (0, 0, 255), ant1)
    else:
        pygame.draw.rect(screen, (125, 125, 125), ant1)
    pygame.display.flip()

    # - constant game speed / FPS -

    clock.tick(FPS)

# - end -

pygame.quit()