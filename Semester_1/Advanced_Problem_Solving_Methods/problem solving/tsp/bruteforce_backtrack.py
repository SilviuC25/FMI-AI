import math

counter = 0
MAX_OPERATIONS = int(2e6)

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
    dist = {}
    for index1, x1, y1 in points:
        for index2, x2, y2 in points:
            if index1 != index2:
                dist[(index1, index2)] = eucledian_distance(x1, y1, x2, y2)
    return dist

def tsp_backtrack(current_city, visited, current_dist, n, dist, best):
    global counter
    counter += 1
    if counter > MAX_OPERATIONS:
        return
    if len(visited) == n:
        return_to_start = dist[(current_city, 1)]
        total_dist = current_dist + return_to_start
        if total_dist < best[0]:
            best[0] = total_dist
            best[1] = visited[:]
        return
    for next_city in range(1, n + 1):
        if next_city not in visited:
            new_dist = current_dist + dist[(current_city, next_city)]
            if new_dist < best[0]:
                visited.append(next_city)
                tsp_backtrack(next_city, visited, new_dist, n, dist, best)
                visited.pop()

def main():
    global counter
    filename = "berlin52.tsp"
    points = read_points(filename)
    dist = compute_all_distances(points)
    n = len(points)
    best = [1e10, []]
    visited = [1]
    tsp_backtrack(1, visited, 0, n, dist, best)

    print("Best distance found:", best[0])
    print("Best path found:", best[1])

main()

"""
The result of bruteforce:

Best distance found: 19367.280560788986
Best path (partial if stopped): [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 45, 42, 50, 47, 52, 51, 43, 48, 46, 44, 49] 
"""