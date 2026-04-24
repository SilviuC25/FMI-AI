from domain.graph import Graph

def test_graph(file_name):
    print(f"\n================ {file_name} ================")

    g = Graph.create_from_file(file_name)

    print("\n=== GRAPH ===")
    print(g)

    print("Vertices:", g.get_vertices())
    print("Edges:", g.get_edges())
    print("Number of vertices:", g.get_v())
    print("Number of edges:", g.get_e())

    vertices = g.get_vertices()
    if not vertices:
        return

    start = vertices[0]

    print(f"\n=== BFS from {start} ===")
    bfs = g.BFS_iter(start)

    while True:
        try:
            bfs.next() 
            print(
                "Node:", bfs.get_current(),
                "| Distance:", bfs.get_path_length(),
                "| Path:", " -> ".join(bfs.get_path())
            )
        except ValueError:
            break

    print(f"\n=== DFS from {start} ===")
    dfs = g.DFS_iter(start)
        
    while True:
        try:
            dfs.next()
            print(
                "Node:", dfs.get_current(),
                "| Distance:", dfs.get_path_length(),
                "| Path:", " -> ".join(dfs.get_path())
            )
        except ValueError:
            break

    print("\n=== SIMPLE MODIFICATIONS ===")

    try:
        g.add_vertex("new_vertex")
        print("Added vertex new_vertex")
    except:
        pass

    if len(vertices) >= 2:
        try:
            g.add_edge(vertices[0], "new_vertex")
            print(f"Added edge {vertices[0]} -> new_vertex")
        except:
            pass

    print("\nGraph after additions:")
    print(g)

    edges = g.get_edges()
    if edges:
        node, neighbor = edges[0]
        g.remove_edge(node, neighbor)
        print(f"Removed edge ({node}, {neighbor})")

    print("\nGraph after removing an edge:")
    print(g)

    print("\nToggle directed/undirected:")
    g.change_if_directed(not g._Graph__is_directed)
    print(g)

    print("\nToggle weighted/unweighted:")
    g.change_if_weighted(not g._Graph__is_weighted)
    print(g)

    print("============================================\n")


def main():
    files = ["Graph1.txt", "Graph2.txt", "Graph3.txt", "Graph4.txt"]

    for file in files:
        try:
            test_graph(file)
        except Exception as e:
            print(f"Error in {file}: {e}")


if __name__ == "__main__":
    main()