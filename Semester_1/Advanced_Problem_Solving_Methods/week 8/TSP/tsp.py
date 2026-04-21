import random

file = open("berlin52.tsp")

locations = {}


def read_lines():
  for line in file:
    [index, x, y] = line.split()
    index = int(index)
    locations[index] = (float(x), float(y))

read_lines()
location_dist = {}

def calculate_distances():
  for i in range(1, 53):
    for j in range(1, 53):
      if i != j:
        xi, yi = locations[i]
        xj, yj = locations[j]
        dist = ((xi - xj) ** 2 + (yi - yj) ** 2) ** 0.5
        location_dist[i, j] = dist

calculate_distances()

def total_cost(tour):
  cost = 0
  for i in range(len(tour)):
    j = (i + 1) % len(tour)
    cost += location_dist[tour[i], tour[j]]
  return cost

def tsp():
  current_tour = list(locations.keys())
  random.shuffle(current_tour)
  current_cost = total_cost(current_tour)

  min_cost = current_cost
  best_tour = current_tour.copy()

  print("Initial cost:", current_cost)
  print("Initial tour:", current_tour)

  for _ in range(1000):
    for i in range(0, 52):
      for j in range(0, 52):
        if (i != j):
          temp = current_tour[i]
          current_tour[i] = current_tour[j]
          current_tour[j] = temp
          
          current_cost = total_cost(current_tour)

          if (current_cost < min_cost):
            min_cost = current_cost
            best_tour = current_tour.copy()
  
  print("Best cost:", min_cost)
  print("Best tour:", best_tour)

tsp()
