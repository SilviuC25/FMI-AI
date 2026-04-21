# P3. The elements of the sublist all have the same parity (i.e. all are even or all are odd).

def most_frequent_parity(numbers):
    odd_count = 0
    even_count = 0

    for number in numbers:
        if number % 2 == 0:
            even_count += 1
        else:
            odd_count += 1

    parity = 1 if odd_count > even_count else 0 # 1 if odd numbers appear more often and 0 otherwise
    return parity

def get_longest_sublist_same_parity(numbers):
    sublist = []
    parity = most_frequent_parity(numbers)

    for number in numbers:

        if number % 2 == parity:
            sublist.append(number)

    return sublist
