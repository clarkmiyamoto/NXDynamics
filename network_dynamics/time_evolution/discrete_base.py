class DiscreteTimeEvolution:
  """
  
  Args:
    graph (Graph): Graph with initial conditions of simulation
    asynchronous (bool, optional): Do entities update at different times (asychronously) 
      or simultaneously (synchronous). Defaults to True, asynchronous.
  """
  
  def __init__(self,
               graph: Graph,
               asynchronous: bool = True):
    self.graph = graph
    self.asynchronous = asynchronous

  def noise(self):
    raise NotImplemented

  def time_evolution(self):
    raise NotImplemented