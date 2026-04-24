from iterators.bfs_iterators import BFSIterator
from iterators.dfs_iterators import DFSIterator

class Graph:
  def __init__(self, direction: str, weight_type: str):
    """
    Time Complexity: O(1) - because only constant time initializations
    are performed for lists, dictionaries and variables.
    """
    self.__vertices = []
    self.__in_edge = {}
    self.__out_edge = {}
    self.__edge_cost = {}
    self.__number_of_edges = 0

    self.__is_directed = True if direction == "directed" else False
    self.__is_weighted = True if weight_type == "weighted" else False


  def is_vertex(self, vertex: str):
    """
    Time Complexity: O(V) - because we search for the vertex inside
    the list of vertices, where V is the number of vertices.
    """
    return vertex in self.__vertices


  def is_edge(self, node: str, neighbor: str):
    """
    Time Complexity: O(deg(node)) - because we search for neighbor
    inside the adjacency list of node.
    """
    return neighbor in self.__out_edge[node]


  def add_vertex(self, vertex: str):
    """
    Time Complexity: O(V) - because we check if the vertex already
    exists in the list of vertices before adding it.
    """
    if self.is_vertex(vertex):
      raise ValueError(f"Vertex {vertex} already exists.")

    self.__vertices.append(vertex)
    self.__in_edge[vertex] = []
    self.__out_edge[vertex] = []


  def add_edge(self, node: str, neighbor: str, cost: float | None = None):
    """
    Time Complexity: O(V + deg(node)) - because we check if both vertices
    exist (O(V)) and if the edge already exists in adjacency list (O(deg(node))).
    """

    if not self.is_vertex(node):
      self.add_vertex(node)

    if not self.is_vertex(neighbor):
      self.add_vertex(neighbor)

    if self.is_edge(node, neighbor):
      raise ValueError(f"Pair {node}, {neighbor} already form an edge.")

    if self.__is_weighted:
      if cost is None:
        cost = 0
      self.__edge_cost[(node, neighbor)] = cost

    self.__out_edge[node].append(neighbor)
    self.__in_edge[neighbor].append(node)

    if not self.__is_directed:
      self.__out_edge[neighbor].append(node)
      self.__in_edge[node].append(neighbor)

      if self.__is_weighted:
        self.__edge_cost[(neighbor, node)] = cost

    self.__number_of_edges += 1


  def get_v(self):
    """
    Time Complexity: O(1) - returning length of list is constant.
    """
    return len(self.__vertices)


  def get_e(self):
    """
    Time Complexity: O(1) - value stored in variable.
    """
    return self.__number_of_edges


  def neighbors(self, vertex: str):
    """
    Time Complexity: O(deg(vertex)) - because a copy of the adjacency
    list is created.
    """
    return list(self.__out_edge[vertex])


  def inbound_neighbors(self, vertex: str):
    """
    Time Complexity: O(deg_in(vertex)) - because a copy of inbound
    adjacency list is created.
    """
    return list(self.__in_edge[vertex])


  def get_vertices(self):
    """
    Time Complexity: O(V) - because we return a copy of the list.
    """
    return list(self.__vertices)


  def get_edges(self):
    """
    Time Complexity: O(V + E) - because we iterate through all vertices
    and through all their neighbors.
    """
    edges = []

    for vertex in self.__vertices:
      for neighbor in self.__out_edge[vertex]:

        if self.__is_directed:
          edges.append((vertex, neighbor))

        else:
          if vertex < neighbor:
            edges.append((vertex, neighbor))

    return edges


  def __str__(self):
    """
    Time Complexity: O(V + E) - because we iterate through vertices
    and edges to construct the string representation.
    """

    direction = "directed" if self.__is_directed else "undirected"
    weight_type = "weighted" if self.__is_weighted else "unweighted"

    str_to_return = f"{direction} {weight_type}\n"

    for vertex in self.__vertices:
      if len(self.__out_edge[vertex]) == 0 and len(self.__in_edge[vertex]) == 0:
        str_to_return += vertex + "\n"

    for (node, neighbor) in self.get_edges():

      if self.__is_weighted:
        cost = self.__edge_cost[(node, neighbor)]
        str_to_return += f"{node} {neighbor} {cost}\n"

      else:
        str_to_return += f"{node} {neighbor}\n"

    return str_to_return


  def remove_edge(self, node: str, neighbor: str):
    """
    Time Complexity: O(deg(node)) - because we search and remove
    neighbor from adjacency list.
    """

    if neighbor in self.__out_edge[node]:

      self.__out_edge[node].remove(neighbor)
      self.__in_edge[neighbor].remove(node)

      if self.__is_weighted:
        del self.__edge_cost[(node, neighbor)]

      if not self.__is_directed:

        self.__out_edge[neighbor].remove(node)
        self.__in_edge[node].remove(neighbor)

        if self.__is_weighted:
          del self.__edge_cost[(neighbor, node)]

      self.__number_of_edges -= 1


  def remove_vertex(self, vertex: str):
    """
    Time Complexity: O(V + E) - because all inbound and outbound edges
    of the vertex are removed.
    """

    if vertex not in self.__vertices:
      raise ValueError(f"Vertex {vertex} does not exist.")

    for neighbor in list(self.__out_edge[vertex]):
      self.remove_edge(vertex, neighbor)

    for neighbor in list(self.__in_edge[vertex]):
      self.remove_edge(neighbor, vertex)

    del self.__out_edge[vertex]
    del self.__in_edge[vertex]

    self.__vertices.remove(vertex)


  def set_weight(self, node: str, neighbor: str, cost: float):
    """
    Time Complexity: O(1) - dictionary update.
    """

    if not self.__is_weighted:
      raise ValueError("Graph is unweighted.")

    if not self.is_edge(node, neighbor):
      raise ValueError(f"The pair ({node}, {neighbor}) is not an edge.")

    self.__edge_cost[(node, neighbor)] = cost

    if not self.__is_directed:
      self.__edge_cost[(neighbor, node)] = cost


  def get_weight(self, node: str, neighbor: str):
    """
    Time Complexity: O(1) - dictionary lookup.
    """

    if not self.__is_weighted:
      raise ValueError("Graph is unweighted.")

    if not self.is_edge(node, neighbor):
      raise ValueError(f"The pair ({node}, {neighbor}) is not an edge.")

    return self.__edge_cost[(node, neighbor)]


  def change_if_directed(self, new_is_directed: bool):
    """
    Time Complexity: O(V + E) - because we iterate through all edges
    to adapt them to the new graph type.
    """

    if self.__is_directed == new_is_directed:
      return

    if not new_is_directed:

      for (node, neighbor) in self.get_edges():

        if not self.is_edge(neighbor, node):
          self.__out_edge[neighbor].append(node)
          self.__in_edge[node].append(neighbor)

          if self.__is_weighted:
            self.__edge_cost[(neighbor, node)] = self.__edge_cost[(node, neighbor)]

    else:

      edges = list(self.get_edges())

      for (node, neighbor) in edges:
        if self.is_edge(neighbor, node) and node > neighbor:
          self.remove_edge(neighbor, node)

    self.__is_directed = new_is_directed


  def change_if_weighted(self, new_is_weighted: bool):
    """
    Time Complexity: O(E) - because we iterate through all edges
    to assign or remove weights.
    """

    if self.__is_weighted == new_is_weighted:
      return

    if new_is_weighted:

      for (node, neighbor) in self.get_edges():
        self.__edge_cost[(node, neighbor)] = 0

        if not self.__is_directed:
          self.__edge_cost[(neighbor, node)] = 0

    else:

      self.__edge_cost.clear()

    self.__is_weighted = new_is_weighted


  def BFS_iter(self, start_vertex):
    """
    Time Complexity: O(1) - creates iterator object.
    """
    if not self.is_vertex(start_vertex):
      raise ValueError("Invalid start vertex")

    return BFSIterator(self, start_vertex)


  def DFS_iter(self, start_vertex):
    """
    Time Complexity: O(1) - creates iterator object.
    """
    if not self.is_vertex(start_vertex):
      raise ValueError("Invalid start vertex")

    return DFSIterator(self, start_vertex)


  def create_from_file(filename: str):
    """
    Time Complexity: O(V + E)
    """
    with open(filename, "r") as file:
      lines = [line.strip() for line in file if line.strip()]

      if not lines:
        raise ValueError("File is empty.")
      
      first_line = lines[0].split()

      if len(first_line) != 2:
        raise ValueError("The valid first line format: '$direction $weight_type'")
      
      direction, weight_type = first_line

      graph = Graph(direction, weight_type)

      for line in lines[1:]:
        parts = line.split()

        if len(parts) == 1:
          vertex = parts[0]
          graph.add_vertex(vertex)
        elif len(parts) == 2:
          node, neighbor = parts
          graph.add_edge(node, neighbor)
        elif len(parts) == 3:
          node, neighbor, cost = parts
          cost = float(cost)
          graph.add_edge(node, neighbor, cost)
        else:
          raise ValueError(f"Invalid line: {line}")
        
      return graph
          