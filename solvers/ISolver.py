from abc import ABC, abstractmethod

class ISolver(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def solve(self, maze):
        pass

    @abstractmethod
    def solve_step(self, maze, **kwargs):
        pass