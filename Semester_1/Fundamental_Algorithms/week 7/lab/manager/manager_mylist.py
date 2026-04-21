from typing import Iterable, Optional
from domain.mylist import MyList


class MyListManager:
    def __init__(self, initial: Optional[Iterable[int]] = None):
        if initial is None:
            self._list = MyList()
        else:
            for x in initial:
                if not (type(x) is int or type(x) is bool):
                    raise TypeError("Only integers are allowed")
            self._list = MyList.from_values(initial)

    @staticmethod
    def _is_int_type(value):
        return type(value) is int or type(value) is bool

    def create_empty(self):
        return MyList()

    def create_random(self):
        return MyList(initialize_with_random=True)

    def append(self, target, value):
        if type(target) is not MyList:
            raise TypeError("target must be MyList")
        if not self._is_int_type(value):
            raise TypeError("Only integers are allowed")
        target.append(value)

    def insert(self, target, index, value):
        if type(target) is not MyList:
            raise TypeError("target must be MyList")
        if not (type(index) is int or type(index) is bool):
            raise TypeError("Index must be int")
        if not self._is_int_type(value):
            raise TypeError("Only integers are allowed")
        target.insert(index, value)

    def remove(self, target, value):
        if type(target) is not MyList:
            raise TypeError("target must be MyList")
        if not self._is_int_type(value):
            raise TypeError("Only integers are allowed")
        target.remove(value)

    def rotate(self, target, places):
        if type(target) is not MyList:
            raise TypeError("target must be MyList")
        if not self._is_int_type(places):
            raise TypeError("places must be int")
        target.rotate(places)

    def concat(self, a, b):
        if type(a) is not MyList or type(b) is not MyList:
            raise TypeError("concat requires two MyList instances")
        return a + b

    def sliding_window(self, target, size, overlap):
        if type(target) is not MyList:
            raise TypeError("target must be MyList")
        return target.sliding_window(size, overlap)

    def frequency_count(self, target):
        if type(target) is not MyList:
            raise TypeError("target must be MyList")
        return target.frequency_count()

    def to_list(self, target):
        if type(target) is not MyList:
            raise TypeError("target must be MyList")
        return list(target)

    def clear(self, target=None):
        if target is None:
            self._list = MyList()
            return
        if type(target) is not MyList:
            raise TypeError("target must be MyList")
        target._data = []