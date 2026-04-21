from utils import *

def add_concert_to_list(concerts, concert):
  # Adds a concert to the list.
  concerts.append(concert)
  return concerts

def modify_concert(concerts, index, new_date=None, new_price=None):
    """
    Modify the date and/or price of a concert at a specific index in the list.
    Returns True if modified, False if index not valid.
    """
    if 0 <= index < len(concerts):
        if new_date is not None:
            concerts[index]["date"] = new_date
        if new_price is not None:
            concerts[index]["price"] = float(new_price)
        return True
    return False

def calculate_average_price(artist, concerts):
    # Print the average price of a given artist.
    total_price = 0
    no_concerts = 0

    for concert in concerts:
        if get_artist(concert) == artist:
            total_price = total_price + concert["price"]
            no_concerts = no_concerts + 1

    if no_concerts == 0:
        return 0

    average_price = total_price / no_concerts
    return average_price