from maze import Maze
from generator import RandomizedDFS

if __name__ == "__main__":
    m = Maze(10, 10, generator=RandomizedDFS)
    print(m)
    print(m.is_all_visited())