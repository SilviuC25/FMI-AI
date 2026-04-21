from domain import *
from services import *
from ui import *


def add_default_concerts(concerts):
  concert1 = create_concert("Artist A", "City X", "15/08/2023", 50)
  concert2 = create_concert("Artist B", "City Y", "20/09/2023", 75)
  concert3 = create_concert("Artist A", "City Z", "05/10/2023", 60)
  concert4 = create_concert("Artist C", "City X", "12/11/2023", 80)
  add_concert_to_list(concerts, concert1)
  add_concert_to_list(concerts, concert2)
  add_concert_to_list(concerts, concert3)
  add_concert_to_list(concerts, concert4)

def main():
  concerts = []
  concerts_history = []
  add_default_concerts(concerts)
  concerts_history.append(concerts[:])

  while True:
    print_default_menu()
    command = input("Enter command: ").strip().upper()

    if command == "ADD":
      artist, city, date, price = read_add_concert_params()
      concert = create_concert(artist, city, date, price)
      add_concert_to_list(concerts, concert)
      print("Concert added successfully.")

    elif command == "MODIFY":
      index, new_date, new_price = read_modify_concert_params()
      if modify_concert(concerts, index, new_date, new_price):
        print("Concert modified successfully.")
      else:
        print("Invalid concert index.")

    elif command == "REMOVE":
      print_remove_menu()
      option = read_remove_option()

      if option == 1:
        artist = read_artist_name()
        updated_concerts = remove_concerts_by_artist(concerts, artist)
        concerts.clear()
        concerts.extend(updated_concerts)
        print(f"All concerts by {artist} have been removed.")
      elif option == 2:
        min_price, max_price = read_price_interval()
        updated_concerts = remove_concerts_by_price_interval(concerts, min_price, max_price)
        concerts.clear()
        concerts.extend(updated_concerts)
        print(f"All concerts with prices between {min_price} and {max_price} have been removed.")
      elif option == 3:
        start_date, end_date = read_date_interval()
        updated_concerts = remove_concerts_by_time_interval(concerts, start_date, end_date)
        concerts.clear()
        concerts.extend(updated_concerts)
        print(f"All concerts between {start_date} and {end_date} have been removed.")

    elif command == "PRINT":
      print_prints_menu()
      option = read_print_menu_option()

      if option == 1:
        city = read_city_name()
        city_concerts = display_concerts_by_city(concerts, city)
        print_concerts(city_concerts)
      elif option == 2:
        city = read_city_name()
        artist = read_artist_name()
        city_artist_concerts = display_concerts_by_city_andartist(concerts, city, artist)
        print_concerts(city_artist_concerts)
      elif option == 3:
        price = read_price_limit()
        cheap_concerts = display_concerts_below_price(concerts, price)
        print_concerts(cheap_concerts)

    elif command == "REPORT":
      print_reports_menu()
      option = read_report_option()

      if option == 1:
        artist = read_artist_name()
        average_price = calculate_average_price(artist, concerts)
        print(f"The average price of {artist}'s concerts is {average_price}")
      elif option == 2:
        print_concerts_count_per_city(concerts)
      elif option == 3:
        start_date, end_date = read_date_interval()
        interval_concerts = get_concerts_in_date_interval(concerts, start_date, end_date)
        sorted_concerts = sort_concerts_by_price(interval_concerts)
        print_concerts(sorted_concerts)
      elif option == 4:
        start_date, end_date = read_date_interval()
        city = read_city_name()
        interval_concerts = get_concerts_in_date_interval(concerts, start_date, end_date)
        city_concerts = display_concerts_by_city(interval_concerts, city)
        print_concerts(city_concerts)
        

    elif command == "FILTER":
      print_filter_menu()
      option = read_filter_option()

      if option == 1:
        """
        Eliminate concerts by artists in a user-given list for which ticket prices are greater thanagiven price. For example, if user inputs Muse, Taylor Swift and 200, all the concerts fromTaylor Swift
        and Muse for which the price is greater than 200 are removed. Any concerts by Taylor Swift or
        Muse for which ticket prices are lower remain in the list.
        """
        artists, price = read_artists_and_price()
        concerts = filter_concerts_by_artists_and_price(concerts, artists, price)
      elif option == 2:
        """ 
        Eliminate concerts for which the ticket price exceeds a given value or the date is after agiven date.
        """
        max_price, date = read_price_and_date()
        concerts = filter_concerts_by_price_and_date(concerts, price, date)

    elif command == "UNDO":
      concerts = undo_last_operation(concerts_history)

    else:
      print("Unknown command. Please try again.")

    if command in ["ADD", "MODIFY", "REMOVE", "FILTER"]:
      concerts_history.append(concerts[:])

    print_all_concerts(concerts)
    

if __name__ == "__main__":
  main()