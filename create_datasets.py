from utils import *
from maze import Maze
from generators import RandomizedDFS, Wilson

import argparse
import numpy as np

def main():
    parser = argparse.ArgumentParser(description='Create datasets for the maze solver.')
    parser.add_argument('--maze-size', '-s', type=int, default=64, help='The size in the maze.')
    parser.add_argument('--num-mazes', '-n', type=int, default=10, help='The number of mazes to generate.')
    parser.add_argument('--generator', '-g', type=str, default='Wilson', help='The maze generator to use.',
                        choices=['RandomizedDFS', 'Wilson'], 
                        ) # map to the class
    args = parser.parse_args()

    generator_dict = {'RandomizedDFS': RandomizedDFS, 'Wilson': Wilson}

    dataset = create_dataset(args.num_mazes, args.maze_size, generator_dict[args.generator])
    # save the dataset
    np.save('dataset.npy', dataset)

    print('Dataset created successfully!')

if __name__ == "__main__":
    main()