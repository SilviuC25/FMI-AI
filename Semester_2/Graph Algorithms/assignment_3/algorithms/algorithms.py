import heapq
import time
import math
from domain.graph import Graph

def read_positions(filename: str):
    """
    Time Complexity: O(V) - we read all vertices from the file
    """
    positions = {}
    with open(filename, "r") as file:
        for line in file:
            if line.startswith("vertex_name") or not line.strip():
                continue
            parts = line.strip().split(',')
            if len(parts) == 3:
                positions[parts[0]] = (float(parts[1]), float(parts[2]))
    return positions

def euclidean_distance(pos1: tuple, pos2: tuple):
    """
    Time Complexity: O(1)
    """
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def dijkstra(graph: Graph, start: str, end: str):
    """
    Time Complexity: O(E log V)
    """
    start_time = time.perf_counter()
    
    pq = []
    heapq.heappush(pq, (0, start))
    
    distances = {start: 0}
    parent = {start: None}
    
    metrics = {"get_weight": 0, "pq_push": 1, "pq_pop": 0}
    
    while pq:
        current_dist, current = heapq.heappop(pq)
        metrics["pq_pop"] += 1
        
        if current == end:
            break
            
        if current_dist > distances.get(current, float('inf')):
            continue
            
        for neighbor in graph.neighbors(current):
            cost = graph.get_weight(current, neighbor)
            metrics["get_weight"] += 1
            
            new_dist = current_dist + cost
            
            if new_dist < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_dist
                parent[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))
                metrics["pq_push"] += 1
                
    end_time = time.perf_counter()
    execution_time = (end_time - start_time) * 1000
    
    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        curr = parent.get(curr, None)
        if curr == start:
            path.append(curr)
            break
            
    path.reverse()
    
    return path if len(path) > 1 or start == end else [], distances.get(end, -1), execution_time, metrics

def a_star(graph: Graph, start: str, end: str, positions: dict):
    """
    Time Complexity: O(E log V) - similar to Dijkstra
    """
    start_time = time.perf_counter()
    
    pq = []
    heapq.heappush(pq, (0, 0, start))
    
    g_costs = {start: 0}
    parent = {start: None}
    
    metrics = {"get_weight": 0, "pq_push": 1, "pq_pop": 0}
    
    while pq:
        _, current_g, current = heapq.heappop(pq)
        metrics["pq_pop"] += 1
        
        if current == end:
            break
            
        if current_g > g_costs.get(current, float('inf')):
            continue
            
        for neighbor in graph.neighbors(current):
            weight = graph.get_weight(current, neighbor)
            metrics["get_weight"] += 1
            
            new_g = current_g + weight
            
            if new_g < g_costs.get(neighbor, float('inf')):
                g_costs[neighbor] = new_g
                parent[neighbor] = current
                
                h_cost = euclidean_distance(positions[neighbor], positions[end])
                f_cost = new_g + h_cost
                
                heapq.heappush(pq, (f_cost, new_g, neighbor))
                metrics["pq_push"] += 1
                
    end_time = time.perf_counter()
    execution_time = (end_time - start_time) * 1000
    
    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        curr = parent.get(curr, None)
        if curr == start:
            path.append(curr)
            break
            
    path.reverse()
    
    return path if len(path) > 1 or start == end else [], g_costs.get(end, -1), execution_time, metrics