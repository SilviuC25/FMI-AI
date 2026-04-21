from domain.mylist import MyList

def main():
    # Create a new empty MyList
    lst = MyList()  # the list is empty
    print("lst (empty):", repr(lst))  # shows MyList([]) using __repr__

    # Create a new MyList with generated numbers
    lst_r = MyList(initialize_with_random=True)
    print(f"random list (n={len(lst_r)}):", lst_r)

    # Add elements to the end of the list
    lst.append(10)  # 10 is added to the list
    print("after append(10):", lst)  # "10"
    lst.append(20)  # 20 is added to the list
    print("after append(20):", lst)  # "10, 20"

    # Type error examples
    try:
        lst.append("hello")  # Cannot add something other than integer
    except TypeError as e:
        print("append error:", e)

    try:
        lst[0] = 3.14  # Cannot assign something other than integer
    except TypeError as e:
        print("assignment error:", e)

    # Add element at a specific position
    lst.insert(1, 15)  # 15 inserted at index 1, content is now: 10, 15, 20
    print("after insert(1, 15):", lst)

    # Access elements by index
    print("lst[0] =", lst[0])  # 10
    print("lst[1] =", lst[1])  # 15
    print("lst[2] =", lst[2])  # 20

    lst.rotate(1)
    print("after rotate(1):", lst)
    print("frequency_count:", lst.frequency_count())

    windows = lst.sliding_window(2, 1)
    print("sliding windows (size=2, overlap=1):", [str(w) for w in windows])

if __name__ == "__main__":
    main()