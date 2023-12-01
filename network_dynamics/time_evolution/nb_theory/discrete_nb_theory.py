from network_dynamics.time_evolution.discrete_base import DiscreteTimeEvolution

class NBTheory(DiscreteTimeEvolution):
  """
  Implementation of belief updating outlined in NB Theory (Dalege et al, 2023).

  Args:
    graph (Graph): Graph with initial conditions of simulation
    beta_pers (float): 
    beta_soc (float): 
    beta_ext (float): 
    asynchronous (bool, optional): Do entities update at different times (asychronously) 
      or simultaneously (synchronous). Defaults to True, asynchronous. 
  """

  def __init__(self,
               graph: Graph,
               beta_pers: float,
               beta_soc: float,
               beta_ext: float,
               asynchronous: bool = True,
               ):
    super().__init__(graph, asynchronous)

  def calc_dissonance(self,
                      node_id: int):
    H = float
    return H