# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 19:53:04 2020

@author: jonyl
"""
import pygame

WHITE = (255, 255, 255)
NUM_MOVE_SPRITE_STATES= 4

class AntSprite(pygame.sprite.Sprite):
    def __init__(self, pixel_pos_x, pixel_pos_y, pixel_size_x, pixel_size_y):
        super(AntSprite, self).__init__()
        #pygame.sprite.Sprite.__init__(self)
        #adding all the images to sprite array
        self.images = []
        self.images.append(pygame.image.load('ant_50_pix_1_n.png'))
        self.images.append(pygame.image.load('ant_50_pix_2_n.png'))
        self.images.append(pygame.image.load('ant_50_pix_3_n.png'))
        self.images.append(pygame.image.load('ant_50_pix_4_n.png'))
        self.images.append(pygame.image.load('ant_50_pix_1_s_w.png'))
        self.images.append(pygame.image.load('ant_50_pix_2_s_w.png'))
        self.images.append(pygame.image.load('ant_50_pix_3_s_w.png'))
        self.images.append(pygame.image.load('ant_50_pix_4_s_w.png'))
        #index value to get the image from the array
        #initially it is 0 
        self.index = 0

        #now the image that we will display will be the index from the image array 
        self.image = self.images[self.index]

        #creating a rect at position x,y (5,5) of size (150,198) which is the size of sprite 
        self.rect = pygame.Rect(pixel_pos_x, pixel_pos_y, pixel_size_x, pixel_size_y)
        self.selected = True

    def update(self):
        self.index += 1       
        if ((self.index % NUM_MOVE_SPRITE_STATES) == 0):
            if (self.index == NUM_MOVE_SPRITE_STATES):
                self.index = 0
            if (self.index == 2*NUM_MOVE_SPRITE_STATES):
                self.index = NUM_MOVE_SPRITE_STATES    

        if ((not self.selected) and self.index >= NUM_MOVE_SPRITE_STATES):
            self.index -= NUM_MOVE_SPRITE_STATES
        if (self.selected and self.index < NUM_MOVE_SPRITE_STATES):
            self.index += NUM_MOVE_SPRITE_STATES
        print (self.index)
        self.image = self.images[self.index]
 
        

if __name__ == '__main__':
    #initializing pygame
    pygame.init()

    #getting the screen of the specified size
    screen = pygame.display.set_mode([200,200])

    #creating our sprite object
    my_sprite = AntSprite(100,100,50,50)

    #creating a group with our sprite
    my_group = pygame.sprite.Group(my_sprite)

    #getting the pygame clock for handling fps
    clock = pygame.time.Clock()

    while True:
        #getting the events
        for event in pygame.event.get():
    
            #if the event is quit means we clicked on the close window button
            if event.type == pygame.QUIT:
                #quit the game
                pygame.quit()
                quit()
    
        #updating the sprite
        my_group.update()

        #filling the screen with background color
        screen.fill(WHITE)

        #drawing the sprite
        my_group.draw(screen)

        #updating the display
        pygame.display.update()
        #pygame.display.flip()

        #finally delaying the loop to with clock tick for 10fps 
        clock.tick(5)
        print(clock.get_time())