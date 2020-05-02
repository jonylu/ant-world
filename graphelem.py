# -*- coding: utf-8 -*-
"""
Created on Fri May  1 20:24:11 2020

@author: jonyl
"""

import numpy as np

class PathNode():
    def __init__(self, path_cost, node_name):
        self.node = (path_cost, node_name)
    
    def return_path_cost(self):
        return self.node[0]
    
    def return_node_name(self, display_x_y_coor = False, y_size=7):
        if (not display_x_y_coor):
            return self.node[1]
        else:
            return np.array([self.node[1] // y_size, self.node[1] % y_size])  
    
        # overload < (less than) operator
    def __lt__(self, other_node):
        return self.return_path_cost() < other_node.return_path_cost()

    # overload > (greater than) operator
    def __gt__(self, other_node):
        return self.return_path_cost() > other_node.return_path_cost()

    # overload <= (less than or equal to) operator
    def __le__(self, other_node):
        return self.return_path_cost() <= other_node.return_path_cost()

    # overload >= (greater than or equal to) operator
    def __ge__(self, other_node):
        return self.return_path_cost() >= other_node.return_path_cost()

    # overload == (equal to) operator
    def __eq__(self, other_node):
        return self.return_path_cost() == other_node.return_path_cost()
    
    def __str__(self):
        return ('(PCost:' + str(self.return_path_cost()) + ', NodeName:' + str(self.return_node_name(True, 7)) + ')')