import pygame
import numpy as np

from maze.Maze import Maze, Cell
from agents.IAgent import IAgent

class GUI:
    """
    Implement pygame GUI, for showing the maze (with visited/unvisited cells, walls, etc.) and the path found by the algorithm.
    """
    def __init__(self, rows, cols) -> None:
        """
        Initialize the GUI.
        """
        width = rows * 40
        height = cols * 40
        # Initialize the pygame window
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Maze')

        # Initialize the colors
        self.colors = {
            'WHITE': (255, 255, 255),
            'BLACK': (0, 0, 0),
            'GRAY': (128, 128, 128),
            'RED': (255, 0, 0),
            'GREEN': (0, 255, 0),
            'BLUE': (0, 0, 255),
            'YELLOW': (255, 255, 0),
            'WALL':(35, 17, 35),
            'FLOOR':(130, 32, 74),
            'START':(27, 153, 139),
            'END':(255, 253, 130),
            'AGENT': (255, 155, 113),
            'LINE': (131, 144, 250)
            }
        
        # Initialize the font
        self.font = pygame.font.Font(None, 30)

    def draw_maze(self, maze:Maze) -> None:
        """
        Draw the maze on the GUI window.
        
        Args:
            maze; (Maze): The maze instance to draw.
        """
        # Clear the screen
        self.screen.fill(self.colors['GRAY'])

        # Draw the maze cells
        for i, j in np.ndindex(maze.rows, maze.cols):
            cell = maze.get_cell(i, j)
            x = j * 40
            y = i * 40
            color = self.colors['BLACK']
            if cell.visited:
                color = self.colors['FLOOR']
            if cell.is_start:
                color = self.colors['START']
            if cell.is_target:
                color = self.colors['END']
            pygame.draw.rect(self.screen, color, (x, y, 40, 40))
            # pygame.draw.rect(self.screen, self.colors['WHITE'], (x, y, 40, 40), 2)
            # draw the walls
            if cell.walls['N']:
                pygame.draw.line(self.screen, self.colors['WALL'], (x, y), (x + 40, y), 2)
            if cell.walls['S']:
                pygame.draw.line(self.screen, self.colors['WALL'], (x, y + 40), (x + 40, y + 40), 2)
            if cell.walls['E']:
                pygame.draw.line(self.screen, self.colors['WALL'], (x + 40, y), (x + 40, y + 40), 2)
            if cell.walls['W']:
                pygame.draw.line(self.screen, self.colors['WALL'], (x, y), (x, y + 40), 2)
        
        # Update the display
        pygame.display.flip()

    def draw_tile(self, cell:Cell) -> None:
        """
        Draw the tile on the GUI window.
        
        Args:
            maze; (Maze): The maze instance to draw.
        """
        row = cell.row
        col = cell.col
        x = col * 40
        y = row * 40

        color = self.colors['BLACK']
        if cell.visited:
            color = self.colors['FLOOR']
        if cell.is_start:
            color = self.colors['START']
        if cell.is_target:
            color = self.colors['END']

        pygame.draw.rect(self.screen, color, (x, y, 40, 40))

        # pygame.draw.rect(self.screen, self.colors['WHITE'], (x, y, 40, 40), 2)
        # draw the walls
        if cell.walls['N']:
            pygame.draw.line(self.screen, self.colors['WALL'], (x, y), (x + 40, y), 2)
        if cell.walls['S']:
            pygame.draw.line(self.screen, self.colors['WALL'], (x, y + 40), (x + 40, y + 40), 2)
        if cell.walls['E']:
            pygame.draw.line(self.screen, self.colors['WALL'], (x + 40, y), (x + 40, y + 40), 2)
        if cell.walls['W']:
            pygame.draw.line(self.screen, self.colors['WALL'], (x, y), (x, y + 40), 2)
        
        # Update the display
        pygame.display.flip()

    def draw_agent(self, cell) -> None:
        """
        Draw the agent on the GUI window.
        
        Args:
            cell; (Cell): The cell where the agent is.
        """
        x = cell.col * 40 + 20
        y = cell.row * 40 + 20
        pygame.draw.circle(self.screen, self.colors['AGENT'], (x, y), 10)
        pygame.display.flip()

    def draw_trail(self, start_cell, end_cell, prev_trails) -> None:
        """
        Draw the agent on the GUI window.
        
        Args:
            start_cell; (Cell): The cell where the agent is.
            end_cell; (Cell): The cell where the agent is moving to.
            prev_trails; (pygame.Surface): The previous trails drawn on the screen.
        """
        x1 = start_cell.col * 40 + 20
        y1 = start_cell.row * 40 + 20
        x2 = end_cell.col * 40 + 20
        y2 = end_cell.row * 40 + 20

        # pygame.draw.line(self.screen, self.colors['LINE'], start_pos=(x1,y1), end_pos=(x2,y2), width=2)
        if prev_trails == None:
            prev_trails = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        pygame.draw.line(prev_trails, self.colors['LINE'], start_pos=(x1,y1), end_pos=(x2,y2), width=2)
        
        # Update the display
        self.screen.blit(prev_trails, (0, 0))

        pygame.display.flip()
        return prev_trails

    def run(self, maze) -> None:
        """
        Run the GUI to display the maze.
        
        Args:
            maze; (Maze): The maze instance to display.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_maze(maze)
        pygame.quit()

    def simulate(self, maze:Maze, agent:IAgent, show_trail=True) -> None:
        """
        Simulates the agent in the maze.

        Args:
            maze; (Maze): The maze instance to simulate in.
            agent; (IAgent): The agent to simulate.
        """
        running = True
        current_cell = maze.get_cell(*maze.start_indices)
        prev_cell = None
        prev_trails = None
        self.draw_maze(maze)
        input("Press Enter to start the simulation...")
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            if prev_cell != None:
                self.draw_tile(prev_cell)

            if show_trail and prev_cell != None:
                prev_trails = self.draw_trail(prev_cell, current_cell, prev_trails)

            self.draw_agent(current_cell)
            pygame.time.wait(100)

            next_move = agent.get_move(maze, current_cell)
            next_cell = maze.get_next_cell(current_cell, next_move)
            prev_cell = current_cell
            current_cell = next_cell

            if current_cell.is_target:
                running = False

        pygame.quit()