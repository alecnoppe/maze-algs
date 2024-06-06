from abc import ABC, abstractmethod

class IGenerator(ABC):
    @staticmethod
    @abstractmethod
    def generate(self, maze) -> None:
        """
        Generate method that updates the cells of a maze in-place (via updating Cell.visited and Cell.walls attributes).

        Args:
            maze; (Maze object): The maze instance to update.
        """
        pass