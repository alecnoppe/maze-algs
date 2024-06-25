from generators.IGenerator import IGenerator
from maze.Maze import Maze, Cell

from collections import deque
import numpy as np
from copy import copy


class FractalTessellation(IGenerator):
    def __init__(self, n_tiles):
        """
        Initialize the FractalTessellation generator.

        Args:
            n_tiles: int; The number of tiling steps to perform.
        """
        self.n_tiles = n_tiles

    def tile_wall_dict(self, wall_dict, current_size):
        """
        Tile the wall dictionary by copying the current wall dictionary to the next 3 quadrants.

        Args:
            wall_dict: list[list[dict]]; The wall dictionaries
            current_size: int; The current size of the wall dictionary
        """
        for i in range(current_size):
            for j in range(current_size):
                # Copy over the current wall dictionary to the next 3 quadrants
                current_wall_dict = wall_dict[i][j]
                wall_dict[current_size+i][j] = copy(current_wall_dict)
                wall_dict[i][current_size+j] = copy(current_wall_dict)
                wall_dict[current_size+i][current_size+j] = copy(current_wall_dict)

    def wall_dict_to_np(self, wall_dict, current_size):
        """
        Convert the wall dictionary to a numpy array of Cell objects.

        Args:
            wall_dict: list[list[dict]]; The wall dictionaries
            current_size: int; The current size of the wall dictionary
        
        Returns:
            cells: np.array; The numpy array of Cell objects
        """
        cells = np.empty((current_size, current_size), dtype=object)
        for i in range(current_size):
            for j in range(current_size):
                cell = Cell(i,j)
                cell.walls = wall_dict[i][j]
                cells[i,j] = cell
                cells[i,j].visited = True

        return cells
        
    def generate(self, maze: Maze) -> None:
        """
        Generate a maze with the Fractal Tessellation algorithm.

        Works as follows:
        1. Start with a 1x1 grid of cells X
        2. Copy over the current X to the next 3 quadrants
        3. Break 3 walls between the tiled sections
        4. Repeat steps 2 and 3 for n_tiles iterations

        Args:
            maze; (Maze): The maze instance to update.
        """
        # Initialize the wall dictionary
        wall_dict = [[{"N": True, "S": True, "E": True, "W": True} for _ in range(2**self.n_tiles)] for _ in range(2**self.n_tiles)]
        current_size = 1
        # Define the side indices to offset and direction
        side_idx_to_offset_and_direction = {
            0: ([0,1], "E", "W"),
            1: ([0,1], "E", "W"),
            2: ([1,0], "S", "N"),
            3: ([1,0], "S", "N"),
        }
        # Perform n_tiles iterations of tiling
        for _ in range(self.n_tiles):
            # Randomly select the walls to break
            random_idx = np.random.choice(np.arange(current_size), size=4)
            side_offsets = np.array([
                [random_idx[0], current_size-1],
                [current_size + random_idx[1], current_size-1],
                [current_size-1, random_idx[2]],
                [current_size-1, current_size + random_idx[3]]
            ])
            sides = np.random.choice(np.arange(0,4), size=3, replace=False)
            # Tile the wall dictionary
            self.tile_wall_dict(wall_dict, current_size)
            current_size *= 2

            # Remove 3 walls between the tiled sections
            for side_idx in sides:
                base_offset = side_offsets[side_idx]
                next_offset, first_wall, second_wall = side_idx_to_offset_and_direction[side_idx]
                i, j = base_offset
                wall_dict[i][j][first_wall] = False
                
                i, j = i +next_offset[0], j+next_offset[1]
                wall_dict[i][j][second_wall] = False      

        # Convert the wall dictionary to a numpy array of Cell objects
        # And set the start and target indices
        cells = self.wall_dict_to_np(wall_dict, current_size)
        cells[maze.start_indices].is_start = True
        cells[maze.target_indices].is_target = True
        maze.cells = cells
