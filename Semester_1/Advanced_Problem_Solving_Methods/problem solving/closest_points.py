import math

def read_points(filename):
  file = open(filename, "r")
  points = []

  for line in file:
    x, y = map(int, line.split())
    points.append((x, y))

  return points

def dist(x1, y1, x2, y2):
  return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def bruteforce(points):
  n = len(points)
  min_dist = x1 = x2 = y1 = y2 = 1e10
  for i in range (n):
    for j in range(n):
      if i != j:
        current_dist = dist(points[i][0], points[i][1], points[j][0], points[j][1])
        if current_dist < min_dist:
          min_dist = current_dist
          x1 = points[i][0]
          y1 = points[i][1]
          x2 = points[j][0]
          y2 = points[j][1]

  print(x1, y1, x2, y2, min_dist)


def divide_and_conquer(points):
    n = len(points)
    mid = n // 2
    mid_x = points[mid][0]

    left_points = points[:mid]
    right_points = points[mid:]

    d_left, pair_left = divide_and_conquer(left_points)
    d_right, pair_right = divide_and_conquer(right_points)

    if d_left < d_right:
        d = d_left
        best_pair = pair_left
    else:
        d = d_right
        best_pair = pair_right

    strip = []
    for p in points:
        if abs(p[0] - mid_x) < d:
            strip.append(p)

    strip.sort(key=lambda p: p[1])

    m = len(strip)
    for i in range(m):
        for j in range(i + 1, min(i + 7, m)):
            d_curr = dist(strip[i][0], strip[i][1],
                          strip[j][0], strip[j][1])
            if d_curr < d:
                d = d_curr
                best_pair = (strip[i], strip[j])

    return d, best_pair

def main():
  filename = "points.txt"
  points = read_points(filename)
  points.sort()
  divide_and_conquer(points)

main()