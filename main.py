from maze import Maze
from generators import RandomizedDFS, Wilson
from gui import GUI
from agents import RandomAgent, DFSAgent


if __name__ == "__main__":
    gui = GUI(10, 10)
    m = Maze(10, 10, generator=Wilson)
    print(m)
    gui.simulate(m, DFSAgent())
    