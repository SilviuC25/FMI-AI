from domain.puzzle import Puzzle
from domain.validator import PuzzleValidator
from repository.puzzle_repository import PuzzleRepository
from utils import Utils

class PuzzleService:
  def __init__(self, puzzle_repository: PuzzleRepository, puzzle_validator: PuzzleValidator, utils: Utils):
    self.__puzzle_repository = puzzle_repository
    self.__puzzle_validator = puzzle_validator
    self.__utils = utils


  def add_puzzle(self, puzzle: Puzzle):
    """
    Validates a puzzle and append it to the list
    
    Args:
      puzzle: Puzzle
    Raises: 
      ValueError from validator if data is not valid
    """
    self.__puzzle_validator.validate_puzzle(puzzle)
    self.__puzzle_repository.add_puzzle(puzzle)

  def display_by_number_of_pieces(self, min_pieces: int, max_pieces: int):
    """
    Args:
      min_pieces: int,
      max_pieces: int

    Returns:
      puzzles_to_display: list - containing all the puzzles in the given number_of_pieces interval, sorted by price
    """
    puzzles_to_display = []

    for puzzle in self.__puzzle_repository.get_all_puzzles():
      number_of_pieces = int(puzzle.get_number_of_pieces())

      if number_of_pieces >= min_pieces and number_of_pieces <= max_pieces:
        puzzles_to_display.append(puzzle)

    puzzles_to_display = self.__utils.sort_by_price(puzzles_to_display)

    return puzzles_to_display
  
  def display_count_of_categories(self):
    """
    Returns:
      str: containing the count of both categories
    """
    landscape_count = 0
    art_count = 0

    for puzzle in self.__puzzle_repository.get_all_puzzles():
      description = str(puzzle.get_description()).lower()

      found = False

      for word in ["mountain", "lake", "flower"]:
        if word in description and not found:
          landscape_count = landscape_count + 1
          found = True

      pattern = "[art collection]"
      length = len(pattern)
      if description[:length] == pattern:
        art_count = art_count + 1

    return f"Landscape puzzles: {landscape_count}\nArt puzzles: {art_count}"


  