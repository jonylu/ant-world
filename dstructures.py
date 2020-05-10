# -*- coding: utf-8 -*-
"""
Created on Tue May  5 18:56:46 2020

@author: jonyl
"""
import math

class MyHeap():
    def __init__(self, input_array = []):
        self.heap = input_array
        self.heap.insert(0, 0) #insert a placeholder in the front of array. doesn't matter what.
    
    def min_heapify(self, i, N):
        print(len(self.heap))
        left = 2*i
        right = 2*i + 1
        print("left" + str(left))
        print("right" + str(right))
        print(self.heap[left])
        if (left <= N and self.heap[left] < self.heap[i]):
                smallest = left
        else:
            smallest = i
        if (right <= N and self.heap[right] < self.heap[smallest]):
                smallest = right
        if (smallest != i):
            self.swap(i, smallest)
            self.min_heapify(smallest, N)
            
    def build_heap(self, N):
        print(N)
        for i in range(math.floor(N/2), 0, -1):
            print(i)
            self.min_heapify(i, N)
    
    #swap two elements in the heap given two indices a and b
    def swap(self, a, b):
        temp = self.heap[a]
        self.heap[a] = self.heap[b]
        self.heap[b] = temp

    def print_heap(self):
        print('[')
        for elem in self.heap:
            print(elem)
        print(']')
            
if __name__ == "__main__":
    arr = [6,2,3,1,5,7,4,10,11,9,15]
    
    print("length"+str(len(arr)))
    x = MyHeap(arr)
    print("lenth"+str(len(arr)))
    x.print_heap()
    x.build_heap(len(arr)-1) #to account for the null element you added into the heap during initializing
    x.print_heap()
    
        
            