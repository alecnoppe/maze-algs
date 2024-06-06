from generator.IGenerator import IGenerator
from maze.Maze import Maze, Cell
from collections import deque
import numpy as np

class ListDict(object):
    def __init__(self):
        """
        Initialize a ListDict object.
        """
        self._list = []
        self._dict = {}
    
    def append(self, item):
        """
        Append an item to the list and add it to the dictionary.

        Args:
            item; (object): The item to append.
        """
        if item not in self._dict:
            self._list.append(item)
            self._dict[item] = len(self._list) - 1
        
    def remove(self, item):
        """
        Remove an item from the list and dictionary.

        Args:
            item; (object): The item to remove.
        """
        position = self._dict.pop(item)
        last_item = self._list.pop()
        if position != len(self._list):
            self._list[position] = last_item
            self._dict[last_item] = position

    def get_random_item(self):
        return np.random.choice(self._list)

    def __len__(self):
        return len(self._list)
    
    def __contains__(self, item):
        return item in self._dict

class Wilson(IGenerator):
    @staticmethod
    def generate(maze:Maze) -> None:
        """
        Use Wilson's algorithm to generate a maze.

        Args:
            maze; (Maze): The maze instance to update.
        """
        rows = maze.rows
        cols = maze.cols
        
        # Initialize a 2D array to store the legal directions for each cell
        legal_directions = np.full((rows, cols), fill_value=15, dtype=int)
        idx_to_directions = {1: ['N'], 2: ['S'], 4: ['E'], 8: ['W'],
         3: ['N', 'S'], 5: ['N', 'E'], 9: ['N', 'W'],
         6: ['S', 'E'], 10: ['S', 'W'], 12: ['E', 'W'],
         7: ['N', 'S', 'E'], 11: ['N', 'S', 'W'],
         13: ['N', 'E', 'W'], 14: ['S', 'E', 'W'],
         15: ['N', 'S', 'E', 'W']
        }

        # Remove the directions that are out of bounds
        legal_directions[0,:] -= 1
        legal_directions[-1,:] -= 2
        legal_directions[:,0] -= 8
        legal_directions[:,-1] -= 4
        
        # Initialize a list to store the unvisited cells
        unvisited_cells = ListDict()
        for i, j in np.ndindex(rows, cols):
            unvisited_cells.append(maze.get_cell(i, j))
        
        # Choose a random cell to start the generation
        current_cell:Cell = unvisited_cells.get_random_item()
        current_cell.visit()
        unvisited_cells.remove(current_cell)

        # Initialize a list to store the visited cells
        visited_cells = set()
        visited_cells.add(current_cell)

        # Initialize path array
        path = np.zeros((rows, cols), dtype=object)

        while len(unvisited_cells) > 0:
            # Choose a random unvisited cell
            first_cell:Cell = unvisited_cells.get_random_item()
            current_cell:Cell = first_cell
            # While the current cell is not visited, do a random walk
            while True:
                # Get the current cell's row and column
                current_row, current_col = current_cell.row, current_cell.col
                # Get the legal directions for the current cell
                current_legal_directions = legal_directions[current_row, current_col]
                # Choose a random (legal) direction to move
                next_direction = np.random.choice(idx_to_directions[current_legal_directions])
                # Update the path array
                path[current_row, current_col] = next_direction
                # Move to the next cell
                current_cell = maze.get_next_cell(current_cell, next_direction)
                # If the next cell is visited, break the loop
                if current_cell in visited_cells:
                    break

            # Reconstruct the path from the first cell to the current cell, visiting each cell along the way
            current_cell = first_cell
            
            while True:
                # Add the current cell to the visited set
                visited_cells.add(current_cell)
                current_cell.visit()
                # Remove the current cell from the unvisited SetDict
                unvisited_cells.remove(current_cell)
                # Get the direction to the next cell
                direction = path[current_cell.row, current_cell.col]
                # Get the opposite direction
                opposite_direction = maze.get_opposite_direction(direction)
                # Get the next cell
                next_cell = maze.get_next_cell(current_cell, direction)
                # Remove the wall between the current cell and the next cell
                current_cell.remove_wall(direction)
                # Remove the wall between the next cell and the current cell
                next_cell.remove_wall(opposite_direction)
                # Move to the next cell
                current_cell = next_cell
                # If the next cell is visited, break the loop
                if current_cell in visited_cells:
                    break



    
    def get_random_unvisited_cell(self, unvisited: set):
        return np.random.choice(unvisited)