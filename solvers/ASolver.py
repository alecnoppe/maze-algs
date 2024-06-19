from solvers.ISolver import ISolver

from maze import *

import heapq
import numpy as np


def manhattan_distance(current_indices, target_indices):
    """
    Calculate the Manhattan distance between two points.

    Args:
        current_indices (tuple): The current indices.
        target_indices (tuple): The target indices.

    Returns:
        int: The Manhattan distance between the two points.
    """
    return abs(current_indices[0] - target_indices[0]) + abs(current_indices[1] - target_indices[1])

class ASolver(ISolver):
    def __init__(self):
        """
        Initialize the A* Solver.
        """
        pass

    def reconstruct_path(self, came_from, current_cell):
        """
        Reconstruct the path from the start cell to the target cell.

        Args:
            came_from (dict): The dictionary containing the path from the start cell to the target cell.
            current_cell (Cell): The current cell.

        Returns:
            list: The list of directions from the start cell to the target cell.
        """
        path = [current_cell]
        while current_cell in came_from:
            current_cell = came_from[current_cell]
            path.append(current_cell)
        
        path = path[::-1]

        return path

    def solve(self, maze:Maze):
        """
        Solve the maze using the A* algorithm.

        Args:
            maze (Maze): The maze to solve.
        
        Returns:
            list: A list of directions to solve the maze.
            or 
            numpy array of ones and zeros: A numpy array of the maze with the path to the target cell (ones).
        """
        start_indices = maze.start_indices
        target_indices = maze.target_indices

        start_cell = maze.get_cell(*start_indices)
        target_cell = maze.get_cell(*target_indices)

        # Initialize the open and closed sets
        open_set = set()
        closed_set = set()
        # add start cell to open set
        open_set.add(start_cell)

        # Initialize the g and f scores
        g_scores = {cell: np.inf for row in maze.cells for cell in row}
        g_scores[start_cell] = 0
        f_scores = {cell: np.inf for row in maze.cells for cell in row}
        f_scores[start_cell] = manhattan_distance(start_indices, target_indices)

        # Initialize the came_from dictionary
        came_from = {}

        while open_set:
            current_cell: Cell = min(open_set, key=lambda x: f_scores[x])
            closed_set.add(current_cell)

            if current_cell == target_cell:
                return self.reconstruct_path(came_from, current_cell)
                

            for neighbor_cell in [maze.get_next_cell(current_cell, direction) for direction in current_cell.get_possible_neighbors()]:
                if neighbor_cell is None or neighbor_cell in closed_set:
                    continue

                tentative_g_score = g_scores[current_cell] + 1
                if neighbor_cell not in open_set:
                    open_set.add(neighbor_cell)
                elif tentative_g_score >= g_scores[neighbor_cell]:
                    continue

                came_from[neighbor_cell] = current_cell
                g_scores[neighbor_cell] = tentative_g_score
                f_scores[neighbor_cell] = g_scores[neighbor_cell] + manhattan_distance((neighbor_cell.row, neighbor_cell.col), target_indices)

            open_set.remove(current_cell)

    def solve_step(self, maze, **kwargs):
        pass