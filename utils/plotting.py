import matplotlib.pyplot as plt
import numpy as np

def plot_maze_from_npy(fp, name='maze'):
    maze = np.load(fp)
    maze = maze.astype(int)
    # plot 1s as black squares
    # and 0s as white squares
    # use inverse cmap to make 0s white
    plt.imshow(maze, cmap='gray_r')
    plt.title('Maze (black squares are walls)')
    plt.savefig(f'figures/{name}.png')

def plot_path_from_npy(fp, name='path'):
    path = np.load(fp)
    path = path.astype(int)
    # plot 1s as red squares
    # and 0s as white squares

    plt.imshow(path, cmap='gray_r')
    plt.title('(Optimal) path from entrance to exit (red squares)')
    # make tuples from neighboring 1's in the path
    CELL_PIXELS = 100//path.shape[0]
    LINEWIDTH = (CELL_PIXELS // 2) + 3

    # and plot them as a line
    for i in range(1, path.shape[0]-1):
        for j in range(1, path.shape[1]-1):
            if path[i, j] == 1:
                if path[i-1, j] == 1:
                    plt.plot([j, j], [i-1, i], 'r', linewidth=LINEWIDTH)
                if path[i+1, j] == 1:
                    plt.plot([j, j], [i, i+1], 'r', linewidth=LINEWIDTH)
                if path[i, j-1] == 1:
                    plt.plot([j-1, j], [i, i], 'r', linewidth=LINEWIDTH)
                if path[i, j+1] == 1:
                    plt.plot([j, j+1], [i, i], 'r', linewidth=LINEWIDTH)

    # for the entrance and exit points
    # also draw the line to the edge of the maze
    # to make it look more complete
    
    # find the entrance and exit points (1s on the edge of the maze)

    for i in range(path.shape[0]):
        if path[i, 0] == 1:
            entrance = (0, i)
            plt.plot([entrance[0]-0.5, entrance[0]], [entrance[1], entrance[1]], 'r', linewidth=LINEWIDTH)
        if path[i, -1] == 1:
            exit_ = (path.shape[1]-1, i)
            plt.plot([exit_[0], exit_[0]+0.5], [exit_[1], exit_[1]], 'r', linewidth=LINEWIDTH)

    for j in range(path.shape[1]):
        if path[0, j] == 1:
            entrance = (j, 0)
            plt.plot([entrance[0], entrance[0]], [entrance[1]-0.5, entrance[1]], 'r', linewidth=LINEWIDTH)
        if path[-1, j] == 1:
            exit_ = (j, path.shape[0]-1)
            plt.plot([exit_[0], exit_[0]], [exit_[1], exit_[1]+0.5], 'r', linewidth=LINEWIDTH)

    plt.savefig(f'figures/{name}.png')


def plot_maze_and_path(maze_fp, path_fp):
    maze = np.load(maze_fp)
    maze = maze.astype(int)
    path = np.load(path_fp)
    path = path.astype(int)
    # plot 1s as black squares
    # and 0s as white squares
    # use inverse cmap to make 0s white
    plt.imshow(maze, cmap='gray_r')
    # make tuples from neighboring 1's in the path
    # and plot them as a line
    for i in range(1, path.shape[0]-1):
        for j in range(1, path.shape[1]-1):
            if path[i, j] == 1:
                if path[i-1, j] == 1:
                    plt.plot([j, j], [i-1, i], 'r')
                if path[i+1, j] == 1:
                    plt.plot([j, j], [i, i+1], 'r')
                if path[i, j-1] == 1:
                    plt.plot([j-1, j], [i, i], 'r')
                if path[i, j+1] == 1:
                    plt.plot([j, j+1], [i, i], 'r')

    # for the entrance and exit points
    # also draw the line to the edge of the maze
    # to make it look more complete
    
    # find the entrance and exit points (1s on the edge of the maze)

    for i in range(path.shape[0]):
        if path[i, 0] == 1:
            entrance = (0, i)
            plt.plot([entrance[0]-0.5, entrance[0]], [entrance[1], entrance[1]], 'r')
        if path[i, -1] == 1:
            exit_ = (path.shape[1]-1, i)
            plt.plot([exit_[0], exit_[0]+0.5], [exit_[1], exit_[1]], 'r')

    for j in range(path.shape[1]):
        if path[0, j] == 1:
            entrance = (j, 0)
            plt.plot([entrance[0], entrance[0]], [entrance[1]-0.5, entrance[1]], 'r')
        if path[-1, j] == 1:
            exit_ = (j, path.shape[0]-1)
            plt.plot([exit_[0], exit_[0]], [exit_[1], exit_[1]+0.5], 'r')
    
    # draw the entrance and exit lines
    plt.title('Maze with path (red line) from entrance to exit')
    plt.savefig('figures/maze_and_path.png')

