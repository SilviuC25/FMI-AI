from domain.puzzle import Puzzle
from domain.validator import PuzzleValidator
from repository.puzzle_repository import PuzzleRepository
from service.puzzle_service import PuzzleService
from utils import Utils
from ui.console import Console


def test_domain():
  puzzle = Puzzle(101, "Mountain Sunrise", 1000, 24.99)

  assert puzzle.get_id() == 101
  assert puzzle.get_description() == "Mountain Sunrise"

  puzzle.set_price(20)
  assert puzzle.get_price() == 20


def test_repository():
  puzzle1 = Puzzle(101, "Mountain Sunrise", 1000, 24.99)
  puzzle2 = Puzzle(205, "[art collection] Starry Night", 500, 19.5)
  puzzle3 = Puzzle(312, "Lake at Dawn", 768, 34.00)

  repo = PuzzleRepository("test.txt")
  assert len(repo.get_all_puzzles()) == 2

  repo.add_puzzle(puzzle1)
  repo.add_puzzle(puzzle2)
  repo.add_puzzle(puzzle3)

  assert len(repo.get_all_puzzles()) == 5

def test_service():
  puzzle1 = Puzzle(101, "Mountain Sunrise", 1000, 24.99)
  puzzle2 = Puzzle(205, "[art collection] Starry Night", 500, 19.5)
  puzzle3 = Puzzle(312, "Lake at Dawn", 768, 34.00)

  repo = PuzzleRepository("test.txt")
  validator = PuzzleValidator()
  utils = Utils()
  service = PuzzleService()

  assert len(repo.get_all_puzzles()) == 2

  service.add_puzzle(puzzle1)
  service.add_puzzle(puzzle2)
  service.add_puzzle(puzzle3)

  assert len(repo.get_all_puzzles()) == 5


  display_list = service.display_by_number_of_pieces(0, 2000)

  first_puzzle = display_list[0]
  assert first_puzzle.get_id() == 518

  last_puzzle = display_list[-1]
  assert last_puzzle.get_id() == 606

def test_all():
  test_domain()
  print("All tests passed!")