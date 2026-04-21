from domain.puzzle import Puzzle

class Utils:
  def sort_by_price(self, puzzles: list):
    """
    Args:
      puzzles: list
    Returns:
      puzzles: list
      The list of puzzles after sorted using Buuble Sort
      It sorts the list of Puzzle in ascending order by their price
    """
    length = len(puzzles)

    for it in range(length):
      for index in range(length - 1):
        first_price = puzzles[index].get_price()
        second_price = puzzles[index + 1].get_price()

        if (first_price > second_price):
          temp = puzzles[index]
          puzzles[index] = puzzles[index + 1]
          puzzles[index + 1] = temp

    return puzzles
