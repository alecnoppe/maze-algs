from maze import Maze
from generators import RandomizedDFS, Wilson
from gui import GUI
from agents import RandomAgent, DFSAgent
from solvers import ASolver
from utils import *

import numpy as np


if __name__ == "__main__":
    gui = GUI(16, 16)
    m = Maze(16, 16, generator=RandomizedDFS(bias=0.75))
    gui.simulate(m, DFSAgent())
    solver = ASolver()
    path = solver.solve(m)

    maze_array, holes = maze_to_npy(m, return_holes=True)
    path_array = path_to_npy(path, maze_array, holes)

    np.save('mazes/maze.npy', maze_array)
    np.save('mazes/path.npy', path_array)

    plot_maze_from_npy('mazes/maze.npy')
    plot_path_from_npy('mazes/path.npy')
    plot_maze_and_path('mazes/maze.npy', 'mazes/path.npy')

    dataset = create_dataset(10, 5, generator=Wilson())
    # save the dataset
    np.save('dataset.npy', dataset)
