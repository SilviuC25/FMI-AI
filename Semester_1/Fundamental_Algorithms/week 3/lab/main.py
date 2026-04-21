# P3, R5 and (1)

from property_p import get_longest_sublist_same_parity
from property_r import remove_repeating_digit_numbers
import random

def read_numbers():
    numbers = list(map(int, input("Enter numbers: ").split()))
    print("The current list is:", numbers)
    return numbers

def generate_random_items():
    no_numbers = int(input("Enter the length of random list: "))
    left = int(input("Enter the left boundary of range: "))
    right = int(input("Enter the right boundary of range: "))
    random_list = []
    
    for _ in range(0, no_numbers):
        new_num = random.randint(left, right)
        random_list.append(new_num)
    
    print("The random list is:", random_list)



def print_menu():
    print("\n1. Read a list of integer numbers")
    print("2. Find sublist with maximum length that has property P3 (same parity).")
    print("3. Remove elements with property R5 (repeating digits).")
    print("P. Print current list.")
    print("N. Generating a list of random items (you give the number of numbers to generate, and the range, the random module is used)")
    print("E. Exit")

def main():
    numbers = []
    while True:
        print_menu()
        option = input("Choose option: ").strip().upper()

        if option == "1":
            numbers = read_numbers()
        elif option == "2":
            result = get_longest_sublist_same_parity(numbers)
            print("Longest sublist with same parity elements is:", result)
        elif option == "3":
            numbers = remove_repeating_digit_numbers(numbers)
            print("List after removing elements with repeating digits:", numbers)
        elif option == "P":
            print("The current list is:", numbers)
        elif option == "N":
            generate_random_items()
        elif option == "E":
            print("Exiting program...")
            break
        else:
            print("Invalid option! Try again.")

if __name__ == "__main__":
    main()
