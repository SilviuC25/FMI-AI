from domain.puzzle import Puzzle
from domain.validator import PuzzleValidator
from repository.puzzle_repository import PuzzleRepository
from service.puzzle_service import PuzzleService

class Console:
  def __init__(self, puzzle_service: PuzzleService):
    self.__puzzle_service = puzzle_service

  def print_menu():
    """
    Prints the available commands for the user
    """
    print("ADD. Add a new puzzle to the list")
    print("PIECES. Display all the puzzles with the number of pieces in a given interval sorted by price")
    print("CATEGORIES. Display the total number of puzzles in categories")
    print("STOP. Ends the process")

  def handle_add(self):
    """
    Prints the result of the 'ADD' feature.
    """
    id = int(input("Puzzle ID: "))
    description = input("Description: ")
    number_of_pieces = int(input("Pieces: "))
    price = float(input("Price: "))

    try:
      puzzle = Puzzle(id, description, number_of_pieces, price)
      self.__puzzle_service.add_puzzle(puzzle)
      print(f"Puzzle with {id} added successfully")
    except ValueError as err:
      print(err)

  def handle_pieces(self):
    """
    Prints the result of the 'PIECES' feature.
    """
    min_pieces = int(input("Minimum pieces: "))
    max_prices = int(input("Maximum pieces: "))

    puzzles_to_display = self.__puzzle_service.display_by_number_of_pieces(min_pieces, max_prices)

    if not puzzles_to_display:
      print("No puzzles to display for given data")
    else:
      for puzzle in puzzles_to_display:
        print(puzzle)

  def handle_categories(self):
    """
    Prints the result of the 'CATEGORIES' feature.
    """
    print(self.__puzzle_service.display_count_of_categories())

  
  def run(self):
    """
    Runs the console until with available commands until user stops it.
    """
    while True:
      Console.print_menu()
      option = input("Choose an option: ").upper()

      match option:
        case "ADD":
          self.handle_add()
        case "PIECES":
          self.handle_pieces()
        case "CATEGORIES":
          self.handle_categories()
        case "STOP":
          break