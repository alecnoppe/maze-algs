from generators.IGenerator import IGenerator
from maze.Maze import Maze, Cell

from collections import deque
import numpy as np
from itertools import product


class Prim(IGenerator):
    def frontier_insert(self, frontier, maze:Maze, vertex_indices, visited_indices):
        """
        Given most-recent position (vertex_indices), add all (unvisited) neighbors to the frontier.

        Args:

        Returns:

        """
        vertex = maze.get_cell(*vertex_indices)
        vertex.visit()
        possible_directions = maze.get_unvisited_neighbors_directions(vertex)
        for possible_direction in possible_directions:
            neighbor = maze.get_next_cell(vertex, possible_direction)
            # insert into frontier
            i, j = neighbor.row, neighbor.col
            # Check if we have already visited this neighbor
            # If so, skip this iteration
            if (i,j) in visited_indices:
                continue
            # Insert the neighbor into the frontier dictionary
            if frontier.get((i,j)) is not None:
                frontier[(i,j)].append((vertex_indices, possible_direction))
            else:
                frontier[(i,j)] = [(vertex_indices, possible_direction)]
        return frontier

    def generate(self, maze: Maze) -> None:
        """
        Generate a maze with the Randomized Prim's algorithm.

        Works as follows:
        1. Choose a random node v from the unconnected graph G 
            and make a set V = {v}
        2. Randomly select an edge that bridges the frontier of V
            ie edges that connect vi in V to vj not in V
        3. Add that edge to the MST and add vj to V
        4. Repeat steps 2 and 3 until all vertices are visited
        """
        # Define inverse directions lookup table
        inverse_directions = {
            "N":"S",
            "E":"W",
            "S":"N",
            "W":"E"
        }
        # Create a set of unvisited vertex indices
        unvisited_vertex_indices = set()
        for i, j in product(np.arange(maze.rows), np.arange(maze.cols)):
            unvisited_vertex_indices.add((i,j))
        # Create a set of visited vertex indices
        visited_vertex_indices = set()
        start_vertex_indices = unvisited_vertex_indices.pop()
        visited_vertex_indices.add(start_vertex_indices)

        frontier = self.frontier_insert(dict(), maze, start_vertex_indices, visited_vertex_indices)
        
        while unvisited_vertex_indices:
            # Pick a random cell on the frontier of the current MST
            keys_list = list(frontier.keys())
            random_idx = np.random.randint(0, len(keys_list))
            frontier_neighbor_idx = keys_list[random_idx]
            reachable_from = frontier.pop(frontier_neighbor_idx)
            seen_cell_tuple = reachable_from[np.random.randint(0, len(reachable_from))]
            # Remove wall between seen cell and frontier cell
            seen_cell = maze.get_cell(*seen_cell_tuple[0])
            seen_cell.remove_wall(seen_cell_tuple[1])
            # Remove wall (inverse direction) from frontier cell
            new_cell = maze.get_cell(*frontier_neighbor_idx)
            new_cell.remove_wall(inverse_directions[seen_cell_tuple[1]])
            
            # Add all neighbors of the new cell to the frontier dictionary
            frontier = self.frontier_insert(frontier, maze, frontier_neighbor_idx, visited_vertex_indices)
            # Remove from unvisited index set and add to visited index set
            visited_vertex_indices.add(frontier_neighbor_idx)
            unvisited_vertex_indices.remove(frontier_neighbor_idx)
