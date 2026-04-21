import math

def read_points(filename):
    points = []
    with open(filename) as file:
        for line in file:
            index, x, y = line.split()
            points.append((int(index), float(x), float(y)))
    return points

def eucledian_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def compute_all_distances(points):
    n = len(points)
    dist = [[0.0 for _ in range(n + 1)] for _ in range(n + 1)]

    for index1, x1, y1 in points:
        for index2, x2, y2 in points:
            if index1 != index2:
                d = eucledian_distance(x1, y1, x2, y2)
                dist[index1][index2] = d
                dist[index2][index1] = d

    return dist

def find(parent, x):
    while parent[x] != x:
        x = parent[x]
    return x

def union(parent, a, b):
    ra = find(parent, a)
    rb = find(parent, b)
    parent[rb] = ra

def cheapest_link_tsp(dist, n):
    edges = []
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            edges.append((dist[i][j], i, j))

    edges.sort()

    degree = [0] * (n + 1)
    parent = [i for i in range(n + 1)]
    chosen = []

    for cost, u, v in edges:
        if degree[u] == 2 or degree[v] == 2:
            continue

        ru = find(parent, u)
        rv = find(parent, v)

        if ru == rv and len(chosen) < n - 1:
            continue

        chosen.append((u, v, cost))
        degree[u] += 1
        degree[v] += 1
        union(parent, u, v)

        if len(chosen) == n:
            break

    return chosen

def build_tour(edges, n):
    adj = [[] for _ in range(n + 1)]
    for u, v, _ in edges:
        adj[u].append(v)
        adj[v].append(u)

    tour = [1]
    prev = -1
    current = 1

    while True:
        for nxt in adj[current]:
            if nxt != prev:
                prev, current = current, nxt
                break
        if current == 1:
            break
        tour.append(current)

    tour.append(1)
    return tour

def tour_length(tour, dist):
    total = 0
    for i in range(len(tour) - 1):
        total += dist[tour[i]][tour[i + 1]]
    return total

def main():
    filename = "berlin52.tsp"
    points = read_points(filename)
    dist = compute_all_distances(points)
    n = len(points)

    edges = cheapest_link_tsp(dist, n)
    tour = build_tour(edges, n)
    length = tour_length(tour, dist)

    print("The total distance is", length)
    print("The result list is", tour)

main()

"""
The result of greedy method:
The total distance is 9954.06269813768
The result list is [1, 22, 31, 18, 3, 17, 21, 30, 23, 20, 50, 16, 46, 44, 34, 35, 36, 39, 37, 40, 38, 48, 24, 5, 15, 6, 4, 25, 43, 33, 11, 51, 12, 28, 27, 26, 47, 14, 13, 52, 2, 7, 42, 29, 9, 10, 8, 41, 19, 45, 32, 49, 1]
"""