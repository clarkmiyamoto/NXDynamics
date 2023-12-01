import numpy as np

class SimulationData:
  """ 
  Container for simulation data.

  Attributes:
    num_nodes (int):
    total_steps (int):
    node_value (np.array): Size `num_nodes` * `total_steps`
    adj_matrix (np.array): Size `num_nodes` * `num_nodes` * `total_steps`

  Example:
    ```
    sim_results = SimulationData(num_nodes = 3, total_steps = 100)

    # Update with new data
    new_node_values = np.array([1,2,3])
    new_adj_matrix = np.array([[1,2,3], [4,5,6], [7,8,9]])
    sim_results[0] = (new_node_values, new_adj_matrix)

    # Get data
    sim_results[0]["node_value"], sim_results[0]["adj_matrix"]
    ```
  """

  def __init__(self,
               num_nodes: int,
               total_steps: int):
    self.num_nodes = num_nodes
    self.total_steps = total_steps
    self.node_value = np.zeros((num_nodes, total_steps))
    self.adj_matrix = np.zeros((num_nodes, num_nodes, total_steps))

  def __setitem__(self, i, values):
    """
    Allows for index setting.
    
    Example:
      ```
      sim_results = SimulationData(num_nodes = 3, total_steps = 100)

      # Update with new data
      new_node_values = np.array([1,2,3])
      new_adj_matrix = np.array([[1,2,3], [4,5,6], [7,8,9]])
      sim_results[0] = (new_node_values, new_adj_matrix)
      ```
    """
    if i < 0 or i >= self.total_steps:
        raise IndexError("Index out of range")

    node_value, adj_matrix = values
    self.update(i, node_value, adj_matrix)

  def __getitem__(self, i):
    """ 
    Allows for index referencing.

    Example:
      ```
      sim_results = SimulationData(num_nodes = 3, total_steps = 100)

      # Get data
      sim_results[0]["node_value"], sim_results[0]["adj_matrix"]
      ```
    """
    if i < 0 or i >= self.node_value.shape[1]:
        raise IndexError("Index out of range")

    return {
        "node_value": self.node_value[:, i],
        "adj_matrix": self.adj_matrix[:, :, i]
    }

  def append(self, 
             node_value: np.array,
             adj_matrix: np.array):
    """
    Append `node_value` and `adj_matrix` to end of `self.node_value` and `self.adj_matrix`

    Args: 
      new_vector (np.array): New data. Size `self.num_nodes`.
      new_adj_matrix (np.array): New data. Size `self.num_nodes` * `self.num_nodes`.
    """
    if (len(node_value) != self.node_value.shape[0]):
      raise ValueError("Number of new node values should match the existing nodes")
    if adj_matrix.shape != self.adj_matrix[:, :, -1].shape:
      raise ValueError("Shape of new matrix should match existing adj_matrix shape")

    self.node_value = np.concatenate((self.node_value, np.expand_dims(node_value, axis=1)), axis=1)
    self.adj_matrix = np.dstack((self.adj_matrix, adj_matrix))
    self.num_nodes += 1
  
  def update(self,
             i: int,
             new_vector: np.array,
             new_adj_matrix: np.array):
    """
    Replace node values & adj matrix at time index `i`.
    Replaces values in `self.node_value` and `self.adj_matrix` respectively. 

    Args:
      i (int): Time index of node values.
      new_vector (np.array): New data. Size `self.num_nodes`.
      new_adj_matrix (np.array): New data. Size `self.num_nodes` * `self.num_nodes`.
    """
    self.update_node_value(i=i, new_vector=new_vector)
    self.update_adj_matrix(i=i, new_adj_matrix=new_adj_matrix)

  def update_node_value(self, 
                        i: int, 
                        new_vector: np.array):
    """
    Replace node values vector at time index `i`.

    Args:
      i (int): Time index of node values.
      new_vector (np.array): New data. Size `self.num_nodes`.
    """
    if i < 0 or i >= self.total_steps:
      raise IndexError("Index out of range")

    if len(new_vector) != self.num_nodes:
      raise ValueError("Length of new vector should match the number of nodes")

    self.node_value[:, i] = new_vector
  
  def update_adj_matrix(self, 
                        i: int, 
                        new_adj_matrix: np.array):
    """
    Replace adj_matrix values matrix at time index `i`.

    Args:
      i (int): Time index of matrix values.
      new_adj_matrix (np.array): New data. Size `self.num_nodes` * `self.num_nodes`.
    """
    if i < 0 or i >= self.total_steps:
        raise IndexError("Index out of range")

    if new_adj_matrix.shape != self.adj_matrix[:, :, i].shape:
        raise ValueError("Shape of new matrix should match the existing adjacency matrix")

    self.adj_matrix[:, :, i] = new_adj_matrix

  @staticmethod
  def load(filename: str):
    """
    Load previously saved instance of `SimulationData`

    Args: 
      filename (str): Global path, including name, and extension of file.

    Returns:
      container (SimulationData): Initalized obj with data in `filename`.
    """
    data = np.load(filename, allow_pickle=True)
    
    node_value = data['node_value']
    adj_matrix = data['adj_matrix']
    num_nodes, total_steps = node_value.shape

    container = SimulationData(num_nodes = num_nodes, total_steps=total_steps)
    container.node_value = node_value
    container.adj_matrix = adj_matrix

    return container

  def save(self, filename: str):
    """
    Save current instance of `SimulationData`.

    Args:
      filename (str): Name of file.
    """
    np.savez(filename, node_value=self.node_value, adj_matrix=self.adj_matrix)
