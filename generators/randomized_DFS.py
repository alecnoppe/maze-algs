from generators.IGenerator import IGenerator
from maze.Maze import Maze, Cell

from collections import deque
import numpy as np


class RandomizedDFS(IGenerator):
    def __init__(self, bias:float=0.5):
        """
        Remove walls in the given Maze, using the Randomized Depth-First-Search algorithm.

        Args:
            maze; (Maze): Maze instance, with unconnected, unvisited cells.
            bias; (float): Bias for the direction of the DFS. Closer to 0.0 for horizontal, to 1.0 for vertical.
        """
        self.bias = bias

    def generate(self, maze:Maze) -> None:
        """
        Remove walls in the given Maze, using the Randomized Depth-First-Search algorithm.

        Args:
            maze; (Maze): Maze instance, with unconnected, unvisited cells.
            bias; (float): Bias for the direction of the DFS. Closer to 0.0 for horizontal, to 1.0 for vertical.
        """
        # Start the generation from the starting square
        current_cell = maze.get_cell(*maze.start_indices)
        current_cell.visit()
        # Initialize a stack
        stack = deque([current_cell])
        # Algorithm outline:
        # While the stack is not empty
        # 1. Pop the last cell C added to the stack (LIFO)
        # 2. If C has any unvisited neighbors, add C back to the stack.
        # 3. Next, choose an unvisited neighbor N uniformly at random, and add N to the stack
        # 4. Finally, remove the wall in between the C and N

        horizontal_probs = self.bias
        vertical_probs = 1-self.bias

        probability_lookup = {
            "N": vertical_probs,
            "S": vertical_probs,
            "E": horizontal_probs,
            "W": horizontal_probs
        }
        
        while stack:
            # 1. Pop the last cell C added to the stack (LIFO)
            current_cell:Cell = stack.pop()
            # 2. If C has any unvisited neighbors, add C back to the stack.
            unvisited_neighbors_directions = maze.get_unvisited_neighbors_directions(current_cell)
            if len(unvisited_neighbors_directions) > 0:
                # Compute the probabilities for each direction
                probabilities = [probability_lookup[direction] for direction in unvisited_neighbors_directions]
                
                if sum(probabilities) == 0:
                    # If all the probabilities are 0, set them to 1
                    probabilities = [1 for _ in probabilities]
                    
                # normalize probabilities
                probabilities = [p/sum(probabilities) for p in probabilities]
                stack.append(current_cell)
                # 3. Next, choose an unvisited neighbor N uniformly at random, and add N to the stack
                next_direction:str = np.random.choice(unvisited_neighbors_directions, p=probabilities)
                next_cell:Cell = maze.get_next_cell(current_cell, next_direction)
                next_cell.visit()
                stack.append(next_cell)
                # Finally, remove the wall in between the C and N
                current_cell.remove_wall(next_direction)
                next_cell.remove_wall(maze.get_opposite_direction(next_direction))