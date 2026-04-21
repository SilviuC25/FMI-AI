from datetime import datetime

def is_valid_date(date_str: str) -> bool:
    """
    Checks if the given string is a valid date in DD/MM/YYYY format.
    Returns True if valid, False otherwise.
    """
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def is_positive_number(value: float) -> bool:
    """
    Checks if a number is positive.
    """
    return value > 0

def is_non_empty_string(value: str) -> bool:
    """
    Checks if a string is not empty and does not contain only spaces.
    """
    return bool(value.strip())

def get_artist(concert):
    return concert["artist"]

def get_city(concert):
    return concert["city"]

def get_date(concert):
    return concert["date"]

def get_price(concert):
    return concert["price"]