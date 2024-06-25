#!/bin/bash
python create_datasets.py -s 64 -n 10000 -o datasets/10k_Wilson.npy -g Wilson
python create_datasets.py -s 64 -n 10000 -o datasets/10k_DFS.npy -g RandomizedDFS -b 0.75
python create_datasets.py -s 64 -n 10000 -o datasets/10k_Prim.npy -g Prim
python create_datasets.py -s 64 -n 10000 -o datasets/10k_Fractal.npy -g FractalTessellation -nt 6

python create_datasets.py -s 64 -n 100000 -o datasets/100k_Wilson.npy -g Wilson
python create_datasets.py -s 64 -n 100000 -o datasets/100k_DFS.npy -g RandomizedDFS -b 0.75
python create_datasets.py -s 64 -n 100000 -o datasets/100k_Prim.npy -g Prim
python create_datasets.py -s 64 -n 100000 -o datasets/100k_Fractal.npy -g FractalTessellation -nt 6