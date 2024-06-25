from utils import *
from maze import Maze
from generators import RandomizedDFS, Wilson, FractalTessellation, Prim

import argparse
import numpy as np

import time


def main():
    parser = argparse.ArgumentParser(description='Create datasets for the maze solver.')
    parser.add_argument('--maze-size', '-s', type=int, default=64, help='The size in the maze.')
    parser.add_argument('--num-mazes', '-n', type=int, default=10, help='The number of mazes to generate.')
    parser.add_argument('--generator', '-g', type=str, default='Wilson', help='The maze generator to use.',
                        choices=['RandomizedDFS', 'Wilson', 'FractalTessellation', 'Prim'], 
                        ) # map to the class
    parser.add_argument('--output', '-o', type=str, default='datasets/dataset.npy', help='The output file to save the dataset to.')
    parser.add_argument('--bias', '-b', type=float, default=0.5, help='The bias for the RandomizedDFS generator.')
    parser.add_argument('--n-tiles', '-nt', type=int, default=6, help='The number of tiling steps for the FractalTessellation generator.')

    args = parser.parse_args()

    generator_dict = {'RandomizedDFS': RandomizedDFS(bias=args.bias), 'Wilson': Wilson(), 'FractalTessellation': FractalTessellation(args.n_tiles), 'Prim': Prim()}

    start_time = time.time()
    dataset = create_dataset(args.num_mazes, args.maze_size, generator_dict[args.generator])
    # save the dataset
    np.save(args.output, dataset)

    end_time = time.time()

    print(f'Time taken to create dataset: {end_time - start_time:.2f} seconds.')

if __name__ == "__main__":
    main()