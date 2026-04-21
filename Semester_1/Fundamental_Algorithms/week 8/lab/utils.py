import datetime
def str_to_datetime(date_str: str, time_str: str):
  """
  Converts date and time strings to a datetime object.
  Args:
    date_str (str): The date string in 'YYYY-MM-DD'
    time_str (str): The time string in 'HH:MM'

  Returns:
    datetime.datetime: The corresponding datetime object, or None if invalid format.
  """
  try:
    date_parts = [int(part) for part in date_str.split('-')]
    time_parts = [int(part) for part in time_str.split(':')]
    return datetime.datetime(date_parts[0], date_parts[1], date_parts[2],
                             time_parts[0], time_parts[1])
  except ValueError:
    return None