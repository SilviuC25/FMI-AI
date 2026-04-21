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

def compute_neighbors(dist, n):
    neighbors = [[] for _ in range(n + 1)]

    for i in range(1, n + 1):
        arr = []
        for j in range(1, n + 1):
            if i != j:
                arr.append((dist[i][j], j))
        arr.sort()
        neighbors[i] = [city for (_, city) in arr]

    return neighbors

def solve(start, n, neighbors, dist):
  visited = [start]
  total_dist = 0

  while len(visited) < n:
    current_city = visited[-1]
    for next_city in neighbors[current_city]:
      if next_city not in visited:
        visited.append(next_city)
        total_dist += dist[current_city][next_city]
        break

  total_dist += dist[visited[-1]][start]
  visited.append(start)

  print("The total distance is", total_dist)
  print("The result list is", visited)



def main():
    filename = "berlin52.tsp"
    points = read_points(filename)
    dist = compute_all_distances(points)
    n = len(points)
    neighbors = compute_neighbors(dist, n)
    solve(1, n, neighbors, dist)

main()


"""
The result of the Nearest Neighbor Heuristic:

The total distance is 8980.918279329191
The result list is [1, 22, 49, 32, 36, 35, 34, 39, 40, 38, 37, 48, 24, 5, 15, 6, 4, 25, 46, 44, 16, 50, 20, 23, 31, 18, 3, 19, 45, 41, 8, 10, 9, 43, 33, 51, 12, 28, 27, 26, 47, 13, 14, 52, 11, 29, 30, 21, 17, 42, 7, 2, 1]
"""