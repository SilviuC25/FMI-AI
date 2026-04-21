import random

class MyList:
    def __init__(self, initialize_with_random=False):
        self.__data = []
        if initialize_with_random:
            n = random.randint(1, 10)
            self.__data = [random.randint(10, 50) for _ in range(n)]

    @property
    def data(self):
        return self.__data.copy()

    def __len__(self):
        return len(self.__data)

    def __iter__(self):
        return iter(self.__data)

    def __getitem__(self, key):
        if type(key) is slice:
            new_list = MyList()
            new_list.__data = self.__data[key]
            return new_list
        if type(key) is not int and type(key) is not bool:
            raise TypeError("Index must be int or slice")
        return self.__data[key]

    def __setitem__(self, key, value):
        if type(key) is not int and type(key) is not bool:
            raise TypeError("Index must be int")
        if type(value) is not int and type(value) is not bool:
            raise TypeError("Only integers are allowed")
        self.__data[key] = value

    def __delitem__(self, key):
        if type(key) is not int and type(key) is not bool:
            raise TypeError("Index must be int")
        del self.__data[key]

    def append(self, value):
        if type(value) is not int and type(value) is not bool:
            raise TypeError("Only integers are allowed")
        self.__data.append(value)

    def insert(self, index, value):
        if type(value) is not int and type(value) is not bool:
            raise TypeError("Only integers are allowed")
        if type(index) is not int and type(index) is not bool:
            raise TypeError("Index must be int")
        if index >= len(self.__data):
            self.__data.append(value)
        else:
            self.__data.insert(index, value)

    def remove(self, value):
        if type(value) is not int and type(value) is not bool:
            raise TypeError("Only integers are allowed")
        self.__data.remove(value)

    def __contains__(self, value):
        return value in self.__data

    def index(self, value, start=0, end=None):
        if type(value) is not int and type(value) is not bool:
            raise TypeError("Only integers are allowed")
        if end is None:
            end = len(self.__data) - 1
        if type(start) is not int and type(start) is not bool:
            raise TypeError("start must be int")
        if type(end) is not int and type(end) is not bool:
            raise TypeError("end must be int")
        if start < 0:
            start = 0
        if end >= len(self.__data):
            end = len(self.__data) - 1
        for i in range(start, end + 1):
            if self.__data[i] == value:
                return i
        raise ValueError(f"{value} is not in list")

    def __str__(self):
        return ", ".join(str(x) for x in self.__data)

    def __repr__(self):
        return f"MyList([{', '.join(str(x) for x in self.__data)}])"

    def __add__(self, other):
        if type(other) is not MyList:
            raise TypeError(f"Can only concatenate MyList (not '{type(other).__name__}')")
        new_list = MyList()
        new_list.__data = self.__data + other.__data
        return new_list

    def rotate(self, places):
        if type(places) is not int and type(places) is not bool:
            raise TypeError("places must be int")
        n = len(self.__data)
        if n == 0:
            return
        k = places % n
        if k:
            self.__data = self.__data[-k:] + self.__data[:-k]

    def rotate_sublist(self, start, end, places):
        if type(start) is not int and type(start) is not bool:
            raise TypeError("start must be int")
        if type(end) is not int and type(end) is not bool:
            raise TypeError("end must be int")
        if type(places) is not int and type(places) is not bool:
            raise TypeError("places must be int")
        n = len(self.__data)
        if n == 0:
            return
        start = max(0, start)
        end = min(end, n - 1)
        if start > end:
            raise ValueError("start must be <= end")
        sub = self.__data[start:end + 1]
        m = len(sub)
        k = places % m
        if k:
            rotated = sub[-k:] + sub[:-k]
            self.__data[start:end + 1] = rotated

    def sliding_window(self, size, overlap):
        if type(size) is not int and type(size) is not bool:
            raise TypeError("size must be int")
        if type(overlap) is not int and type(overlap) is not bool:
            raise TypeError("overlap must be int")
        if size <= 0:
            raise ValueError("size must be positive")
        if overlap < 0:
            raise ValueError("overlap cannot be negative")
        step = size - overlap
        if step <= 0:
            raise ValueError("overlap must be less than size")

        n = len(self.__data)
        result = []
        i = 0

        while i + size <= n:
            window = self.__data[i:i + size]
            w = MyList()
            w.__data = window
            result.append(w)
            i += step

        if i < n:
            if not result:
                window = self.__data[i:i + size]
                w = MyList()
                w.__data = window
                result.append(w)
            else:
                prev_start = i - step
                last_full_end = prev_start + size
                if last_full_end < n:
                    window = self.__data[i:i + size]
                    w = MyList()
                    w.__data = window
                    result.append(w)

        return result

    def frequency_count(self):
        freq = {}
        for v in self.__data:
            freq[v] = freq.get(v, 0) + 1
        return freq

    @classmethod
    def from_values(cls, iterable):
        m = cls()
        for x in iterable:
            if type(x) is not int and type(x) is not bool:
                raise TypeError("Only integers are allowed")
        m.__data = list(iterable)
        return m

    def __eq__(self, other):
        if type(other) is not MyList:
            return False
        return self.__data == other.__data