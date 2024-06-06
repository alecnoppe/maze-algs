from maze import Maze
from generator import RandomizedDFS, Wilson

if __name__ == "__main__":
    m = Maze(10, 10, generator=RandomizedDFS)
    print(m)
    print(m.is_all_visited())

    m = Maze(10, 10, generator=Wilson)
    print(m)
    print(m.is_all_visited())