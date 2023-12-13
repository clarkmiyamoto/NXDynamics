from nxdynamics.src.time_evolution.discrete_base import DiscreteTimeEvolution
from nxdynamics.src.graphs.base import Graph

import numpy as np
import random
from tqdm import tqdm

class GlaubberDynamics(DiscreteTimeEvolution):

    def __init__(self,
                 graph: Graph,
                 beta: float,
                 asynchronous: bool = True,
                 ):
        super().__init__(graph=graph, asynchronous=asynchronous)
        self.beta = beta

    def calc_deltaH(self, node_id) -> float:
        spins = self.graph.node_values
        adj_matrix = self.graph.adj_matrix
        selected_spin = spins[node_id]
        indices = np.arange(len(spins)) != node_id # will skip entries with `node_id`
        
        # Determine current energy
        # \sum_{neighbors around `node_id` := j} - A_{node_id, j} sigma_j selected_spin
        current_H = - np.dot(adj_matrix[node_id][indices], spins[indices] * selected_spin)
        
        # Determine new energy if spin of interest would flip
        new_H = - np.dot(adj_matrix[node_id][indices], spins[indices] * -1 * selected_spin)

        deltaH = new_H - current_H

        return deltaH

    def calc_probability(self, 
                         beta: float, 
                         deltaH: float):
        return 1/(1 + np.exp(beta * deltaH))

    def flip_spin(self, node_id):
        new_value = -1 * self.graph.node_values[node_id]
        self.graph.set_node_value(node_values={node_id:new_value})
        
    def run_sweep(self):
        # Randomly choose a `node_id`. 
        # This will the spin we'll attempt to flip
        num_nodes = self.graph.num_nodes
        node_id = random.randrange(0, num_nodes)

        # Sum the spins
        deltaH = self.calc_deltaH(node_id=node_id)

        # Calc probability to flip spin `node_id`
        probability_to_flip = self.calc_probability(beta=self.beta, deltaH=deltaH)

        if random.random() < probability_to_flip:
            self.flip_spin(node_id=node_id)
        
        # Record this sweep
        new_node_values = self.graph.node_values
        new_adj_matrix = self.graph.adj_matrix
        self.record_step(node_value=new_node_values, adj_matrix=new_adj_matrix)
    
    def run_simulation(self, total_steps):
        for i in tqdm(range(total_steps)):
            self.run_sweep()



