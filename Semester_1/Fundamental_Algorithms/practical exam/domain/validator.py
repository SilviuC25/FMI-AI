from domain.puzzle import Puzzle

class PuzzleValidator:
  def validate_puzzle(puzzle: Puzzle):
    """
    Validates the given Puzzle object

    Args:
      puzzle: Puzzle
    Returns:
      ValueError if number of pieces is not in [500, 768, 1000, 2000] or the given price is negative
    """
    number_of_pieces = puzzle.get_number_of_pieces()

    if number_of_pieces not in [500, 768, 1000, 2000]:
      raise ValueError("Number of pieces must be one of: 500, 768, 1000, 2000.")
    
    price = puzzle.get_price()

    if price < 0:
      raise ValueError("The price must be a positive number.")
    