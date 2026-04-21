from utils import convert_string_to_date
from domain import *

def create_concert(artist, city, date, price):
  """
  Creates a concert list with the given details.
  Args:
      artist (str): The name of the artist.
      city (str): The city where the concert takes place.
      date (str): The date of the concert in DD/MM/YYYY format.
      price (float): The ticket price for the concert.
  Returns:
      concert (list): A list representing the concert.
  """
  concert = []
  concert.append(artist)
  concert.append(city)
  concert.append(date)
  concert.append(price)

  return concert

def concert_param_index(param):
  param_indices = {
      "artist": 0,
      "city": 1,
      "date": 2,
      "price": 3
  }
  return param_indices[param]

def get_artist(concert):
    return concert[concert_param_index("artist")]

def get_city(concert):
    return concert[concert_param_index("city")]

def get_date(concert):
    return concert[concert_param_index("date")]

def get_price(concert):
    return concert[concert_param_index("price")]

def get_concerts_in_date_interval(concerts, start_date, end_date):
    # Get all concerts within a given date interval.
    start_date = convert_string_to_date(start_date)
    end_date = convert_string_to_date(end_date)
    return [concert for concert in concerts if start_date <= convert_string_to_date(get_date(concert)) <= end_date]

def sort_concerts_by_price(concerts):
    # Sort concerts by ticket price in ascending order.
    return sorted(concerts, key=lambda concert: get_price(concert))

def set_date(concert, new_date):
    concert[concert_param_index("date")] = new_date

def set_price(concert, new_price):
    concert[concert_param_index("price")] = new_price

def set_artist(concert, new_artist):
    concert[concert_param_index("artist")] = new_artist

def set_city(concert, new_city):
    concert[concert_param_index("city")] = new_city