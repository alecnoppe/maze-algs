import numpy as np

class Cell:
    def __init__(self, row:int, col:int, is_start:bool=False, is_target:bool=False) -> None:
        """
        Initialize a cell with its row and column indices.
        Set all walls to True and visited to False.

        Args:
            row; (int): The row index of the cell.
            col; (int): The column index of the cell.
            is_start; (bool): True if the cell is the start cell, False otherwise.
            is_target; (bool): True if the cell is the target cell, False otherwise.
        """
        self.row        :int  = row
        self.col        :int  = col
        self.walls      :dict = {'N': True, 'S': True, 'E': True, 'W': True}
        self.visited    :bool = False
        self.is_start   :bool = is_start
        self.is_target  :bool = is_target

    def visit(self) -> None:
        """
        Set the cell as visited.
        """
        self.visited = True

    def remove_wall(self, direction) -> None:
        """
        Remove the wall in the given direction.
        Direction can be 'N', 'S', 'E', or 'W'.

        Args:
            direction; (str): The direction of the wall to remove.
        """
        self.walls[direction] = False

    def get_possible_neighbors(self) -> list:
        """
        Get the possible neighbors of the cell.
        A neighbor is a cell that is adjacent to the current cell and not separated by a wall.

        Returns:
            list: A list of possible neighbors of the cell.
        """
        return [key for key, value in self.walls.items() if not value]
    
    def get_wall_directions(self) -> list:
        """
        Get the directions of the walls of the cell.

        Returns:
            list: A list of the directions of the walls of the cell.
        """
        return [key for key, value in self.walls.items() if value]

    def __repr__(self) -> str:
        """
        Convert the cell to a numpy 2d (5x5) array of strings.
        """
        # Create a representation of 5x5 characters
        # '#' for wall direction, ' ' for no wall direction
        out = np.zeros((5, 5), dtype=str)
        out[:] = ' '
        out[0, :] = '#'
        out[-1, :] = '#'
        out[:, 0] = '#'
        out[:, -1] = '#'

        if not self.walls['N']:
            out[0, 1:4] = ' '
        if not self.walls['S']:
            out[-1, 1:4] = ' '
        if not self.walls['E']:
            out[1:4, -1] = ' '
        if not self.walls['W']:
            out[1:4, 0] = ' '
        
        # If the cell is the start cell, mark it with 'S'
        if self.is_start:
            out[2, 2] = 'S'
        
        # If the cell is the target cell, mark it with 'X'
        if self.is_target:
            out[2, 2] = 'X'

        return out

class Maze:
    def __init__(self, rows:int, cols:int, generator:callable=None, start_indices:tuple=None, target_indices:tuple=None) -> None:
        """
        Initialize a maze with the given number of rows and columns.
        The maze is represented as a 2D grid of cells.
        If a generator function is provided, it will be called to generate the maze.

        Args:
            rows; (int): The number of rows in the maze.
            cols; (int): The number of columns in the maze.
            generator; (callable): The generator function to generate the maze.
            start_indices; (tuple): The row and column indices of the start cell. Defaults to (0, 0).
            target_indices; (tuple): The row and column indices of the target cell. Defaults to (rows - 1, cols - 1).
        """
        self.rows:int = rows
        self.cols:int = cols
        self.generator:callable = generator
        # Set the start and target indices
        if start_indices is None:
            start_indices = (0, 0)
        self.start_indices:tuple = start_indices
        if target_indices is None:
            target_indices = (rows - 1, cols - 1)
        self.target_indices:tuple = target_indices
        # Initialize the maze with empty cells (all walls and not visited)
        self.cells:np.ndarray = np.array([[Cell(i, j) for j in range(cols)] for i in range(rows)])
        # Set the start and target cells
        self.cells[start_indices].is_start = True
        self.cells[target_indices].is_target = True
        # If a generator function is provided, call it to generate the maze
        if self.generator:
            self.generator.generate(self)
    
    def is_all_visited(self) -> bool:
        """
        Check if all cells in the maze have been visited.

        Returns:
            bool: True if all cells have been visited, False otherwise.
        """
        return all([cell.visited for row in self.cells for cell in row])

    def convert_direction(self, direction:str) -> tuple:
        """
        Convert the direction to the row and column indices change.

        Args:
            direction; (str): The direction to convert.

        Returns:
            tuple: A tuple of the row and column indices change.
        """
        if direction == 'N':
            return -1, 0
        if direction == 'S':
            return 1, 0
        if direction == 'E':
            return 0, 1
        if direction == 'W':
            return 0, -1
        
    def convert_indices(self, row:int, col:int) -> tuple:
        """
        Convert the row and column indices to the direction.

        Args:
            row; (int): The row index.
            col; (int): The column index.

        Returns:
            tuple: A tuple of the direction.
        """
        if row == -1:
            return 'N'
        if row == 1:
            return 'S'
        if col == 1:
            return 'E'
        if col == -1:
            return 'W'
    
    def get_cell(self, row:int, col:int) -> Cell:
        """
        Get the cell at indices (row, col).

        Args:
            row; (int): The row of the cell to select.
            col; (int): The column of the cell to select.

        Returns:
            Cell: The cell at indices (row, col).
        """
        return self.cells[row, col]
        
    def get_next_cell(self, cell:Cell, direction:str) -> Cell:
        """
        Get the next cell in the given direction from the current cell.

        Args:
            cell; (Cell): The current cell.
            direction; (str): The direction to move to.

        Returns:
            Cell: The next cell in the given direction.
        """
        d_row, d_col = self.convert_direction(direction)
        return self.cells[cell.row + d_row, cell.col + d_col]
    
    def get_unvisited_neighbors_directions(self, cell:Cell) -> list[str]:
        """
        Get the directions from a given cell, to unvisible directions.

        Args:
            cell; (Cell): current cell

        Return:
            list of strings; either "N", "S", "E", "W"
        """
        cell_idx = cell.row, cell.col
        # Get the neighbors of the cell that have not been visited yet
        neighbors = []
        if cell_idx[0] > 0 and not self.cells[cell_idx[0] - 1, cell_idx[1]].visited:
            neighbors.append("N")
        if cell_idx[0] < self.rows - 1 and not self.cells[cell_idx[0] + 1, cell_idx[1]].visited:
            neighbors.append("S")
        if cell_idx[1] > 0 and not self.cells[cell_idx[0], cell_idx[1] - 1].visited:
            neighbors.append("W")
        if cell_idx[1] < self.cols - 1 and not self.cells[cell_idx[0], cell_idx[1] + 1].visited:
            neighbors.append("E")
        
        return neighbors
    
    def get_opposite_direction(self, direction:str) -> str:
        """
        Get the opposite direction of the given direction.

        Args:
            direction; (str): The direction to get the opposite of.

        Returns:
            str: The opposite direction of the given direction.
        """
        if direction == 'N':
            return 'S'
        if direction == 'S':
            return 'N'
        if direction == 'E':
            return 'W'
        if direction == 'W':
            return 'E'

    def __str__(self) -> str:
        """
        Convert the maze to a string representation.
        """
        # Create a representation of the maze
        # Each cell is represented by a 5x5 character grid
        # The grid contains walls ('#') and empty spaces (' ')
        out = np.zeros((self.rows * 5, self.cols * 5), dtype=str)
        out[:] = ' '
        out[::5, :] = '#'
        out[-1, :] = '#'
        out[:, ::5] = '#'
        out[:, -1] = '#'

        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.cells[i, j]
                out[i * 5: (i + 1) * 5, j * 5: (j + 1) * 5 ] = cell.__repr__()
        
        return '\n'.join([''.join(row) for row in out])