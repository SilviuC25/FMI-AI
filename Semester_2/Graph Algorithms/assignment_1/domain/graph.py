class Graph:
  def __init__(self):
    """
    Time Complexity: O(1) - because only constant time initializations
    are performed for lists, dictionaries and variables.
    """
    self.__vertices = []
    self.__in_edge = {}
    self.__out_edge = {}
    self.__number_of_edges = 0
  
  def is_vertex(self, vertex: str):
    """
    Time Complexity: O(V) - because we search for the vertex inside
    the list of vertices, where V is the number of vertices.
    """
    return vertex in self.__vertices

  def is_edge(self, node: str, neighbor: str):
    """
    Time Complexity: O(deg(node)) - because we search for neighbor inside
    the list of outbound neighbors of node, where deg(node) is the
    out-degree of the node.
    """
    return neighbor in self.__out_edge[node]

  def add_vertex(self, vertex: str):
    """
    Time Complexity: O(V) - because we check if the vertex already exists
    in the list of vertices before adding it.
    """
    if self.is_vertex(vertex):
      raise ValueError(f"Vertex {vertex} already exists.")
    
    self.__vertices.append(vertex)
    self.__in_edge[vertex] = []
    self.__out_edge[vertex] = []

  def add_edge(self, node: str, neighbor: str):
    """
    Time Complexity: O(V + deg(node)) - because we check if both vertices
    exist in the list of vertices (O(V)) and then check if the edge already
    exists in the adjacency list of node (O(deg(node))).
    """
    if not self.is_vertex(node):
      raise ValueError(f"Vertex {node} does not exist.")
    if not self.is_vertex(neighbor):
      raise ValueError(f"Vertex {neighbor} does not exist.") 
    if self.is_edge(node, neighbor):
      raise ValueError(f"Pair {node}, {neighbor} already form an edge.")
    
    self.__out_edge[node].append(neighbor)
    self.__in_edge[neighbor].append(node)
    self.__number_of_edges = self.__number_of_edges + 1

  def get_v(self):
    """
    Time Complexity: O(1) - because returning the length of a list
    is a constant time operation.
    """
    return len(self.__vertices)
  
  def get_e(self):
    """
    Time Complexity: O(1) - because the number of edges is stored
    in a variable and returned directly.
    """
    return self.__number_of_edges
  
  def neighbors(self, vertex: str):
    """
    Time Complexity: O(deg(vertex)) - because a copy of the list of
    outbound neighbors is created, where deg(vertex) is the out-degree.
    """
    return list(self.__out_edge[vertex])
  
  def inbound_neighbors(self, vertex: str):
    """
    Time Complexity: O(deg_in(vertex)) - because a copy of the list of
    inbound neighbors is created, where deg_in(vertex) is the in-degree.
    """
    return list(self.__in_edge[vertex])
    
  def get_vertices(self):
    """
    Time Complexity: O(V) - because a copy of the list of vertices
    is created, where V is the number of vertices.
    """
    return list(self.__vertices)
  
  def get_edges(self):
    """
    Time Complexity: O(V + E) - because we iterate through all vertices
    and through all their neighbors, effectively iterating through
    all edges, where V is the number of vertices and E is the number of edges.
    """
    edges = []

    for vertex in self.__vertices:
      for neighbor in self.neighbors(vertex):
        edges.append((vertex, neighbor))

    return edges
  
  def __str__(self):
    """
    Time Complexity: O(V + E) - because we iterate through all vertices
    and through all their outbound edges in order to build the string
    representation of the graph.
    """
    str_to_return = "directed unweighted\n"

    for vertex in self.__vertices:
      if not self.__out_edge[vertex]:
        str_to_return += vertex
        str_to_return += "\n"
      else:
        for neighbor in self.neighbors(vertex):
          str_to_return += f"{vertex} {neighbor}\n"

    return str_to_return

  def remove_edge(self, node: str, neighbor: str):
    """
    Time Complexity: O(deg(node)) - because we search and remove the
    neighbor from the adjacency list of node, where deg(node) is the
    out-degree of the node.
    """
    if neighbor in self.__out_edge[node]:
      self.__out_edge[node].remove(neighbor)
      self.__in_edge[neighbor].remove(node)
      self.__number_of_edges = self.__number_of_edges - 1
  
  def remove_vertex(self, vertex: str):
    """
    Time Complexity: O(V + E) - because we remove all inbound and outbound
    edges of the vertex, iterating through its neighbors and inbound
    neighbors, and then remove the vertex itself from the list.
    """
    if not vertex in self.__vertices:
      raise ValueError(f"Vertex {vertex} does not exist.")
    
    for neighbor in list(self.__out_edge[vertex]):
      self.remove_edge(vertex, neighbor)

    for neighbor in list(self.__in_edge[vertex]):
      self.remove_edge(neighbor, vertex)

    del self.__in_edge[vertex]
    del self.__out_edge[vertex]

    self.__vertices.remove(vertex)