from agents.IAgent import IAgent
from maze.Maze import Maze, Cell

import numpy as np


class RandomAgent(IAgent):
    def __init__(self):
        """
        Initialize the Random Agent.
        """
        pass

    def get_move(self, maze:Maze, cell:Cell):
        """
        Get the next move of the agent.

        Args:
            maze; (Maze): The maze instance that the agent is in.

        Returns:
            str: The next move of the agent. One of ['N', 'S', 'E', 'W'].
        """
        possible_neighbors = cell.get_possible_neighbors()
        next_direction = np.random.choice(possible_neighbors)
        return next_direction
        