from abc import abstractmethod, ABC
from maze.Maze import Maze, Cell

class IAgent(ABC):
    """Agent interface that defines the methods that an agent must implement."""
    def __init__(self, **kwargs):
        """
        Initialize the agent with the given keyword arguments.
        
        Args:
            kwargs; (dict): Keyword arguments to initialize the agent.
        """
        pass
    
    @abstractmethod
    def get_move(self, maze:Maze, cell:Cell) -> str:
        """
        Get the next move of the agent.
        
        Args:
            maze; (Maze): The maze instance that the agent is in.
            cell; (Cell): The current cell that the agent is in.
        
        Returns:
            str: The next move of the agent. One of ['N', 'S', 'E', 'W'].
        """
        pass