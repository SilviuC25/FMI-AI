import unittest
from copy import deepcopy
from typing import Callable, Any, List, Dict

from utils.sorting import bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort, heap_sort


ALL_ALGS: Dict[str, Callable[..., List[Any]]] = {
    "bubble": bubble_sort,
    "selection": selection_sort,
    "insertion": insertion_sort,
    "merge": merge_sort,
    "quick": quick_sort,
    "heap": heap_sort,
}


class TestSortingAlgorithms(unittest.TestCase):
    def setUp(self) -> None:
        self.simple = [5, 3, 1, 2, 4]
        self.duplicates = [3, 1, 2, 3, 2, 1, 3]
        self.empty: List[int] = []
        self.single = [42]

    def test_basic_sorting_matches_python_sorted(self):
        for name, func in ALL_ALGS.items():
            with self.subTest(algo=name):
                src = self.simple.copy()
                res = func(src)
                self.assertEqual(res, sorted(src))

    def test_key_function(self):
        data = [(0, 3), (1, 1), (2, 2), (3, 0)]
        for name, func in ALL_ALGS.items():
            with self.subTest(algo=name):
                src = data.copy()
                res = func(src, key=lambda x: x[1])
                expected = sorted(data, key=lambda x: x[1])
                self.assertEqual(res, expected)

    def test_handles_empty_and_single(self):
        for name, func in ALL_ALGS.items():
            with self.subTest(algo=name):
                self.assertEqual(func(self.empty), [])
                self.assertEqual(func(self.single), [42])

    def test_non_mutating(self):
        for name, func in ALL_ALGS.items():
            with self.subTest(algo=name):
                src = [4, 2, 5, 1]
                original = deepcopy(src)
                _ = func(src)
                self.assertEqual(src, original)

    def test_duplicates_sorted_correctly(self):
        for name, func in ALL_ALGS.items():
            with self.subTest(algo=name):
                src = self.duplicates.copy()
                res = func(src)
                self.assertEqual(res, sorted(src))

    def test_works_with_negative_numbers(self):
        src = [0, -10, 5, -3, 2]
        for name, func in ALL_ALGS.items():
            with self.subTest(algo=name):
                self.assertEqual(func(src), sorted(src))

    def test_works_with_already_sorted(self):
        src = [1, 2, 3, 4, 5]
        for name, func in ALL_ALGS.items():
            with self.subTest(algo=name):
                self.assertEqual(func(src), src)

    def test_works_with_reverse_sorted(self):
        src = [5, 4, 3, 2, 1]
        for name, func in ALL_ALGS.items():
            with self.subTest(algo=name):
                self.assertEqual(func(src), sorted(src))


def run_all_sorting_tests(verbosity: int = 2) -> bool:
    """
    Runs all sorting tests and returns True if all passed, otherwise False.
    """
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestSortingAlgorithms)
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    ok = run_all_sorting_tests()
    raise SystemExit(0 if ok else 1)
