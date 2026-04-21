import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from manager.manager_mylist import MyListManager
from domain.mylist import MyList

def test_manager():
    m = MyListManager()
    a = m.create_empty()
    assert type(a).__name__ == "MyList", "create_empty should return MyList"
    b = m.create_random()
    assert type(b).__name__ == "MyList", "create_random should return MyList"

    m.append(a, 10)
    assert str(a) == "10", f"append failed: {str(a)}"
    m.insert(a, 0, 5)
    assert str(a) == "5, 10", f"insert failed: {str(a)}"
    m.rotate(a, 1)
    assert str(a) == "10, 5", f"rotate failed: {str(a)}"

    c = m.concat(a, b)
    assert type(c).__name__ == "MyList", "concat should return MyList"
    assert len(c) == len(a) + len(b), "concat resulted in a list with incorrect length"


def run_all():
    tests = [test_manager]
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
