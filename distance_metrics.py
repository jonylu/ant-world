# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 10:16:42 2020

@author: jonyl
"""
import numpy as np
import math

DIRT = 1
AIR = 0

#given two coordinates which are each numpy arrays of xcoor and y coor
def manhatten_distance(coor1, coor2):
    return np.sum(np.absolute(coor1-coor2))

def euclidean_distance(coor1, coor2):
    return math.sqrt(np.sum(np.square(coor1 - coor2)))

if __name__=="__main__":
    x = np.array([1,2])
    y = np.array([5,5])
    print(x)
    print(manhatten_distance(x, y))
    grid = np.zeros([6,6])
    print(grid)
    grid[2:4,1:3]=DIRT
    grid[2,4]=DIRT
    print(grid)