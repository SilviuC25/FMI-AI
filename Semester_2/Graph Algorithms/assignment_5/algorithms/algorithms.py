import sys
import os
from collections import deque

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from domain.graph import Graph

def get_connected_components(graph: Graph):
    """
    Time Complexity: O(V + E)
    """
    visited = set()
    components = []

    for vertex in graph.get_vertices():
        if vertex not in visited:
            component = set()
            queue = deque([vertex])
            visited.add(vertex)
            component.add(vertex)

            while queue:
                current = queue.popleft()
                for neighbor in graph.neighbors(current):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        component.add(neighbor)
                        queue.append(neighbor)
            
            components.append(component)
            
    return components

def classify_component(graph: Graph, component: set) -> str:
    """
    Time Complexity: O(V_c + E_c)
    """
    if not component:
        return "General Graph"

    start_node = next(iter(component))
    group = {start_node: 0}
    queue = deque([start_node])
    is_bipartite = True

    while queue:
        current = queue.popleft()
        current_group = group[current]

        for neighbor in graph.neighbors(current):
            if neighbor in component:
                if neighbor not in group:
                    group[neighbor] = 1 - current_group
                    queue.append(neighbor)
                elif group[neighbor] == current_group:
                    is_bipartite = False

    edge_count = sum(len(graph.neighbors(v)) for v in component) // 2
    vertex_count = len(component)

    if not is_bipartite:
        return "General Graph"

    u_count = sum(1 for v in component if group[v] == 0)
    w_count = vertex_count - u_count
    
    is_tree = (edge_count == vertex_count - 1)
    is_complete_bipartite = (edge_count == u_count * w_count)

    if is_tree and is_complete_bipartite:
        return "Tree and Complete Bipartite"
    if is_tree:
        return "Tree"
    if is_complete_bipartite:
        return "Complete Bipartite"
    
    return "Bipartite"

def main():
    graph_filename = "dataset/Connected_Components.txt"
    
    graph = Graph.create_from_file(graph_filename)

    components = get_connected_components(graph)

    print(f"Total connected components: {len(components)}\n")

    for i, component in enumerate(components, 1):
        component_type = classify_component(graph, component)
        vertices_list = sorted(list(component))
        
        print(f"Component {i}:")
        print(f"  Vertices: {vertices_list}")
        print(f"  Classification: {component_type}\n")

if __name__ == "__main__":
    main()