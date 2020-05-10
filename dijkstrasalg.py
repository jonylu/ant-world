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
    
    def uniform_cost_search(self, debugmode = False):
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
            if debugmode:
                print(counter)
                print("frontier")
                frontier.print_pq()
                print("visited")
                visited.print_pq()
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
            #print("frontier")
            #frontier.print_pq()
        #after while loop either you have a current_index
        backtrack_node = end_index
        path_array= []
        while(backtrack_node != -1):
            path_array.append(backtrack_node)
            backtrack_node = previous[backtrack_node]
        #path_array = path_array[::-1] reverses the array
        return [self.index_to_coor(index) for index in path_array] 
    
    def a_star_search(self, debugmode = False):
        start_index = self.coor_to_index(self.start)
        current_index = start_index
        edge_mat = self.edge_matrix()
        
        end_index = self.coor_to_index(self.end)
        previous = self.initialize_prev_vector_with_neg_ones() #traces the previous path
        visited = pq.PriorityQueueList() #there is no reason to use priority queue here, mainly for convenenience
        frontier= pq.PriorityQueueList() #vector of inifinty
        #heuristic = self.manhatten_heuristic(end_index)
        heuristic = self.euclidean_heuristic(end_index)
        path_cost_array = np.zeros(self.x_size()*self.y_size())
        path_cost_array = path_cost_array + math.inf #create path_cost matrix as map of infinity
        path_cost_array[current_index] = 0
        frontier.insert(path_cost_array[current_index] + heuristic[current_index], current_index)
        counter = 0 
        while True:        
            if debugmode:
                print(counter)
                print("frontier")
                frontier.print_pq()
                print("visited")
                visited.print_pq()
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
        #after while loop either you have a current_index
        backtrack_node = end_index
        path_array= []
        while(backtrack_node != -1):
            path_array.append(backtrack_node)
            backtrack_node = previous[backtrack_node]
        return [self.index_to_coor(index) for index in path_array] 


    #create child nodes assuming that 
    def create_child_nodes(self, current_node, edge_mat): 
        curr_path_cost = current_node.return_node_priority()
        node_name = current_node.return_node_name()
        node_coor = self.index_to_coor(node_name)
        child_nodes = []
        for state_shift in [(-1, 0), (1, 0), (0,1), (0,-1)]:
            next_coor = node_coor + state_shift
            if (all(next_coor>=0) and all(next_coor < (self.x_size(), self.y_size()))): #inbounds then add
                child_nodes.append(PathNode(curr_path_cost + edge_mat[node_name][self.coor_to_index(next_coor)],self.coor_to_index(next_coor)))
        return child_nodes
    
    def create_child_nodes_with_heuristic(self, current_node, edge_mat, end_index, heuristic, path_cost_array): 
        updated_path_cost_array = path_cost_array
        node_name = current_node.return_node_name()
        node_coor = self.index_to_coor(node_name)
        child_nodes = []
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
    #return heuristic as a 1D array of size x_size()*y_size()
    
    def manhatten_heuristic(self, end_index):
        heuristic_len = self.x_size()*self.y_size()
        heuristic = np.zeros(heuristic_len)
        end_coor = self.index_to_coor(end_index)
        for index in range(heuristic_len):
            coor = self.index_to_coor(index)
            heuristic[index] = distance_metrics.manhatten_distance(coor, end_coor)
        return heuristic
    
    def euclidean_heuristic(self, end_index):
        heuristic_len = self.x_size()*self.y_size()
        heuristic = np.zeros(heuristic_len)
        end_coor = self.index_to_coor(end_index)
        for index in range(heuristic_len):
            coor = self.index_to_coor(index)
            heuristic[index] = 2*distance_metrics.euclidean_distance(coor, end_coor)
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
    grid = np.zeros([4,4])
    source = np.array([2,2])
    dest = np.array([0,0])
    p = PathFind(source, dest, grid)
    path = p.a_star_search()  
    print(path)
    
def baby_uniform_test():
    print("running baby uniform")
    grid = np.zeros([4,4])
    source = np.array([2,2])
    dest = np.array([0,0])
    p = PathFind(source, dest, grid)
    path = p.uniform_cost_search()  
    print(path)
    
def time_comparison():
    starttime = time.time()
    simple_dijkstras_test()
    print(time.time()-starttime)
    
    starttime = time.time()
    simple_uniform_cost_search_test()
    print(time.time()-starttime) 
 
    starttime = time.time()
    simple_a_star_cost_search_test()
    print(time.time()-starttime)

    starttime = time.time()
    larger_dijkstras_test()
    print(time.time()-starttime)

    starttime = time.time()
    larger_uniform_cost_search_test()
    print(time.time()-starttime)   
    
    starttime = time.time()
    larger_a_star_test()
    print(time.time()-starttime)

def comparison_a_star_uniform():
    baby_uniform_test()
    baby_a_star_test()

if __name__=="__main__": 
    #larger_dijkstras_test()
    #larger_uniform_cost_search_test()
    #baby_a_star_test()
    time_comparison()
    #comparison_a_star_uniform()
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

    
    