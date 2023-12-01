from nxdynamics.src.graphs.base import Graph

import networkx as nx
import random

class CompleteGraph(Graph):
  """
  Work with a Complete Graph w/ randomized values at each node.

  Ref: https://en.wikipedia.org/wiki/Complete_graph

  Args:
    size (int): Number of nodes in graph.
    mean (float): Initalize graph where nodes are around the mean.
    std (float): Initalize graph where nodes are around the std.
  """

  def __init__(self,
               size: int,
               mean: float):
    self.G = nx.complete_graph(size)
    self.data = dict()
    self._init_node_value(size=size, mean=mean)
    self._init_edge_value()

  def _init_node_value(self,
                       size: int,
                       mean: float):
    """
    Initalize node values with `randomize_node_values`.
    Function is called at __init__.
    """
    self.data = randomize_node_values(size=size, mean=mean)
    self.set_node_value(self.data)

  def _init_edge_value(self):
    """
    Initalize node values with `randomize_edge_values`.
    Function is called at __init__.
    """
    size = len(self.G.edges.values())
    edge_values = randomize_edge_values(size)
    for edge_ids, value in zip(self.G.edges, edge_values):
      node1, node2 = edge_ids
      self.G[node1][node2]['weight'] = value

def randomize_node_values(size, mean: float):
    """
    Create an dictionary of nodes which have values of (+1) or (-1).
    Args:
      percent (float): Mean value of the values.
    """
    if (mean > 1) or (mean < -1):
      raise ValueError('`mean` must be between -1 and 1.')

    map = float(mean) / 2 + 0.5
    # Generate a random distribution of +1 and -1
    random_values = {key: 1 if random.random() < map else -1 for key in range(size)}
    return random_values

def randomize_edge_values(size) -> list:
    values = np.random.uniform(-1, 1, size)
    return values