from typing import List, TypeVar, Callable, Any

T = TypeVar("T")

def bubble_sort(items: List[T], key: Callable[[T], Any] = lambda x: x, reverse: bool = False) -> List[T]:
    """Simple bubble sort. Complexity: best O(n), average/worst O(n^2)."""
    res = items.copy()
    n = len(res)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            a, b = key(res[j]), key(res[j + 1])
            if (a > b) ^ reverse:
                res[j], res[j + 1] = res[j + 1], res[j]
                swapped = True
        if not swapped:
            break
    return res


def selection_sort(items: List[T], key: Callable[[T], Any] = lambda x: x, reverse: bool = False) -> List[T]:
    """Selection sort. Complexity: O(n^2) always."""
    res = items.copy()
    n = len(res)
    for i in range(n):
        idx = i
        for j in range(i + 1, n):
            if (key(res[j]) < key(res[idx])) ^ reverse:
                idx = j
        res[i], res[idx] = res[idx], res[i]
    return res


def insertion_sort(items: List[T], key: Callable[[T], Any] = lambda x: x, reverse: bool = False) -> List[T]:
    """Insertion sort. Complexity: best O(n), average/worst O(n^2)."""
    res = items.copy()
    for i in range(1, len(res)):
        cur = res[i]
        curk = key(cur)
        j = i - 1
        while j >= 0 and ((key(res[j]) > curk) ^ reverse):
            res[j + 1] = res[j]
            j -= 1
        res[j + 1] = cur
    return res


def merge_sort(items: List[T], key: Callable[[T], Any] = lambda x: x, reverse: bool = False) -> List[T]:
    """Merge sort. Complexity: O(n log n) all cases. Stable."""
    if len(items) <= 1:
        return items.copy()

    def merge(a: List[T], b: List[T]) -> List[T]:
        i = j = 0
        out: List[T] = []
        while i < len(a) and j < len(b):
            if (key(a[i]) <= key(b[j])) ^ reverse:
                out.append(a[i]); i += 1
            else:
                out.append(b[j]); j += 1
        out.extend(a[i:]); out.extend(b[j:])
        return out

    mid = len(items) // 2
    left = merge_sort(items[:mid], key=key, reverse=reverse)
    right = merge_sort(items[mid:], key=key, reverse=reverse)
    return merge(left, right)


def quick_sort(items: List[T], key: Callable[[T], Any] = lambda x: x, reverse: bool = False) -> List[T]:
    """Quick sort. Complexity: average O(n log n), worst O(n^2)."""
    res = items.copy()

    def _qs(lo: int, hi: int) -> None:
        if lo >= hi:
            return
        pivot = key(res[(lo + hi) // 2])
        i, j = lo, hi
        while i <= j:
            while i <= j and ((key(res[i]) < pivot) ^ reverse):
                i += 1
            while i <= j and ((key(res[j]) > pivot) ^ reverse):
                j -= 1
            if i <= j:
                res[i], res[j] = res[j], res[i]
                i += 1; j -= 1
        if lo < j:
            _qs(lo, j)
        if i < hi:
            _qs(i, hi)

    _qs(0, len(res) - 1)
    return res


def heap_sort(items: List[T], key: Callable[[T], Any] = lambda x: x, reverse: bool = False) -> List[T]:
    """Heap sort. Complexity: O(n log n) all cases."""
    res = items.copy()
    n = len(res)

    def heapify(sz: int, i: int) -> None:
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < sz and ((key(res[l]) > key(res[largest])) ^ reverse):
            largest = l
        if r < sz and ((key(res[r]) > key(res[largest])) ^ reverse):
            largest = r
        if largest != i:
            res[i], res[largest] = res[largest], res[i]
            heapify(sz, largest)

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        res[0], res[i] = res[i], res[0]
        heapify(i, 0)
    return res
