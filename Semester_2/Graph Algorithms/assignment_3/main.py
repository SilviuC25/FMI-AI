from domain.graph import Graph
from algorithms.algorithms import read_positions, dijkstra, a_star

def main():
    graph_filename = "positive_only_dataset/positives_5_v1000_e4000.txt"
    positions_filename = "positive_only_dataset/positives_5_vertex_positions.txt"
    start_node = "344"
    end_node = "963"

    graph = Graph.create_from_file(graph_filename)
    positions = read_positions(positions_filename)

    path_d, cost_d, time_d, metrics_d = dijkstra(graph, start_node, end_node)
    
    path_a, cost_a, time_a, metrics_a = a_star(graph, start_node, end_node, positions)

    print("=== Minimum Cost Walk Result ===")
    print(f"Start: {start_node}, End: {end_node}")
    print("-" * 30)
    
    print(f"Dijkstra:")
    print(f"  Time: {time_d:.4f} ms")
    print(f"  Cost: {cost_d}")
    print(f"  Path: {path_d}")
    print()
    
    print(f"A* Algorithm:")
    print(f"  Time: {time_a:.4f} ms")
    print(f"  Cost: {cost_a}")
    print(f"  Path: {path_a}")
    
    print("\n=== Efficiency Metrics ===")
    print(f"Dijkstra Metrics: Weight Calls: {metrics_d['get_weight']}, PQ Push: {metrics_d['pq_push']}, PQ Pop: {metrics_d['pq_pop']}")
    print(f"A* Metrics:       Weight Calls: {metrics_a['get_weight']}, PQ Push: {metrics_a['pq_push']}, PQ Pop: {metrics_a['pq_pop']}")
    print("-" * 30)

if __name__ == "__main__":
    main()