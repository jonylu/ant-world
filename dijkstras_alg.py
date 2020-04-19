# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 20:57:01 2020

@author: jonyl
"""

import numpy as np
import distance_metrics
import math

DIRT=1
AIR=0

#Will I eventually need to split env and grid? env will have numbers to indicate what is at each grid.
#Correction: 3/28/2020 I eventually settled on just using a grid. No env involved. The grid will show what is land what is water etc. Also, know that the coordinates, from an ant's perspective, x is horizontal and y is vertical. The code will take care of the transposing inside.


class PathFind:
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
            #print (coor1)
            #print (coor2)
            if(self.grid_type(coor1)==AIR and self.grid_type(coor2)==AIR):
                return 1
            if(self.grid_type(coor1)==DIRT or self.grid_type(coor2)==DIRT):
                return 12
        else:
            return math.inf

    #In this function you think about internet matrix shape. [x, y]
    def index_to_coor(self, index):
        return np.array([index // self.y_size(), index % self.y_size()])
    
    def coor_to_index(self, coor):
        return self.y_size()* self.x_coor(coor) + self.y_coor(coor)
    
    def x_size(self):
        print(np.shape(self.grid))  #Only shows one coordinate for some reason
        return np.shape(self.grid)[0]
    
    def y_size(self):
        return np.shape(self.grid)[1]

    def x_coor(self, coor):
        return coor[0]

    def y_coor(self, coor):
        return coor[1]
    
    def edge_matrix(self):
        edge_mat = np.zeros([self.x_size()*self.y_size(),self.x_size()*self.y_size()])
        print(np.shape(edge_mat))
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
        previous = np.zeros(np.shape(dist_mat), dtype=int)
        previous[:]=-1
        #previous[coor_to_index(start_coor, grid)] = 0
        start_index = self.coor_to_index(self.start)
        current_index = start_index
        end_index = self.coor_to_index(self.end)
        visited.append(current_index)
        while(not(end_index in visited)):
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

 
if __name__=="__main__": 
#    grid = np.zeros([26,30])
#    grid[10:20, 10:20]=DIRT
#    grid[24:25,0:3] = DIRT
#    grid[0,2] = DIRT
#
#    source =np.array([0,0])
#    dest = np.array([18,25])
#    p = PathFind(source, dest, grid)
#    print(p.edge_matrix())
#    path = p.dijkstra()
#    print(path)
#    new_grid = grid
#    for coor in path:
#        new_grid[coor[0]][coor[1]]=6
#    print(new_grid)
#    
#    grid = np.zeros([5,5])
#    grid[0:4,2:3]=DIRT
#    start=[0,0]
#    last = [0,4]
#    p = PathFind(start,last,grid)
#    path = p.dijkstra()
#    print(grid)
#    print(path)

    source =np.array([0,0])
    dest = np.array([9,4])
    grid = np.zeros([5,10])
    p = PathFind(source, dest, grid)
    path = p.dijkstra()    
    print(path)