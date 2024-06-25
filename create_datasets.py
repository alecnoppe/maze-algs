import subprocess
import argparse
import numpy as np
import time
import os

from utils import *


def main():
    parser = argparse.ArgumentParser(description='Create datasets for the maze solver.')
    parser.add_argument('--maze-size', '-s', type=int, default=64, help='The size in the maze.')
    parser.add_argument('--num-mazes-per-process', '-n', type=int, default=10, help='The number of mazes to generate.')
    parser.add_argument('--generator', '-g', type=str, default='Wilson', help='The maze generator to use.',
                        choices=['RandomizedDFS', 'Wilson', 'FractalTessellation', 'Prim'], 
                        ) # map to the class
    parser.add_argument('--output', '-o', type=str, default='datasets/dataset.npy', help='The output file to save the dataset to.')
    parser.add_argument('--processes', '-p', type=int, default=1, help='The number of processes to use. Default is 1.')
    parser.add_argument('--bias', '-b', type=float, default=0.5, help='The bias for the RandomizedDFS generator.')
    parser.add_argument('--n-tiles', '-nt', type=int, default=6, help='The number of tiling steps for the FractalTessellation generator.')

    args = parser.parse_args()

    start_time = time.time()

    processes = []

    for i in range(args.processes):
        p = subprocess.Popen(['python', 'create_dataset.py', 
                          '--maze-size', str(args.maze_size), 
                          '--num-mazes', str(args.num_mazes_per_process), 
                          '--generator', args.generator, 
                          '--bias', str(args.bias),
                          '--n-tiles', str(args.n_tiles),
                          '--output', f'datasets/dataset_{i}.npy'])
        
        processes.append(p)
    
    z = [p.wait() for p in processes]

    end_time = time.time()

    print(f'Time taken to create dataset: {end_time - start_time:.2f} seconds.')

    # concatenate the datasets
    datasets = [np.load(f'datasets/dataset_{i}.npy') for i in range(args.processes)]
    dataset = np.concatenate(datasets, axis=0)
    # save the dataset
    np.save(args.output, dataset)

    # remove the temporary datasets
    for i in range(args.processes):
        os.remove(f'datasets/dataset_{i}.npy')

if __name__ == "__main__":
    main()