from maze import Maze
from generators import RandomizedDFS, Wilson
from gui import GUI
from agents import RandomAgent


if __name__ == "__main__":
    gui = GUI(10, 10)
    m = Maze(10, 10, generator=RandomizedDFS)
    print(m)
    print(m.is_all_visited())
    gui.run(m)

    gui = GUI(10, 10)
    m = Maze(10, 10, generator=Wilson)
    print(m)
    print(m.is_all_visited())
    gui.run(m)

    gui = GUI(10, 10)
    m = Maze(10, 10, generator=Wilson)
    gui.simulate(m, RandomAgent())
    