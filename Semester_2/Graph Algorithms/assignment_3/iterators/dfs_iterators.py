class DFSIterator:
    def __init__(self, graph, start_vertex):
        """
        Time Complexity: O(1)
        """
        self.__graph = graph
        self.__start_vertex = start_vertex
        self.__stack = []
        self.__visited = set()
        self.__parent = {}
        self.__distance = {}
        self.__current = None
        self.first()

    def first(self):
        """
        Time Complexity: O(1)
        """
        self.__stack.clear()
        self.__visited.clear()
        self.__parent.clear()
        self.__distance.clear()
        self.__stack.append((self.__start_vertex, None, 0))
        self.__current = None
        self.next()

    def valid(self):
        """
        Time Complexity: O(1)
        """
        return self.__current is not None

    def get_current(self):
        """
        Time Complexity: O(1) - returns current vertex
        """
        if not self.valid():
            raise ValueError("Iterator is invalid.")
        return self.__current

    def next(self):
        """
        Time Complexity: O(deg(v)) - finds next unvisited node
        """
        while self.__stack:
            vertex, parent, dist = self.__stack.pop()

            if vertex not in self.__visited:
                self.__visited.add(vertex)
                self.__parent[vertex] = parent
                self.__distance[vertex] = dist
                self.__current = vertex

                neighbors = list(self.__graph.neighbors(vertex))
                for neighbor in reversed(neighbors):
                    if neighbor not in self.__visited:
                        self.__stack.append((neighbor, vertex, dist + 1))
                return

        self.__current = None

    def get_path_length(self):
        """
        Time Complexity: O(1)
        """
        return self.__distance[self.__current]

    def get_path(self):
        """
        Time Complexity: O(path_length)
        """
        path = []
        node = self.__current
        while node is not None:
            path.append(node)
            node = self.__parent[node]
        return path[::-1]