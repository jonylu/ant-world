# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 20:57:01 2020

@author: jonyl
"""

import numpy as np
import distance_metrics
import math
from graphelem import PathNode
import priorityqueue as pq 
import time
import pygame

# --- constants --- (UPPER_CASE names)
DIRT = 1
AIR = 0
ANT = 2


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED   = (255, 0, 0)
BROWN = (165,42,42)
BLUE = (0,0,255)
FPS = 30

CELL_SIZE= 20

CIRCLE_SIZE= 10

#Graphics pixel should be converted to the grid coordinates for the ant.
def pixel_to_coor(pixel):
    return (np.floor(pixel / CELL_SIZE)).astype(int)

#Coor of ants can be converted to pixel units for plotting. Interface between ant grid world to the graphics world. Coor in this case can be integers, or also floats to indicate moving between grids.
def coor_to_pixel(coor):
    return CELL_SIZE/2 + coor * CELL_SIZE


def draw_node(self, pygame, vispathfind, pnode):
    coor = vispathfind.index_to_coor(pnode.return_node_name())
    x_coor = coor[0]
    y_coor = coor[1]
    #self.rect = pygame.rect.Rect(coor_to_pixel(x_coor)-np.floor(/2), coor_to_pixel((self.ant).return_y_current_pos())-np.floor(ANT_GRAPHIC_SIZE/2), ANT_GRAPHIC_SIZE, ANT_GRAPHIC_SIZE)
         
    

class VisualizePathFind:
    #start_coor, end_coor is numpy array of two numbers, grid is a numpy 2d array.
    def __init__(self, start_coor, end_coor, grid):
        self.start = start_coor
        self.end = end_coor
        self.grid = np.transpose(grid)

    def grid_type(self, coor):
        return self.grid[self.x_coor(coor), self.y_coor(coor)]

    def edge_distance_manhatten(self, coor1, coor2):
        if (distance_metrics.manhatten_distance(coor1,coor2)==0):
            return 0
        elif (distance_metrics.manhatten_distance(coor1,coor2)==1):
            if(self.grid_type(coor1)==AIR and self.grid_type(coor2)==AIR):
                return 1
            if(self.grid_type(coor1)==DIRT or self.grid_type(coor2)==DIRT):
                return 200
        else:
            return math.inf

    #In this function you think about internet matrix shape. [x, y]
    def index_to_coor(self, index):
        return np.array([index // self.y_size(), index % self.y_size()])
    
    def coor_to_index(self, coor):
        return self.y_size()* self.x_coor(coor) + self.y_coor(coor)
    
    def x_size(self):
        return np.shape(self.grid)[0]
    
    def y_size(self):
        return np.shape(self.grid)[1]

    def x_coor(self, coor):
        return coor[0]

    def y_coor(self, coor):
        return coor[1]
    
    def edge_matrix(self):
        edge_mat = np.zeros([self.x_size()*self.y_size(),self.x_size()*self.y_size()])
        for pt1_index in range(np.shape(edge_mat)[0]):
            for pt2_index in range(pt1_index, np.shape(edge_mat)[1]):
                edge_mat[pt1_index][pt2_index]=self.edge_distance_manhatten(self.index_to_coor(pt1_index), self.index_to_coor(pt2_index))
                edge_mat[pt2_index][pt1_index]=edge_mat[pt1_index][pt2_index] #redundant when pt1_index == pt2_index
        return edge_mat

    def initialize_distance_mat(self, start_coor, edge_mat):
        dist_mat = np.zeros(np.shape(edge_mat)[0])
        dist_mat[:] = math.inf
        dist_mat[self.coor_to_index(start_coor)]  = 0
        return dist_mat

        #returns path nodes from start_coor to end_coor backwards.
    def dijkstra(self):
        edge_mat = self.edge_matrix()
        dist_mat = self.initialize_distance_mat(self.start, edge_mat)
        visited = []
        previous = self.initialize_prev_vector_with_neg_ones()
        #previous[coor_to_index(start_coor, grid)] = 0
        start_index = self.coor_to_index(self.start)
        current_index = start_index
        end_index = self.coor_to_index(self.end)
        visited.append(current_index)
        while (len(visited) != self.x_size()*self.y_size()):
        #while(not(end_index in visited)):
            minimum_dist = math.inf
            new_node = 0 #set arbitrarily
            for test_index in range(len(edge_mat)):
                d = dist_mat[current_index] + edge_mat[current_index][test_index]
                if(d<dist_mat[test_index] and not(test_index in visited)):
                    dist_mat[test_index] = d
                    previous[test_index] = current_index
                if(minimum_dist > dist_mat[test_index] and not(test_index in visited)): 
                    minimum_dist = dist_mat[test_index] #why does =d not work?
                    new_node = test_index
            current_index = new_node
            visited.append(current_index)
        backtrack_node = end_index
        path_array= []
        while(backtrack_node != -1):
            path_array.append(backtrack_node)
            backtrack_node = previous[backtrack_node]
        #path_array = path_array[::-1] reverses the array
        return [self.index_to_coor(index) for index in path_array] 
    #initialize vector indicating the previous matrix of a path
    def initialize_prev_vector_with_neg_ones(self):
        previous = np.zeros(self.x_size()*self.y_size(), dtype=int)
        previous[:] = -1
        return previous
    
   
    def uniform_cost_search(self):
        start_index = self.coor_to_index(self.start)
        current_index = start_index
        edge_mat = self.edge_matrix()
        
        end_index = self.coor_to_index(self.end)
        previous = self.initialize_prev_vector_with_neg_ones() #traces the previous path
        visited = pq.PriorityQueueList() #there is no reason to use priority queue here, mainly for convenenience
        frontier= pq.PriorityQueueList() #vector of inifinty
        frontier.insert(0, current_index)
        counter=0
        while True:
            #print("frontier")
            #print(counter)
            #frontier.print_pq()
            
            #print("visited")
            #visited.print_pq()
            if (not frontier):
                print("failure")
                return
            current_node = frontier.pop()
            if (current_node.return_node_name() == end_index): #hit state, found your final state, break loop
                break 
            if (not visited.is_present(current_node)): #add node state to explored if not there already
                visited.insert(current_node.return_node_priority(), current_node.return_node_name())
                #visited.print_pq()
            for child_node in self.create_child_nodes(current_node, edge_mat):
                if (not (visited.is_present(child_node)) and not (frontier.is_present(child_node))):
                    frontier.insert(child_node.return_node_priority(), child_node.return_node_name())
                    previous[child_node.return_node_name()] = current_node.return_node_name()
                elif (frontier.is_present(child_node)):
                    if (child_node.return_node_priority() < frontier.find_node(child_node).return_node_priority()):
                        frontier.replace_node(child_node)#remove the old path and put in the new child_node into frontier with a more optimal path cost
                        previous[child_node.return_node_name()] = current_node.return_node_name()
            counter = counter + 1
            for node in frontier.return_list_nodes():
                plot_index_node(screen, vpf, node.return_node_name(), color = BLUE)
            for node in visited.return_list_nodes():
                plot_index_node(screen, vpf, node.return_node_name(), color = RED)
            plot_index_node(screen, vpf, start_index, color = BLACK)
            plot_index_node(screen, vpf, end_index, color = BLACK)
            pygame.display.flip()
            clock.tick(5)
            #print("frontier")
            #frontier.print_pq()
        #after while loop either you have a current_index
        backtrack_node = end_index
        path_array= []
        while(backtrack_node != -1):
            path_array.append(backtrack_node)
            backtrack_node = previous[backtrack_node]
            plot_index_node(screen, vpf, backtrack_node, color = BLACK)
        pygame.display.flip()
        #path_array = path_array[::-1] reverses the array
        return [self.index_to_coor(index) for index in path_array] 
    
    def a_star_search(self):
        start_index = self.coor_to_index(self.start)
        current_index = start_index
        edge_mat = self.edge_matrix()
        
        end_index = self.coor_to_index(self.end)
        previous = self.initialize_prev_vector_with_neg_ones() #traces the previous path
        visited = pq.PriorityQueueList() #there is no reason to use priority queue here, mainly for convenenience
        frontier= pq.PriorityQueueList() #vector of inifinty
        heuristic = self.euclidean_heuristic(end_index)
        path_cost_array = np.zeros(self.x_size()*self.y_size())
        path_cost_array = path_cost_array + math.inf #create path_cost matrix as map of infinity
        #heuristic = np.zeros(self.x_size()*self.y_size())
        path_cost_array[current_index] = 0
        frontier.insert(path_cost_array[current_index] + heuristic[current_index], current_index)
        counter = 0 
        while True:
            #print("frontier")
            #print(counter)
            #frontier.print_pq()
            #print("visited")
            #visited.print_pq()
            
            if (not frontier):
                print("failure")
                return
            current_node = frontier.pop()
            if (current_node.return_node_name() == end_index): #hit state, found your final state, break loop
                break 
            if (not visited.is_present(current_node)): #add node state to explored if not there already
                visited.insert(current_node.return_node_priority(), current_node.return_node_name())
            path_cost_array, potential_child_nodes = self.create_child_nodes_with_heuristic(current_node, edge_mat, end_index, heuristic, path_cost_array)
            for child_node in potential_child_nodes:
                if (not (visited.is_present(child_node)) and not (frontier.is_present(child_node))):
                    frontier.insert(child_node.return_node_priority(), child_node.return_node_name())
                    previous[child_node.return_node_name()] = current_node.return_node_name()
                elif (frontier.is_present(child_node)):
                    if (child_node.return_node_priority() < frontier.find_node(child_node).return_node_priority()):
                        frontier.replace_node(child_node)#remove the old path and put in the new child_node into frontier with a more optimal path cost
                        previous[child_node.return_node_name()] = current_node.return_node_name()
            counter = counter + 1
            for node in frontier.return_list_nodes():
                plot_index_node(screen, vpf, node.return_node_name(), color = BLUE)
            for node in visited.return_list_nodes():
                plot_index_node(screen, vpf, node.return_node_name(), color = RED)
            plot_index_node(screen, vpf, start_index, color = BLACK)
            plot_index_node(screen, vpf, end_index, color = BLACK)
            pygame.display.flip()
            clock.tick(5)
        #after while loop either you have a current_index
        backtrack_node = end_index
        path_array= []
        while(backtrack_node != -1):
            path_array.append(backtrack_node)
            backtrack_node = previous[backtrack_node]
            plot_index_node(screen, vpf, backtrack_node, color = BLACK)
        #path_array = path_array[::-1] reverses the array
        pygame.display.flip()
        return [self.index_to_coor(index) for index in path_array] 


    #create child nodes assuming that 
    def create_child_nodes(self, current_node, edge_mat): 
        curr_path_cost = current_node.return_node_priority()
        node_name = current_node.return_node_name()
        node_coor = self.index_to_coor(node_name)
        child_nodes = []
        for state_shift in [(-1, 0), (1, 0), (0,1), (0,-1)]:
            next_coor = node_coor + state_shift
            #print(next_coor)
            if (all(next_coor>=0) and all(next_coor < (self.x_size(), self.y_size()))): #inbounds then add
                child_nodes.append(PathNode(curr_path_cost + edge_mat[node_name][self.coor_to_index(next_coor)],self.coor_to_index(next_coor)))
        return child_nodes
    
    def create_child_nodes_with_heuristic(self, current_node, edge_mat, end_index, heuristic, path_cost_array): 
        updated_path_cost_array = path_cost_array
        node_name = current_node.return_node_name()
        node_coor = self.index_to_coor(node_name)
        child_nodes = []
        #end_coor = self.index_to_coor(end_index)
        for state_shift in [(-1, 0), (1, 0), (0,1), (0,-1)]:
            next_coor = node_coor + state_shift
            if (all(next_coor>=0) and all(next_coor < (self.x_size(), self.y_size()))): #inbounds then add
                next_coor_index = self.coor_to_index(next_coor)
                new_path_cost = path_cost_array[node_name] + edge_mat[node_name][next_coor_index]               
                if (new_path_cost < path_cost_array[next_coor_index]): #if the new path cost is smaller than the old path cost, then replace with new path cost in array
                    updated_path_cost_array[next_coor_index] = new_path_cost
                else: #if you don't have a better path then there is no way you could beat the past path because the heuristic would be the same
                    continue
                g = updated_path_cost_array[next_coor_index] 
                h = heuristic[next_coor_index]
                child_nodes.append(PathNode( g + h, next_coor_index))
        return updated_path_cost_array, child_nodes
    
    def manhatten_heuristic(self, end_index, scale = 1):
        heuristic_len = self.x_size()*self.y_size()
        heuristic = np.zeros(heuristic_len)
        end_coor = self.index_to_coor(end_index)
        for index in range(heuristic_len):
            coor = self.index_to_coor(index)
            heuristic[index] = scale * distance_metrics.manhatten_distance(coor, end_coor)
        return heuristic
    
    def euclidean_heuristic(self, end_index, scale = 1):
        heuristic_len = self.x_size()*self.y_size()
        heuristic = np.zeros(heuristic_len)
        end_coor = self.index_to_coor(end_index)
        for index in range(heuristic_len):
            coor = self.index_to_coor(index)
            heuristic[index] = scale * distance_metrics.euclidean_distance(coor, end_coor)
        return heuristic
    
def test_child_nodes():
    source =np.array([0,0])
    dest = np.array([9,4])
    grid = np.zeros([5,10])
    grid[1:3, 1:4] = DIRT
    p = PathFind(source, dest, grid)
    x=PathNode(0,2)
    child_nodes = p.create_child_nodes(x)
    for child in child_nodes:
        print(child)

def simple_dijkstras_test():
    print("Running simple dijkstras test")
    source =np.array([0,0])
    dest = np.array([9,4])
    grid = np.zeros([5,10])
    grid[1:3, 1:4] = DIRT
    p = PathFind(source, dest, grid)
    path = p.dijkstra()   
    print(path)    
    
def larger_dijkstras_test():
    print("Running large dijkstras test")
    grid = np.zeros([26,30])
    grid[10:20, 10:20]=DIRT
    grid[24:25,0:3] = DIRT
    grid[0,2] = DIRT

    source =np.array([0,0])
    dest = np.array([18,25])
    p = PathFind(source, dest, grid)
    path = p.dijkstra()
    print(path)
    
def larger_uniform_cost_search_test():
    print("Running large uniform cost")
    grid = np.zeros([26,30])
    grid[10:20, 10:20]=DIRT
    grid[24:25,0:3] = DIRT
    grid[0,2] = DIRT

    source =np.array([0,0])
    dest = np.array([18,25])
    p = PathFind(source, dest, grid)
    path = p.uniform_cost_search()
    print(path)

def simple_uniform_cost_search_test():
    print("Running simple uniform cost search")
    source =np.array([0,0])
    dest = np.array([9,4])
    grid = np.zeros([5,10])
    grid[1:3, 1:4] = DIRT
    p = PathFind(source, dest, grid)
    path = p.uniform_cost_search()   
    print(path)  
    
def simple_a_star_cost_search_test():
    print("Running simple a star")
    source =np.array([0,0])
    dest = np.array([9,4])
    grid = np.zeros([5,10])
    grid[1:3, 1:4] = DIRT
    p = PathFind(source, dest, grid)
    path = p.a_star_search()   
    print(path)  

def larger_a_star_test():
    print("Running larger a star test")
    grid = np.zeros([26,30])
    grid[10:20, 10:20]=DIRT
    grid[24:25,0:3] = DIRT
    grid[0,2] = DIRT

    source =np.array([0,0])
    dest = np.array([18,25])
    p = PathFind(source, dest, grid)
    path = p.a_star_search()
    print(path) 
    
def baby_a_star_test():
    print("running baby a star")
    grid = np.zeros([7,7])
    source = np.array([2,2])
    dest = np.array([6,6])
    p = PathFind(source, dest, grid)
    path = p.a_star_search()  
    print(path)
    
def baby_uniform_test():
    print("running baby uniform")
    grid = np.zeros([7,7])
    source = np.array([2,2])
    dest = np.array([6,6])
    p = PathFind(source, dest, grid)
    path = p.uniform_cost_search()  
    print(path)
    
def time_comparison():
    starttime = time.time()
    simple_uniform_cost_search_test()
    print(time.time()-starttime) 
 
    starttime = time.time()
    simple_dijkstras_test()
    print(time.time()-starttime)

    starttime = time.time()
    simple_a_star_cost_search_test()
    print(time.time()-starttime)

    starttime = time.time()
    larger_uniform_cost_search_test()
    print(time.time()-starttime) 
    
    starttime = time.time()
    larger_dijkstras_test()
    print(time.time()-starttime)
    
    starttime = time.time()
    larger_a_star_test()
    print(time.time()-starttime)

def comparison_a_star_uniform():
    baby_uniform_test()
    baby_a_star_test()


def plot_node(scr, x_coor, y_coor, color = BLUE):
    pygame.draw.circle(scr, color, (int(coor_to_pixel(x_coor)), int(coor_to_pixel(y_coor))), int(CELL_SIZE/2))

def plot_index_node(scr, vpf, index, color = BLUE):
    coor = vpf.index_to_coor(index)
    x_coor = coor[0]
    y_coor = coor[1]
    pygame.draw.circle(scr, color, (int(coor_to_pixel(x_coor)), int(coor_to_pixel(y_coor))), int(CELL_SIZE/2))
  

if __name__ == '__main__':
    #initializing pygame
    pygame.init()

    #grid = np.zeros([30,30])
    #grid[10:20,10:20] = DIRT
    #source = np.array([4,6])
    #dest = np.array([25,25])

    grid = np.zeros([15,15])
    grid[5:10,5:10] = DIRT
    source = np.array([2,2])
    dest = np.array([12,12])    
    
    SCREEN_WIDTH = CELL_SIZE * np.shape(grid)[1]
    SCREEN_HEIGHT = CELL_SIZE * np.shape(grid)[0]

    #getting the screen of the specified size
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    #getting the pygame clock for handling fps
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #filling the screen with background color
        screen.fill(WHITE)
        for x_grid in range(np.shape(grid)[1]):
            for y_grid in range(np.shape(grid)[0]):
                if (grid[y_grid,x_grid]==DIRT):
                    pygame.draw.rect(screen, BROWN, pygame.rect.Rect(coor_to_pixel(x_grid)-np.floor(CELL_SIZE/2), coor_to_pixel(y_grid)-np.floor(CELL_SIZE/2), CELL_SIZE, CELL_SIZE))
        vpf = VisualizePathFind(source, dest, grid)
        vpf.uniform_cost_search()
        #vpf.a_star_search()                 
        time.sleep(20)
        #finally delaying the loop to with clock tick for 10fps 
        clock.tick(5)