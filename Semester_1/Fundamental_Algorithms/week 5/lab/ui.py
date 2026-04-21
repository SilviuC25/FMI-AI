from utils import *
from domain import *

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

def read_remove_option():
    """
    Reads the removal option from the user.
    Returns the selected option as an integer.
    """
    while True:
        try:
            option = int(input("Select removal option (1-3): "))
            if option in [1, 2, 3]:
                return option
            else:
                print("Option must be between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter an integer between 1 and 3.")
    
def read_artist_name():
    artist = input("Enter the artist's name: ")
    return artist

def read_price_interval():
    while True:
        try:
            min_price = float(input("Enter minimum price: "))
            max_price = float(input("Enter maximum price: "))
            if min_price <= max_price:
                return min_price, max_price
            else:
                print("Minimum price must be less than or equal to maximum price.")
        except ValueError:
            print("Invalid input. Please enter numeric values for prices.")

def read_date_interval():
    while True:
        start_date = input("Enter start date (DD/MM/YYYY): ").strip()
        end_date = input("Enter end date (DD/MM/YYYY): ").strip()
        if is_valid_date(start_date) and is_valid_date(end_date):
            if start_date <= end_date:
                return start_date, end_date
            else:
                print("Start date must be earlier than or equal to end date.")
        else:
            print("Invalid date format. Please enter dates in DD/MM/YYYY format.")

def read_print_menu_option():
    """
    Reads the print menu option from the user.
    Returns the selected option as an integer.
    """
    while True:
        try:
            option = int(input("Select print option (1-3): "))
            if option in [1, 2, 3,]:
                return option
            else:
                print("Option must be between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter an integer between 1 and 4.")

def read_city_name():
    city = input("Enter the city name: ")
    return city

def print_concerts(concerts):
    if not concerts:
        print("No concerts to display.")
        return

    for i, concert in enumerate(concerts, start=1):
        artist = get_artist(concert)
        city = get_city(concert)
        date = get_date(concert)
        price = get_price(concert)
        print(f"{i}. Artist: {artist}, City: {city}, Date: {date}, Price: {price}")

def read_price_limit():
    while True:
        try:
            price = float(input("Enter the price limit: "))
            if is_positive_number(price):
                return price
            else:
                print("Price must be a positive number.")
        except ValueError:
            print("Invalid input. Please enter a numeric value for the price.")

def print_prints_menu():
    print("1. Display all concerts in a given city.")
    print("2. Display all concerts in a given city by a given artist.")
    print("3. Display all concerts below a given price.")

def print_concerts_count_per_city(concerts):
    city_count = {}
    for concert in concerts:
        city = get_city(concert)
        if city in city_count:
            city_count[city] += 1
        else:
            city_count[city] = 1

    for city, count in city_count.items():
        print(f"{city}: {count} concert(s)")

def print_all_concerts(concerts):
    print("The current concerts list:")
    for i, concert in enumerate(concerts):
      artist = get_artist(concert)
      city = get_city(concert)
      date = get_date(concert)
      price = get_price(concert)
      print(f"{i + 1}. {artist} in {city} on {date} - ${price}")

def print_filter_menu():
    print("1. Eliminate concerts by artists in a user-given list for which ticket prices are greater thanagiven price")
    print("2. Eliminate concerts for which the ticket price exceeds a given value or the date is after agiven date.")

def read_filter_option():
    """
    Reads the filter option from the user.
    Returns the selected option as an integer.
    """
    while True:
        try:
            option = int(input("Select filter option (1-2): "))
            if option in [1, 2]:
                return option
            else:
                print("Option must be between 1 and 2.")
        except ValueError:
            print("Invalid input. Please enter an integer between 1 and 2.")

def read_artists_and_price():
    artists_input = input("Enter artist names separated by commas: ")
    artists = [artist.strip() for artist in artists_input.split(",") if artist.strip()]
    
    while True:
        try:
            price = float(input("Enter the price limit: "))
            if is_positive_number(price):
                return artists, price
            else:
                print("Price must be a positive number.")
        except ValueError:
            print("Invalid input. Please enter a numeric value for the price.")

def read_price_and_date():
    while True:
        try:
            price = float(input("Enter the price limit: "))
            if is_positive_number(price):
                break
            else:
                print("Price must be a positive number.")
        except ValueError:
            print("Invalid input. Please enter a numeric value for the price.")

    while True:
        date = input("Enter the date (DD/MM/YYYY): ").strip()
        if is_valid_date(date):
            return price, date
        print("Invalid date format. Please enter in DD/MM/YYYY format.")

