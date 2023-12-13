from nxdynamics.src.data_structures.simulation_data import SimulationData
from nxdynamics.src.graphs.base import Graph

import numpy as np

class TimeEvolution:

    def __init__(self, graph: Graph):
        self.graph = graph
        self.data = SimulationData(num_nodes=graph.num_nodes, total_steps=1)

    def record_step(self, 
                    node_value: np.array, 
                    adj_matrix: np.array):
        """Record single step of simulation"""
        self.data.append(node_value=node_value, adj_matrix=adj_matrix)