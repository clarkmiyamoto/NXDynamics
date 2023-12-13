from nxdynamics.src.time_evolution.base import TimeEvolution
from nxdynamics.src.graphs.base import Graph

class DiscreteTimeEvolution(TimeEvolution):
  """
  
  Args:
    graph (Graph): Graph with initial conditions of simulation
    asynchronous (bool, optional): Do entities update at different times (asychronously) 
      or simultaneously (synchronous). Defaults to True, asynchronous.
  """
  
  def __init__(self,
               graph: Graph,
               asynchronous: bool = True):
    super().__init__(graph=graph)
    self.asynchronous = asynchronous