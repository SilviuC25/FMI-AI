import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from domain.mylist import MyList


def test_append_and_str_and_len():
    lst = MyList()
    assert len(lst) == 0, "a new list should be empty"
    lst.append(10)
    assert str(lst) == "10", f"after append(10) expected str(lst) '10', got '{str(lst)}'"
    lst.append(20)
    assert str(lst) == "10, 20", f"after append(20) expected str(lst) '10, 20', got '{str(lst)}'"
    assert len(lst) == 2, "length should be 2"


def test_type_checks():
    lst = MyList()
    try:
        lst.append("a")
    except TypeError:
        pass
    else:
        assert False, "append with string should have raised TypeError"

    lst.append(1)
    try:
        lst[0] = 3.14
    except TypeError:
        pass
    else:
        assert False, "assignment with float should have raised TypeError"


def test_insert_and_index_and_contains_and_remove():
    lst = MyList()
    lst.append(10)
    lst.append(20)
    lst.insert(1, 15)
    assert lst[1] == 15, "insert did not place the value at index 1"
    assert 15 in lst, "membership test did not find 15"
    assert lst.index(15) == 1, "index(15) should return 1"
    lst.remove(15)
    assert not (15 in lst), "remove did not remove 15"


def test_slicing_and_iteration_and_concat():
    lst = MyList.from_values([1, 2, 3, 4])
    sl = lst[1:3]
    assert type(sl).__name__ == "MyList", "slice should return a MyList"
    assert str(sl) == "2, 3", f"incorrect slice: expected '2, 3', got '{str(sl)}'"
    out = [x for x in lst]
    assert out == [1, 2, 3, 4], f"iteration should produce [1,2,3,4], got {out}"
    lst2 = MyList.from_values([5, 6])
    cat = lst + lst2
    assert type(cat).__name__ == "MyList", "concatenation should return MyList"
    assert str(cat) == "1, 2, 3, 4, 5, 6", f"incorrect concat, got '{str(cat)}'"


def test_rotate_and_rotate_sublist():
    lst = MyList.from_values([10, 20, 30, 40])
    lst.rotate(1)
    assert str(lst) == "40, 10, 20, 30", f"rotate(1) incorrect: {str(lst)}"
    lst.rotate_sublist(1, 3, 1)
    assert str(lst) == "40, 30, 10, 20", f"rotate_sublist incorrect: {str(lst)}"


def test_sliding_window_and_frequency():
    lst = MyList.from_values([1, 2, 3, 4, 5])
    windows = lst.sliding_window(3, 2) 
    got = [str(w) for w in windows]
    expected = ["1, 2, 3", "2, 3, 4", "3, 4, 5"]
    assert got == expected, f"sliding_window(3,2) incorrect: {got}"
    freq = lst.frequency_count()
    assert freq == {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, f"frequency_count incorrect: {freq}"


def test_index_valueerror():
    lst = MyList.from_values([5, 6, 7])
    try:
        lst.index(100)
    except ValueError:
        pass
    else:
        assert False, "index for a nonexistent value should have raised ValueError"

def test_eq_concatenation():
    a = MyList.from_values([1, 23, 4])
    b = MyList.from_values([12, 34])
    c = MyList.from_values([1, 23, 4])
    d = MyList.from_values([1, 2, 3, 4])
    assert a == c, "Lists with same concatenated elements should be equal"
    assert not (a == b), "Lists with different concatenated elements should not be equal"
    assert a != d, "Lists with different concatenated elements should not be equal"

def run_all():
    tests = [
        test_append_and_str_and_len,
        test_type_checks,
        test_insert_and_index_and_contains_and_remove,
        test_slicing_and_iteration_and_concat,
        test_rotate_and_rotate_sublist,
        test_sliding_window_and_frequency,
        test_index_valueerror,
        test_eq_concatenation
    ]
    total = len(tests)
    passed = 0
    for t in tests:
        name = t.__name__
        try:
            t()
            print(f"[OK] {name}")
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {name}: {e}")
        except Exception as e:
            print(f"[ERROR] {name}: {type(e).__name__}: {e}")
    print(f"\nResult: {passed}/{total} tests passed")
    if passed != total:
        raise SystemExit(1)


if __name__ == "__main__":
    run_all()
