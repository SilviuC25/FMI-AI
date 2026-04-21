from domain.puzzle import Puzzle

class PuzzleRepository:
  def __init__(self, filename: str):
    self.__filename = filename
    self.__puzzles = []
    self.__load_from_file()

  def add_puzzle(self, puzzle: Puzzle):
    """
    Adds a Puzzle to the list of all puzzles

    Args:
      puzzle: Puzzle
    Return:
      ValueError if given ID is already in the list of all puzzles, otherwise:
      Appends the puzzle to the list and saves it to the file
    """

    id = puzzle.get_id()

    if not self.is_unique_id(id):
      raise ValueError(f"A puzzle with ID {id} already exists.")

    self.__puzzles.append(puzzle)
    self.__save_to_file()

  def get_all_puzzles(self):
    """
    Args:
      -  
    Returns:
      self.__puzzles: list of Puzzle
      The list of all saved puzzles
    """
    return self.__puzzles
  
  def is_unique_id(self, id: int):
    """
    Args:
      id: int
    Returns:
      boolean: True if id is unique in self.__puzzles, False otherwise
    """
    for puzzle in self.__puzzles:
      if puzzle.get_id() == id:
        return False
    
    return True

  def __load_from_file(self):
    """
    Loads the given data from the text file to the list of all puzzles
    """
    with open(self.__filename, "r") as file:
      for line in file:
        line = line.strip()
        parts = line.split("; ")
        id = int(parts[0])
        description = parts[1]
        number_of_pieces = parts[2]
        price = float(parts[3])

        puzzle = Puzzle(id, description, number_of_pieces, price)
        self.__puzzles.append(puzzle)

  def __save_to_file(self):
    """
    Saves the puzzles added to the list in the text file
    """
    with open(self.__filename, "w") as file:
      for puzzle in self.__puzzles:
        id = puzzle.get_id()
        description = puzzle.get_description()
        number_of_pieces = puzzle.get_number_of_pieces()
        price = puzzle.get_price()

        line = (
          f"{id}; "
          f"{description}; "
          f"{number_of_pieces}; "
          f"{price}\n"
        )

        file.write(line)


  
