# -*- coding: utf-8 -*-
"""
Created on Fri May  1 20:38:07 2020

@author: jonyl
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 20:42:04 2020

@author: jonyl
"""
import numpy as np
from graphelem import PathNode 

INVALID_NODE = -1

class PriorityQueueList():
    def __init__(self):
        self.list = []
        self.size = 0
    
    def insert(self, path_cost, node):
        self.list.append(PathNode(path_cost, node))
        self.list.sort(reverse = True)
        self.size += 1
    
    # return node of desired name with binary search, returns -1 if not found. Assumes that the node_name being searched is present
    def find_node(self, node):
        index = 0
        for index in range(0,len(self.list)):
            if (self.list[index].return_node_name() == node.return_node_name()):
                return self.list[index]
    
    #replace the old node in the list, with a new node of the same type but a different
    def replace_node(self, new_node):
        for index in range(self.size):
            if (self.list[index].return_node_name() == new_node.return_node_name()):
                del self.list[index] #remove the old element
                self.insert(new_node.return_path_cost(), new_node.return_node_name()) #add in the new element
                return
        print("ERROR: node not here")
        return
    
    def is_present(self, node):
        index = 0
        for index in range(0,len(self.list)):
            if (self.list[index].return_node_name() == node.return_node_name()):
                return True
        return False
    
    #def replace_node_(self, node)
        
    def pop(self):
        if (self.size>0):
            self.size = self.size -1
            return self.list.pop()
        print("no elements left")
        return -1
        
    def print_pq(self):
        for index in range(self.size):
            print(self.list[index])
        
#if __name__ == "__main__":
#    x = PriorityQueueList()
#    x.insert(1, 5)
#    x.insert(1.5,5)
#    x.insert(5,3)
#    x.insert(3.4, 4)
#    x.insert(6,5)
#    x.insert(5.4,5)
#    x.print_pq() 
#    print(x.find_node(3))
    