import pygame
from node import Node
import keyboard
"""
Project: A* Algorithm Visualization
File Name: grid.py
Author: Ahmed Aamir
Instructions: 'spacebar' - used to start the algorithm
              'c' - clears and generates and new grid, note that this only
                    works if the algorithm has finished executing or if
                    the while loop was stopped with the 's' key
              's' - stops the algorithm from proceeding, can be used at any time,
                    however it is usually used to stop the algorithm prematurely
                    if we see that there isn't any way to reach the goal node, meaning
                    the goal node is surrounded by walls, we can thereafter press the 'c' 
                    key to regenerate a new grid for the algorithm to 

Potential Errors: If the program doesn't run, it may be due to the pygame and keyboard
                  libraries not being installed, if so please try the commands below:

                  pip install pygame - used for the visualization
                  pip install keyboard - used to detect if the 's' key is pressed
                                         to break the while loop

Meaning of each color:
                        Red - Nodes in the closed set
                        Green - Nodes in the open set
                        Black - Barriers/Walls, so non-traversable nodes
                        White - Traversable nodes
                        Yellow - Start node
                        Turquoise - Goal node
                        Blue - Shortest path from start node to goal node
"""

# Create a 2D array
def createGrid():
    grid = []
    for row in range(45):
        # Add an empty array that will hold each row
        grid.append([])
        for column in range(90):
            # Append a node to the current row
            grid[row].append(Node())

    # Used to add the neighbors into a variable for each node
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            grid[row][column].row, grid[row][column].column = row, column
            grid[row][column].addNeighbors(row, column, grid)

    # These statement ensure that the start
    # and goal nodes aren't made into walls,
    # since if they were the algorithm wouldn't
    # finish, even if there was a path available
    grid[0][0].isBarrier = False
    grid[len(grid) - 1][len(grid[0]) - 1].isBarrier = False

    # Return the grid so, it may be drawn onto the screen
    return grid 

# Draw the grid in its entirety
def drawGrid(openSet, closedSet, path, grid):
        # Define the indices for the start and goal nodes
        startIndices = (0, 0)
        goalIndices = (len(grid) - 1, len(grid[0]) - 1)

        # Draw the entire grid with the 
        # appropriate colors for each node
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                # By default each traversable node is white
                color = WHITE
                node = grid[row][column]
                # If the node is the start node it is
                # displayed in a yellow color
                if (row, column) == startIndices:
                    color = YELLOW
                
                # If the node is the goal node it is
                # displayed in a turquoise color
                if (row, column) == goalIndices:
                    color = TURQUOISE
                
                # If the node's variable isBarrier is true it is
                # displayed in a black color, also we make sure
                # we don't color the start or end nodes black
                if node.isBarrier == True and (row, column) != startIndices and (row, column) != goalIndices:
                    color = BLACK
                
                # If the node is in the open set it is
                # displayed in a green color
                if node in openSet:
                    color = GREEN

                # If the node is in the closed set it is
                # displayed in a red color
                if node in closedSet:
                    color = RED
                
                # Finally, if the path has been constructed
                # it is displayed in a blue color
                if node in path:
                    color = BLUE
                
                # Draw the current node to the screen with the given
                # color and position on the window
                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])
                
                # Calculate and save the pixel position of the middle of the current node so,
                # it may be used when calculating the heuristic (Euclidean distance)
                node.x = ((((MARGIN + WIDTH) * column) + 12.5) + MARGIN)
                node.y = ((((MARGIN + HEIGHT) * row) + 12.5) + MARGIN)

# Used to help draw the grid after each step in the algorithm
def constructGrid(openSet, closedSet, path, grid):
    # The window must be filled each time we draw to
    # the screen in order to show a live animation 
    # of the visualization
    screen.fill(BLACK)
    drawGrid(openSet, closedSet, path, grid)

