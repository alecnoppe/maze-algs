from maze import Maze
from generators import RandomizedDFS, Wilson, Prim
from gui import GUI
from agents import RandomAgent, DFSAgent
from solvers import ASolver
from utils import *

import numpy as np


if __name__ == "__main__":
    gui = GUI(16, 16)
    m = Maze(16, 16, generator=Prim())
    gui.simulate(m, DFSAgent())
