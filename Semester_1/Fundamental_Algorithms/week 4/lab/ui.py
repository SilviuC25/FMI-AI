from utils import *

def print_default_menu():
  print("ADD. Add a new concert with data provided by the user (artist, city, date, ticket price).")
  print("MODIFY. Modify the information of an existing concert.")
  print("REMOVE. Remove the concerts that meet certain criteria.")
  print("PRINT. Display the concerts that meet certain criteria.")
  print("REPORT. Generate reports based on concerts list data.")
  print("FILTER. Removing all concerts that meet a given criteria from the list of concerts.")
  print("UNDO. Revert the last operation that modified the concerts list.")

def print_remove_menu():
  print("1. Delete all concerts for a given artist.")
  print("2. Delete all concerts with ticket prices in a given interval.")
  print("3. Delete all concerts taking place in a given interval.")

def print_reports_menu():
    print("1. Print the average ticket price for a given artist.")
    print("2. Print the number of concerts per city.")
    print("3. Print the the concerts in a given interval (e.g. 11/09/2026 - 13/09/2026), sorted inascending order by ticket price.")
    print("4. Print the concerts from a given interval (e.g. 11/09/2026 - 13/09/2026) which take place ina given city (e.g. Berlin).")

def read_add_concert_params():
    """
    Reads concert parameters from the user, with validation for each field.
    Returns a tuple: (artist, city, date, price)
    """
    # Validate artist
    while True:
        artist = input("Enter the artist's name: ").strip()
        if is_non_empty_string(artist):
            break
        print("Artist name cannot be empty.")

    # Validate city
    while True:
        city = input("Enter the city: ").strip()
        if is_non_empty_string(city):
            break
        print("City name cannot be empty.")

    # Validate date
    while True:
        date = input("Enter the date (DD/MM/YYYY): ").strip()
        if is_valid_date(date):
            break
        print("Invalid date format. Please enter in DD/MM/YYYY format.")

    # Validate price
    while True:
        try:
            price = float(input("Enter the ticket price: "))
            if is_positive_number(price):
                break
            else:
                print("Price must be a positive number.")
        except ValueError:
            print("Invalid input. Please enter a numeric value for the price.")

    return artist, city, date, price


def read_modify_concert_params():
    """
    Reads parameters for modifying an existing concert.
    User can leave fields empty to keep existing values.
    Returns: (index, new_date, new_price)
    """
    # Validate index input
    while True:
        try:
            index = int(input("Enter the concert index to modify: ")) - 1
            if index >= 0:
                break
            else:
                print("Index must be a positive number.")
        except ValueError:
            print("Invalid input. Please enter an integer index.")

    # Validate new date
    while True:
        new_date = input("Enter new date (DD/MM/YYYY) or leave empty to keep: ").strip()
        if new_date == "" or is_valid_date(new_date):
            break
        print("Invalid date format. Please enter in DD/MM/YYYY format or leave empty.")

    # Validate new price
    while True:
        new_price_input = input("Enter new price or leave empty to keep: ").strip()
        if new_price_input == "":
            new_price = None
            break
        try:
            new_price = float(new_price_input)
            if is_positive_number(new_price):
                break
            else:
                print("Price must be a positive number.")
        except ValueError:
            print("Invalid input. Please enter a numeric value or leave empty.")

    return index, new_date if new_date != "" else None, new_price

def read_report_option():
    """
    Reads parameters for generating reports.
    Returns the selected report option and any necessary parameters.
    """
    while True:
        try:
            option = int(input("Select report option (1-4): "))
            if option in [1, 2, 3, 4]:
                return option
                break
            else:
                print("Option must be between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter an integer between 1 and 4.")

    
def read_artist_name():
    artist = input("Enter the artist's name: ")
    return artist