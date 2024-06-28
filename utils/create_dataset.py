from maze import *
from generators import *
from solvers import ASolver

import numpy as np
from tqdm import trange
import threading

def path_to_npy(path: list[Cell], maze_array: np.ndarray, holes: list[tuple[int]] = []):
    """
    Convert a path to a numpy array of 1s and 0s.

    Where 1s represent the path and 0s represent the unvisited cells.
    
    Args:
        path (list[Cell]): The path to convert.
        maze_array (np.ndarray): The maze as a numpy array.
        holes (list[tuple[int]]): The holes in the outer walls of the maze.

    Returns:
        np.ndarray: The path as a numpy array.
    """
    rows = maze_array.shape[0]
    cols = maze_array.shape[1]
    path_array = np.zeros((rows, cols), dtype=int)

    # find holes in the outer walls of the maze
    if holes:
        path_array[holes[0][0], holes[0][1]] = 1
        path_array[holes[1][0], holes[1][1]] = 1
    else:
        for i in range(rows):
            if maze_array[i, 0] == 0:
                path_array[i, 0] = 1
            if maze_array[i, cols-1] == 0:
                path_array[i, cols-1] = 1
        for j in range(cols):
            if maze_array[0, j] == 0:
                path_array[0, j] = 1
            if maze_array[rows-1, j] == 0:
                path_array[rows-1, j] = 1

    current_cell = path[0]

    for cell in path[1:]:
        # draw a line from the current cell to the next cell
        if current_cell.row == cell.row:
            # move horizontally
            row = 2*current_cell.row+1
            start_col = 2 * min(current_cell.col, cell.col) + 1
            end_col = 2 * max(current_cell.col, cell.col) + 2
            path_array[row, start_col:end_col] = 1
        else:
            # move vertically
            col = 2*current_cell.col+1
            start_row = 2 * min(current_cell.row, cell.row) + 1
            end_row = 2 * max(current_cell.row, cell.row) + 2
            path_array[start_row:end_row, col] = 1

        current_cell = cell
    
    return path_array

def maze_to_npy(maze: Maze, return_holes: bool = False):
    """
    Convert a maze object to a numpy array.

    Args:
        maze (Maze): The maze object to convert.
        return_holes (bool): Whether to return the holes in the outer walls of the maze.
    
    Returns:
        np.ndarray: The maze object as a numpy array.
        optional: list[tuple[int]]: The holes in the outer walls of the maze.
    """
    # Add walls around each cell in the maze
    rows = (maze.rows * 2) + 1
    cols = (maze.cols * 2) + 1
    maze_array = np.ones((rows, cols), dtype=int)
    # All indices i,j that are both not divisible by 2 are empty cells
    maze_array[1::2, 1::2] = 0

    # Break a wall around the start cell
    start_row, start_col = maze.start_indices
    if start_row == 0:
        start_hole = (0, 2*start_col+1)
        maze_array[0, 2*start_col+1] = 0
    elif start_row == maze.rows - 1:
        start_hole = (2*maze.rows, 2*start_col+1)
        maze_array[2*maze.rows, 2*start_col+1] = 0
    elif start_col == 0:
        start_hole = (2*start_row+1, 0)
        maze_array[2*start_row+1, 0] = 0
    elif start_col == maze.cols - 1:
        start_hole = (2*start_row+1, 2*maze.cols)
        maze_array[2*start_row+1, 2*maze.cols] = 0

    # Break a wall around the target cell
    target_row, target_col = maze.target_indices
    if target_row == 0:
        target_hole = (0, 2*target_col+1)
        maze_array[0, 2*target_col+1] = 0
    elif target_row == maze.rows - 1:
        target_hole = (2*maze.rows, 2*target_col+1)
        maze_array[2*maze.rows, 2*target_col+1] = 0
    elif target_col == 0:
        target_hole = (2*target_row+1, 0)
        maze_array[2*target_row+1, 0] = 0
    elif target_col == maze.cols - 1:
        target_hole = (2*target_row+1, 2*maze.cols)
        maze_array[2*target_row+1, 2*maze.cols] = 0
    
    # iterate over cell indices and cells
    for i, row in enumerate(maze.cells):
        for j, cell in enumerate(row):
            # Add walls to the maze array
            if not cell.walls['N']:
                maze_array[2*i, 2*j+1] = 0
            if not cell.walls['S']:
                maze_array[2*i+2, 2*j+1] = 0
            if not cell.walls['E']:
                maze_array[2*i+1, 2*j+2] = 0
            if not cell.walls['W']:
                maze_array[2*i+1, 2*j] = 0
    
    if return_holes:
        return maze_array, [start_hole, target_hole]
    
    return maze_array

def create_dataset(n_samples, maze_size, generator=Wilson):
    """
    Create a dataset of mazes and their solutions.

    Args:
        n_samples (int): The number of samples to create.
        maze_size (int): The size of the maze.
        generator (type): The maze generator to use.
    """
    dataset = []
    solver = ASolver()
    for i in trange(n_samples):
        # pick start/target indices somewhere along the edges of the maze
        # Ensure that the start and target cells are not on the same edge
        if np.random.rand() < 0.5:
            start_indices = (np.random.randint(maze_size), 0)
            target_indices = (np.random.randint(maze_size), maze_size - 1)
        else:
            start_indices = (0, np.random.randint(maze_size))
            target_indices = (maze_size - 1, np.random.randint(maze_size))

        maze = Maze(maze_size, maze_size, start_indices=start_indices, target_indices=target_indices, generator=generator)
        maze_array, holes = maze_to_npy(maze, return_holes=True)

        path = solver.solve(maze)
        path_array = path_to_npy(path, maze_array, holes)

        # convert maze_array, path_array to uint8 arrays
        maze_array = maze_array.astype(np.uint8)
        path_array = path_array.astype(np.uint8)

        dataset.append((maze_array, path_array))

    return dataset