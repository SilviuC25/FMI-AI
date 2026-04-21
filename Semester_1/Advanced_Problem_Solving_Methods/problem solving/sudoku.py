def read_grid_from_file(filename):
    grid = []
    file = open(filename, "r")

    for _ in range (9):
      line = file.readline()
      line = line.strip().split()
      line = [int(num) for num in line]
      grid.append(line)

    return grid

def print_grid(grid):
  for row in range(9):
    for col in range(9):
      if col == 0:
        print("|", end=" ")
      print(grid[row][col], end=" ")
      if (col + 1) % 3 == 0:
        print("|", end=" ")
      if col == 8:
        print()
        print("_" * 25)
        print()

def check(grid, row, col, num):
  for c in range(9):
      if grid[row][c] == num:
          return False

  for r in range(9):
      if grid[r][col] == num:
          return False

  start_row = 3 * (row // 3)
  start_col = 3 * (col // 3)
  for r in range(start_row, start_row + 3):
      for c in range(start_col, start_col + 3):
          if grid[r][c] == num:
              return False

  return True

def solve(grid):
  for row in range(9):
     for col in range(9):
        if grid[row][col] == 0:
            for num in range (1, 10):
              if check(grid, row, col, num):
                grid[row][col] = num
                if solve(grid):
                  return True
                grid[row][col] = 0
            return False
  return True

def main():
  filename = "sudoku_input.txt"
  grid = read_grid_from_file(filename)
  solve(grid)
  print_grid(grid)

main()
         