# Implementation of the A* algorithm
def aStar(grid):
        finishedTuple = (False, False)
        constructGrid(openSet, closedSet, path, grid)

        # Check if there are any nodes in the open set
        if len(openSet) > 0:
            # Find the node with the lowest F value in the 
            # open set
            lowestNode = 0
            for value in range(len(openSet)):
                if openSet[value].f < openSet[lowestNode].f:
                    lowestNode = value
            
            current = openSet[lowestNode]

            # Check if reached the goal node
            if current == goalNode:
                print("ALGORITHM COMPLETE")

                # Create the path from the goal
                # node to the start node by backtracking
                # using the 'previous' variable in each node,
                # which gives up the parent node for the node
                # we are currently looking at 
                temp = current
                path.append(temp)
                while temp.previous:
                    path.append(temp.previous)
                    temp = temp.previous

                # Draw the grid with the shortest path shown
                # and set the two variables to true to break
                # out of the while loop that executes the aStar function,
                # stopping the algorithm from continuing any further
                drawGrid(openSet, closedSet, path, grid)
                finished = True
                noSolution = True
                finishedTuple = (finished, noSolution)
                return finishedTuple
            
            # Remove the the node with the lowest F value
            # from the open set, as it will be evaluated
            lowestFNode = openSet.pop(lowestNode)
            
            # Add the node to the closed set, as it is
            # being evaluated
            closedSet.append(lowestFNode)

            # Go through each neighbor for the node
            # currently being evaluated
            for neighbor in lowestFNode.neighbors:
                # Check if neighbor has not already 
                # been evaluted, meaning is not already 
                # in the closed set or if the neighbor 
                # is a wall so, we can't traverse to it
                if neighbor not in closedSet and neighbor.isBarrier == False:
                    # Add the distance to the neighbor from the current node,
                    # it is one for all directions, so the weight of each edge is 1,
                    # also the value is stored in a temporary variable because
                    # might have already evaluted the neighbor from a different node 
                    # and put it into the open set so, it may have a
                    # lower G cost, meaning we must check which path gives it a lower 
                    # G cost 
                    tempG = lowestFNode.g + 1

                    # Check if the neighbor is in the open set, if so
                    # compare the two G values, if not set the temporary G
                    # value to the G value for the neighbor and place the
                    # neighbor in the open set
                    newPath = False
                    if neighbor in openSet:
                        if tempG < neighbor.g:
                            neighbor.g = tempG
                            newPath = True
                    else:
                        neighbor.g = tempG
                        newPath = True
                        openSet.append(neighbor)

                    # Calculate the H and F values for the neighbor and
                    # assign the current node as the parent node for the
                    # neighbor using the 'previous' variable, which 
                    # will be used when reconstructing the path
                    if newPath:
                        neighbor.h = calculateHeuristic(neighbor, goalNode)
                        neighbor.f = neighbor.g + neighbor.h
                        neighbor.previous = current
        
        # Once we run out of nodes in the open set we end the program by 
        # breaking the while loop with our returned tuple
        else:
            finishedTuple = (False, True)
            return finishedTuple
        
        # Used to update the visualization window 
        # as the algoritm proceeds
        pygame.display.update()

        # Return false values within the tuple
        # to continue the while loop and in-turn the algorithm
        return finishedTuple

def calculateHeuristic(neighbor, end):
    # Calculate and return the Euclidean distance
    distance = pygame.math.Vector2(neighbor.x, neighbor.y).distance_to((end.x, end.y))
    return distance

# Initialize the lists for the
# openSet, closedSet, and path
openSet = []
closedSet = []
path = []

# Define some colors that will be used
# when drawing the grid
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TURQUOISE = (0, 255, 255)
 
# Define the width and height of each
# square on the grid along with the margin
# between each square
WIDTH = 15
HEIGHT = 15
MARGIN = 2

# Initialize pygame
pygame.init()

# Set the height and width of the screen
WINDOW_SIZE = [1532, 767]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of the screen
pygame.display.set_caption("A* Algorithm")

# Variable used to loop until the user
# clicks the close button
running = True

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Create the grid (2D array) that is used 
# to hold all of the nodes
grid = createGrid()

# Make sure that the start and goal nodes
# aren't walls, cause if they were then
# we wouldn't be able to reach the goal even
# if there was a path available
grid[0][0].isBarrier = False
grid[len(grid) - 1][len(grid[0]) - 1].isBarrier = False

# Place the starting node in the openSet and define
# the goal node
openSet.append(grid[0][0])
# goalNode = grid[len(grid) - 1][len(grid[0]) - 1]

# Set both conditions to false initally (finished, noSolution)
finishedConditions = (False, False)

# Main Program Loop 
while running:
    # Save the value of goal node for each grid created
    # since a new node is assigned as the goal node  
    # each time we reset the grid
    goalNode = grid[len(grid) - 1][len(grid[0]) - 1]

    # Continuously check for any input given by the user
    for event in pygame.event.get():  # User did something
        # Checks if the window was closed, if it ends the while loop
        if event.type == pygame.QUIT:
            running = False

        # Checks if keyboard input was received / if a key was pressed
        if event.type == pygame.KEYDOWN:
            # If the space was pressed, start the algorithm 
            if event.key == pygame.K_SPACE:
                while finishedConditions[0] == False and finishedConditions[1] == False:
                    finishedConditions = aStar(grid)
                    # If the letter 's' was pressed, we stop the loop 
                    # (this conditional check is present in order to 
                    # prematurely stop the loop if we can visibly 
                    # see that there is no path to the goal node, as 
                    # if we don't stop the while loop, we cannot reset
                    # or close the grid without the program crashing)
                    if keyboard.is_pressed("s"):
                        break
            
            # If the letter 'c' was pressed, we clear and create a new  grid 
            # so that we may run the algorithm once again without 
            # closing the program
            if event.key == pygame.K_c:
                grid = createGrid()
                openSet = []
                closedSet = []
                path = []

                # Add the value of the new node
                # which represents the starting node 
                # to the openSet
                openSet.append(grid[0][0])
                finishedConditions = (False, False)

    # Used to draw the grid with the appropriate
    # colors for each node as the algorithm proceeds
    drawGrid(openSet, closedSet, path, grid)

    # Used to limit the program to 60 frames per second
    clock.tick(60)
 
    # Used to update the screen with what we have drawn
    # onto the window so it may be properly displayed
    pygame.display.flip()

# Used to properly quit the program
pygame.quit()