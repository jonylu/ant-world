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
#Correction: 3/28/2020 I eventually settled on just using a grid. No env involved. The grid will show what is land what is water etc.

def grid_type(coor, grid):
    return grid[y_coor(coor), x_coor(coor)]

def edge_distance_manhatten(coor1, coor2, grid):
    if (distance_metrics.manhatten_distance(coor1,coor2)==0):
        return 0
    elif (distance_metrics.manhatten_distance(coor1,coor2)==1):
        if(grid_type(coor1, grid)==AIR and grid_type(coor2, grid)==AIR):
            return 1
        if(grid_type(coor1, grid)==DIRT or grid_type(coor2, grid)==DIRT):
            return 12
    else:
        return math.inf
    
def nodes(grid):
    nodes = []
    for y_coor in range(np.shape(grid)[0]):
        for x_coor in range(np.shape(grid)[1]):
            nodes.append(np.array([y_coor, x_coor]))
    return nodes

#In this function you think about internet matrix shape. [y,x]
def index_to_coor(index, grid):
    return np.array([index % y_size(grid), index // y_size(grid)])
    
def coor_to_index(coor, grid):
    return y_size(grid)* x_coor(coor) + y_coor(coor)
def x_size(grid):
    return np.shape(grid)[1]
def y_size(grid):
    return np.shape(grid)[0]

def x_coor(coor):
    return coor[1]

def y_coor(coor):
    return coor[0]
    
def edge_matrix(grid):
    edge_mat = np.zeros([x_size(grid)*y_size(grid),x_size(grid)*y_size(grid)])
    for pt1_index in range(np.shape(edge_mat)[0]):
        for pt2_index in range(pt1_index, np.shape(edge_mat)[1]):
            edge_mat[pt1_index][pt2_index]=edge_distance_manhatten(index_to_coor(pt1_index, grid), index_to_coor(pt2_index, grid), grid)
            edge_mat[pt2_index][pt1_index]=edge_mat[pt1_index][pt2_index] #redundant when pt1_index == pt2_index
    return edge_mat

def initialize_distance_mat(start_coor, edge_mat):
    dist_mat = np.zeros(np.shape(edge_mat)[0])
    dist_mat[:] = math.inf
    dist_mat[coor_to_index(start_coor, grid)]  = 0
    return dist_mat


    
def dijkstra(grid, start_coor, end_coor):
    edge_mat = edge_matrix(grid)
    dist_mat = initialize_distance_mat(start_coor, edge_mat)
    visited = []
    previous = np.zeros(np.shape(dist_mat), dtype=int)
    previous[:]=-1
    #previous[coor_to_index(start_coor, grid)] = 0
    start_index = coor_to_index(start_coor, grid)
    current_index = start_index
    end_index = coor_to_index(end_coor, grid)
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
    path_array = path_array[::-1]
    return [index_to_coor(index, grid) for index in path_array] 

 
if __name__=="__main__": 
    grid = np.zeros([20,30])
    grid[10:20, 10:20]=DIRT
    grid[40:45,10:20] = DIRT
    grid[0,2] = DIRT
    coor_nodes = nodes(grid)
    
    source =np.array([0,0])
    dest = np.array([18,25])
    path = dijkstra(grid, source, dest)
    new_grid = grid
    for coor in path:
        new_grid[coor[0]][coor[1]]=6
    print(new_grid)
    
    grid = np.zeros([5,5])
    grid[0:4,2:3]=DIRT
    start=[0,0]
    last = [0,4]
    path = dijkstra(grid, start, last)
    print(grid)
    print(path)