def create_concert(artist, city, date, price):
  """
  Creates a concert dictionary with the given details.
  Args:
    artist (str): The name of the artist or band.
    city (str): The city where the concert will take place.
    date (str): The date of the concert.
    price (float): The price of the concert ticket.
  """
  concert = {
    "artist": artist,
    "city": city,
    "date": date,
    "price": price
  }
  return concert

