from agents.IAgent import IAgent
from maze.Maze import Maze, Cell

import numpy as np

from collections import deque


class DFSAgent(IAgent):
    def __init__(self):
        """
        Initialize the Depth-First-Search Agent.
        """
        self.history = deque([])
        self.visited = set()

    def get_move(self, maze:Maze, cell:Cell):
        """
        Get the next move of the agent.

        Args:
            maze; (Maze): The maze instance that the agent is in.

        Returns:
            str: The next move of the agent. One of ['N', 'S', 'E', 'W'].
        """
        self.visited.add(cell)
        possible_neighbors = [(direction, possible_neighbor) for direction in cell.get_possible_neighbors() \
                              if (possible_neighbor := maze.get_next_cell(cell, direction)) not in self.visited]

        if len(possible_neighbors) > 0:
            next_direction = possible_neighbors[np.random.randint(0, len(possible_neighbors))][0]
            self.history.append(next_direction)
        else:
            next_direction = maze.get_opposite_direction(self.history.pop())

        return next_direction
        