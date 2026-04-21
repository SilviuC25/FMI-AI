import math
import random

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

def tour_length(tour, dist):
    total = 0
    for i in range(len(tour) - 1):
        total += dist[tour[i]][tour[i + 1]]
    total += dist[tour[-1]][tour[0]]
    return total

def random_tour(n):
    tour = list(range(1, n + 1))
    random.shuffle(tour)
    return tour

def order_crossover(p1, p2):
    n = len(p1)
    a = random.randint(0, n - 2)
    b = random.randint(a + 1, n - 1)

    child = [-1] * n
    child[a:b] = p1[a:b]

    pos = b
    for city in p2:
        if city not in child:
            if pos == n:
                pos = 0
            child[pos] = city
            pos += 1

    return child

def mutate(tour):
    i = random.randint(0, len(tour) - 1)
    j = random.randint(0, len(tour) - 1)
    tour[i], tour[j] = tour[j], tour[i]

def genetic_tsp(dist, n):
    POP_SIZE = 100
    GENERATIONS = 300
    MUTATION_RATE = 0.2

    population = []
    for _ in range(POP_SIZE):
        population.append(random_tour(n))

    best_tour = population[0]
    best_length = tour_length(best_tour, dist)

    for _ in range(GENERATIONS):
        population.sort(key=lambda t: tour_length(t, dist))
        population = population[:POP_SIZE // 2]

        if tour_length(population[0], dist) < best_length:
            best_tour = population[0]
            best_length = tour_length(best_tour, dist)

        new_population = population[:]

        while len(new_population) < POP_SIZE:
            p1 = random.choice(population)
            p2 = random.choice(population)
            child = order_crossover(p1, p2)

            if random.random() < MUTATION_RATE:
                mutate(child)

            new_population.append(child)

        population = new_population

    return best_tour, best_length

def main():
    filename = "berlin52.tsp"
    points = read_points(filename)
    dist = compute_all_distances(points)
    n = len(points)

    tour, length = genetic_tsp(dist, n)

    tour.append(tour[0])
    print("The total distance is", length)
    print("The result list is", tour)

main()
"""
The result of Genetic Algo:
The total distance is 9726.896628200273
The result list is [50, 29, 20, 23, 30, 7, 42, 2, 21, 17, 18, 22, 1, 49, 32, 31, 3, 19, 45, 41, 8, 10, 9, 44, 34, 40, 39, 37, 46, 48, 6, 4, 25, 12, 11, 27, 28, 26, 47, 13, 14, 52, 51, 33, 43, 15, 5, 24, 38, 36, 35, 16, 50]
"""