from domain.puzzle import Puzzle
from domain.validator import PuzzleValidator
from repository.puzzle_repository import PuzzleRepository
from service.puzzle_service import PuzzleService
from utils import Utils
from ui.console import Console
import tests.tests as tests


def main():
  filename = "puzzles.txt"
  puzzle_repository = PuzzleRepository(filename)
  puzzle_validator = PuzzleValidator
  utils = Utils()
  puzzle_service = PuzzleService(puzzle_repository, puzzle_validator, utils)
  console = Console(puzzle_service)
  tests.test_all()

  console.run()

if __name__ == "__main__":
  main()
