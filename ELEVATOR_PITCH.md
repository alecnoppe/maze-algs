
# Elevator pitch
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

A common issue with mazes generated with probabilistic models is that they have multiple connected components (instead of one), and possibly do not have a path from start to finish. To address the former, we incorporate a term in the loss function to penalize 'islands'. To address the latter, we introduce a conditioning factor $y \in \{ 0, 1 \}^{D \times D}$ that marks a shortest path from the start to the finish with $1$'s. 
\
More formally, we want to generate samples $\hat x \sim p_\theta(x|y)$ where $\theta = \argmax_\theta \quad  p_\text{data}(x); \quad x \sim p_\theta(x|y)$. 

## Model

I propose we use a conditional VAE, with encoder

$q_\phi(z|x,y) \sim \mathcal{N}(\mu_\phi, \sigma^2_\phi)$

And decoder

$p_\theta(x|z,y) \sim \text{Bern}(\theta)$

where $x$ is the maze, $y$ is a path from start to finish.

With a learnable prior (either MoG or VampPrior)

#### Model architecture
I think an easy but expressive model would be a UNet-style model (without skip-connections) using residual blocks. 

## Evaluation
There are many cool (perceptual) evaluation metrics we could try for mazes:
- connected components (islands)
- branching factor
- distribution of # edges, average shortest path length
- has path start->end
- how many have start and end
- are there cycles?
    - if yes it is adding new properties to maze, unlike spanning tree algs

We can choose a subset here, but I think we should at least keep the 'islands' metric and 'branching factor', as these can very clearly be connected to the maze generation algorithms.

## Feasibility

This project would be feasible within the week, for three main reasons:
1. We already have the code to generate the mazes, and can generate a flexible amount. We can also choose to vary the maze generation algorithms easily.

2. Everyone is familiar with the model, and the math is not too complex to the point we cannot explain it.

3. There are many tutorials online for image generation with (conditional) VAEs

Since everyone has other commitments, I think it's best if we stick to an 'easy' task. The VAE does not need any fancy layers (attention/recurrence etc.), and could even work reasonably well with only linear/convolutional layers.

