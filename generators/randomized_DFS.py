from generators.IGenerator import IGenerator
from maze.Maze import Maze, Cell

from collections import deque
import numpy as np


class RandomizedDFS(IGenerator):
    @staticmethod
    def generate(maze:Maze) -> None:
        """
        Remove walls in the given Maze, using the Randomized Depth-First-Search algorithm.

        Args:
            maze; (Maze): Maze instance, with unconnected, unvisited cells.
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
        while stack:
            # 1. Pop the last cell C added to the stack (LIFO)
            current_cell:Cell = stack.pop()
            # 2. If C has any unvisited neighbors, add C back to the stack.
            unvisited_neighbors_directions = maze.get_unvisited_neighbors_directions(current_cell)
            if len(unvisited_neighbors_directions) > 0:
                stack.append(current_cell)
                # 3. Next, choose an unvisited neighbor N uniformly at random, and add N to the stack
                next_direction:str = np.random.choice(unvisited_neighbors_directions)
                next_cell:Cell = maze.get_next_cell(current_cell, next_direction)
                next_cell.visit()
                stack.append(next_cell)
                # Finally, remove the wall in between the C and N
                current_cell.remove_wall(next_direction)
                next_cell.remove_wall(maze.get_opposite_direction(next_direction))