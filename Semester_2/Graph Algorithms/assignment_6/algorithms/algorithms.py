import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from domain.graph import Graph

def find_maximum_cliques(graph: Graph):
    """
    Time Complexity: O(2^V * V^2)
    """
    def is_clique(vertex_set):
        vertex_list = list(vertex_set)
        for i in range(len(vertex_list)):
            for j in range(i + 1, len(vertex_list)):
                u = vertex_list[i]
                w = vertex_list[j]
                if not graph.is_edge(u, w):
                    return False
        return True

    def backtrack(start_index, current_set):
        if is_clique(current_set):
            all_cliques.append(set(current_set))
            
        for i in range(start_index, graph.get_v()):
            current_set.add(vertices[i])
            backtrack(i + 1, current_set)
            current_set.remove(vertices[i])

    all_cliques = []
    vertices = graph.get_vertices()
    
    backtrack(0, set())
    
    if not all_cliques:
        return []
        
    max_size = max(len(clique) for clique in all_cliques)
    return [sorted(list(clique)) for clique in all_cliques if len(clique) == max_size]



def find_k_coloring(graph: Graph, k: int):
    """
    Time Complexity: O(k^V * V)
    """
    vertices = graph.get_vertices()
    colors = {}

    def is_valid(v, color):
        for neighbor in graph.neighbors(v):
            if neighbor in colors and colors[neighbor] == color:
                return False
        return True

    def backtrack(index):
        if index == len(vertices):
            return True
        
        v = vertices[index]
        for c in range(1, k + 1):
            if is_valid(v, c):
                colors[v] = c
                if backtrack(index + 1):
                    return True
                del colors[v]
        return False

    if backtrack(0):
        return colors
    return None

def main():
    graph_filename = "dataset/positives_1_v10_e40.txt"
    graph = Graph.create_from_file(graph_filename)

    print("=== Problem 2: Maximum Cliques ===")
    max_cliques = find_maximum_cliques(graph)
    print(f"Found {len(max_cliques)} maximum cliques:")
    for clique in max_cliques:
        print(f"  {clique}")

    print("\n=== Problem 14: K-Coloring ===")
    k = 7
    coloring = find_k_coloring(graph, k)
    if coloring:
        print(f"Valid {k}-coloring found:")
        for node in sorted(coloring.keys()):
            print(f"  Node {node}: Color {coloring[node]}")
    else:
        print(f"No valid {k}-coloring exists for this graph.")

if __name__ == "__main__":
    main()