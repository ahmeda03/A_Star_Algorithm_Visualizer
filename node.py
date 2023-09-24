import random
"""
Project: A* Algorithm Visualization
File Name: node.py
Author: Ahmed Aamir
"""
class Node(object):
    def __init__(self, percentOfBarriers = 0.45):
        self.f = 0 # f(n) value
        self.g = 0 # g(n) value
        self.h = 0 # h(n) value
        self.row, self.column = 0, 0 # row and column for the given node
        self.neighbors = [] # list of neighbors for the node
        self.isBarrier = False # tells whether the node is a barrier or not
        self.x, self.y = 0, 0 # the pixel values of the location of the node
                              # on the screen, used to calculate the heuristic
        self.previous = None # used to tell what the parent node is of the current
                             # node, used when backtracking to find the shortest path

        # used to randomly make traversable nodes into 
        # barriers/walls, this can be changed if you pass
        # a different percentage into the Node instantiation 
        # when we create each node in the grid class's createGrid function  
        if random.random() < percentOfBarriers:
            self.isBarrier = True
    
    # Used to add the neighbors in all eight directions for each node
    def addNeighbors(self, row, column, grid):
        if row < len(grid) - 1:
            self.neighbors.append(grid[row + 1][column])

        if row > 0:
            self.neighbors.append(grid[row - 1][column])

        if column < len(grid[0]) - 1:
            self.neighbors.append(grid[row][column + 1])

        if column > 0:
            self.neighbors.append(grid[row][column - 1])

        if row < len(grid) - 1 and column < len(grid[0]) - 1:
            self.neighbors.append(grid[row + 1][column + 1])

        if row > 0 and column < len(grid[0]) - 1:
            self.neighbors.append(grid[row - 1][column + 1])

        if row < len(grid) - 1 and column > 0:
            self.neighbors.append(grid[row + 1][column - 1])
        
        if row < 0 and column > 0:
            self.neighbors.append(grid[row - 1][column - 1])

        # [
        # [1,2,3]
        # [4,5,6]
        # [7,8,9]
        #     ]