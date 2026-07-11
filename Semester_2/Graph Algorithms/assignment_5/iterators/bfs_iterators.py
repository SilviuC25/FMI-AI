from collections import deque

class BFSIterator:
    def __init__(self, graph, start_vertex):
        """
        Time Complexity: O(1)
        """
        self.__graph = graph
        self.__start_vertex = start_vertex
        self.__queue = deque()
        self.__visited = set()
        self.__parent = {}
        self.__distance = {}
        self.__current = None
        self.first()

    def first(self):
        """
        Time Complexity: O(1)
        """
        self.__queue.clear()
        self.__visited.clear()
        self.__parent.clear()
        self.__distance.clear()
        self.__visited.add(self.__start_vertex)
        self.__parent[self.__start_vertex] = None
        self.__distance[self.__start_vertex] = 0
        self.__queue.append(self.__start_vertex)
        self.__current = self.__start_vertex

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
        Time Complexity: O(deg(v)) - processes neighbors of the popped node
        """
        if not self.valid():
            raise ValueError("Iterator is invalid.")

        if not self.__queue:
            self.__current = None
            return

        node = self.__queue.popleft()
        for neighbor in self.__graph.neighbors(node):
            if neighbor not in self.__visited:
                self.__visited.add(neighbor)
                self.__parent[neighbor] = node
                self.__distance[neighbor] = self.__distance[node] + 1
                self.__queue.append(neighbor)

        if self.__queue:
            self.__current = self.__queue[0]
        else:
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