from utils import *
from domain import *

def add_concert_to_list(concerts, concert):
   """
   Adds a concert to the list.
   Param:
        concerts -> list of all concerts,
        concert -> list, the concert the will be added
    Returns:
        concerts -> list of concerts after the add operation
   """
   concerts.append(concert)

def modify_concert(concerts, index, new_date=None, new_price=None):
    """
    Modify the date and/or price of a concert at a specific index in the list.
    Param:
        concerts -> list of all concerts,
        index -> int, the index of the concert list
        new_date -> date, the new date of the concert
        new_price -> date, the new price of the concert
    Returns:
        True if modified, False if index not valid.
    """
    if 0 <= index < len(concerts):
        if new_date is not None:
            set_date(concerts[index], new_date)
        if new_price is not None:
            set_price(concerts[index], new_price)
        return True
    return False
    

def calculate_average_price(artist, concerts):
    """
    Print the average price of a given artist.
    Param:
        artist -> string, artist's name
        concerts -> list of all concerts,
    Returns:
        average_price -> float, average price of the artist's concerts
    """
    total_price = 0
    no_concerts = 0

    for concert in concerts:
        if get_artist(concert) == artist:
            total_price = total_price + get_price(concert)
            no_concerts = no_concerts + 1

    if no_concerts == 0:
        return 0

    average_price = total_price / no_concerts
    return average_price

def remove_concerts_by_artist(concerts, artist):
    """
    Remove all concerts by a given artist.
    Param:
        concerts -> list of all concerts,
        artist -> string, artist's name
    Returns:
        concerts -> list of concerts after removing concerts from the artist
    """
    return [concert for concert in concerts if get_artist(concert) != artist]

def remove_concerts_by_price_interval(concerts, min_price, max_price):
    """
    Remove all concerts within a given price interval.
    Param:
        concerts -> list of all concerts,
        artist -> string, artist's name,
        min_price -> float
        max_price -> float
    Returns:
        concerts -> list of concerts after removing concerts from the given price interval
    """
    return [concert for concert in concerts if not (min_price <= get_price(concert) <= max_price)]

def remove_concerts_by_time_interval(concerts, start_date, end_date):
    """
    Remove all concerts within a given time interval.
    Param:
        concerts -> list of all concerts,
        start_date -> date, the start limit of the time interval
        end_date -> date, the end limit of the time interVAL
    Returns:
        concerts -> list of concerts after removing concerts in the given time interval
    """
    start_date = convert_string_to_date(start_date)
    end_date = convert_string_to_date(end_date)
    return [concert for concert in concerts if not (start_date <= convert_string_to_date(get_date(concert)) <= end_date)]

def display_concerts_by_city(concerts, city):
    """
    Display all concerts in a given city.
    Param:
        concerts -> list of all concerts,
        city -> string, the city's name
    Returns:
        concerts -> list, from a given city
    """
    return [concert for concert in concerts if get_city(concert) == city]

def display_concerts_by_city_andartist(concerts, city, artist):
    """
    Display all concerts in a given city by a given artist.
    Param:
        concerts -> list of all concerts,
        city -> string, the city's name
        artist -> string, the artist's name
    Returns:
        concerts -> list, from artist and given city
    """
    return [concert for concert in concerts if get_city(concert) == city and get_artist(concert) == artist]

def display_concerts_below_price(concerts, price):
    """
    Display all concerts below a given price.
    Param:
        concerts -> list of all concerts,
        price -> positive int, the price limit for concerts
    Returns:
        concerts -> list, concerts below the price
    """
    return [concert for concert in concerts if get_price(concert) < price]

def filter_concerts_by_artists_and_price(concerts, artists, max_price):
    """
    Remove concerts that match both: artist in given list AND price <= max_price.
    Param:
        concerts -> list of all concerts,
        artists -> list of artists to filter
        max_price -> positive int, the max price value for tickets
    Returns:
        concerts -> the remaining list of concerts after filtering them
    """
    return [concert for concert in concerts
            if not (get_artist(concert) in artists and get_price(concert) <= max_price)]


def filter_concerts_by_price_and_date(concerts, max_price, max_date):
    """
    Remove concerts that match both: price <= max_price AND date <= max_date.
    Param:
        concerts -> list of all concerts,
        max_price -> positive int, the max price value for tickets,
        max_date -> date, the date limit for concert date
    Returns:
        concerts -> the remaining list of concerts after filtering them
    """
    max_date = convert_string_to_date(max_date)
    return [concert for concert in concerts
            if not (get_price(concert) <= max_price and convert_string_to_date(get_date(concert)) <= max_date)]


def undo_last_operation(concerts_history):
    """
    Undo the last operation performed on the concert list.
    Param:
        concerts_history -> list of all concerts history,
    Returns:
        concerts -> the concert's list after undo operation
    """
    if concerts_history:
        concerts_history.pop()
        return concerts_history[-1] if concerts_history else []
    else:
        print("No more undos available.")
        return []
