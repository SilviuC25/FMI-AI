import heapq
from collections import deque
from domain.graph import Graph

def prim_mst(graph: Graph) -> Graph:
    """
    Time Complexity: O(E log V)
    """
    vertices = graph.get_vertices()
    if not vertices:
        return Graph("undirected", "weighted")

    mst = Graph("undirected", "weighted")
    start_vertex = vertices[0]
    
    mst.add_vertex(start_vertex)
    visited = {start_vertex}
    pq = []

    for neighbor in graph.neighbors(start_vertex):
        cost = graph.get_weight(start_vertex, neighbor)
        heapq.heappush(pq, (cost, start_vertex, neighbor))

    while pq and len(visited) < graph.get_v():
        cost, u, v = heapq.heappop(pq)

        if v in visited:
            continue

        visited.add(v)
        mst.add_vertex(v)
        mst.add_edge(u, v, cost)

        for neighbor in graph.neighbors(v):
            if neighbor not in visited:
                next_cost = graph.get_weight(v, neighbor)
                heapq.heappush(pq, (next_cost, v, neighbor))

    return mst

def get_tree_height(mst: Graph, root: str) -> int:
    """
    Time Complexity: O(V + E)
    """
    if not mst.is_vertex(root):
        raise ValueError(f"Vertex {root} does not exist in the MST.")

    queue = deque([(root, 0)])
    visited = {root}
    max_height = 0

    while queue:
        current, depth = queue.popleft()
        max_height = max(max_height, depth)

        for neighbor in mst.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, depth + 1))

    return max_height

def main():
    graph_filename = "MST.txt"
    root_node = "1"

    graph = Graph.create_from_file(graph_filename)

    mst = prim_mst(graph)
    
    total_cost = sum(mst.get_weight(u, v) for u, v in mst.get_edges())
    height = get_tree_height(mst, root_node)

    print("=== Minimal Spanning Tree (Prim) ===")
    print(f"Total MST Cost: {total_cost}")
    print(f"MST Edges: {mst.get_edges()}")
    
    print("\n=== Tree Height ===")
    print(f"Height from root '{root_node}': {height}")

if __name__ == "__main__":
    main()