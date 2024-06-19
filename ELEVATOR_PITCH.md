# maze-gen-ai
Repository for generating mazes with generative models.


## Elevator pitch

<table>
  <tr>
    <td>Maze with solution</td>
    <td>Input x (Maze)</td>
    <td>Conditioning y (Path)</td>
  </tr>
  <tr>
    <td><img src="figures/maze_and_path.png" width="250" /></td>
    <td><img src="figures/maze.png" width="250" /></td> 
    <td><img src="figures/path.png" width="250" /></td>
  </tr>
</table>

Given a dataset of $n$ mazes $X \sim p_\text{data}$ where each individual maze $x \in X$ consists of $D\times D$ pixels $x \in \{ 0, 1 \}^{D \times D}$. A pixel value of 1 indicates there is a wall, and 0 indicates no wall. 

Since generating large mazes can be time consuming, depending on the algorithm, we want to learn how to generate new mazes. To do so, we want to learn a distribution with parameters $\theta$, $p_\theta(x)$, that is similar to the real distribution. 

A common issue with mazes generated with probabilistic models is that they have multiple connected components (instead of one), and possibly do not have a path from start to finish. To address the former, we incorporate a term in the loss function to penalize 'islands'. To address the latter, we introduce a conditioning factor $y \in \{ 0, 1 \}^{D \times D}$ that marks the shortest path from the start to the finish with $1$'s. 
\
More formally, we want to generate samples $\hat x \sim p_\theta(x|y)$ where $\theta = \argmax_\theta \quad  p_\text{data}(x); \quad x \sim p_\theta(x|y)$. 

