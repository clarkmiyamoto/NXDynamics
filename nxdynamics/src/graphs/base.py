import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from typing import Dict, Tuple

class Graph:

  def _init_node_value(self):
    raise NotImplemented

  def _init_edge_value(self):
    raise NotImplemented

  @property
  def node_values(self) -> np.array:
    return np.array([value[1] for value in self.G.nodes(data='value')])

  @property
  def node_mean(self) -> float:
    return self.node_values.mean()

  @property
  def node_std(self) -> float:
    values = np.array([value[1] for value in self.G.nodes(data='value')])
    return self.node_values.std()

  @property
  def adj_matrix(self) -> np.array:
    return nx.to_numpy_array(self.G)

  def set_node_value(self, node_values: Dict[int, float]):
    """
    Set a value at a specified node.

    Args:
      node_values (Dict[int, float]): Keys are the node IDs. Values are the value of the nodes.
    """
    nx.set_node_attributes(self.G, node_values, 'value')

  def set_edge_value(self, edge_values: Dict[Tuple[int, int], float]):
    for edge, value in edge_values.items():
      if self.G.has_edge(*edge):  # Check if the edge exists in the graph
        self.G[edge[0]][edge[1]]['weight'] = value  # Assign the value to the 'weight' attribute
      else:
        # Edge doesn't exist in the graph, you may want to handle this case
        raise ValueError(f'Edge between nodes {edge} does not exist.')

  def show(self,
           edge: bool = False):
    # Node labels
    node_labels = {node: round(self.G.nodes[node]['value'], 3) for node in self.G.nodes()}

    # Edge labels (with weights)
    edge_labels = {(u, v): round(data['weight'], 3) for u, v, data in self.G.edges(data=True)}

    # Draw the graph with node and edge labels
    nx.draw(self.G, with_labels=True, labels=node_labels, node_color='skyblue', node_size=500, font_weight='bold')

    if (edge == True):
      nx.draw_networkx_edge_labels(self.G, pos=nx.spring_layout(self.G), edge_labels=edge_labels)
    plt.show()