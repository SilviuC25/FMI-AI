from domain import create_concert
from services import add_concert_to_list, modify_concert, calculate_average_price
from ui import *

concerts = []

def main():
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

    elif command == "PRINT":
      pass

    elif command == "REPORT":
      print_reports_menu()
      option = read_report_option()

      if option == 1:
        artist = read_artist_name()
        average_price = calculate_average_price(artist, concerts)
        print(f"The average price of {artist}'s concerts is {average_price}")

    elif command == "FILTER":
      pass

    elif command == "UNDO":
      pass

    else:
      print("Unknown command. Please try again.")
  
    print("The current concerts list:")
    for i, concert in enumerate(concerts):
      print(f"{i + 1}. {concert['artist']} in {concert['city']} on {concert['date']} - ${concert['price']}")

if __name__ == "__main__":
  main()